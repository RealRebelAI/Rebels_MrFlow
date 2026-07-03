# ComfyUI-Rebels-MrFlow
# MrFlow staged sampling (training-free acceleration) ported to Z-Image (ZIT) and Krea-2.
#
# Method credit: MrFlow — Xingyu-Zheng et al.
#   https://github.com/Xingyu-Zheng/MrFlow  (arXiv:2607.01642)
# Port: RealRebelAI
#
# Pipeline (all training-free):
#   Stage 1: sample the composition at LOW resolution with your normal KSampler
#   Stage 2: VAE-decode, upscale in pixel space with an SR model (RealESRGAN x2 etc.)
#   Stage 3: VAE re-encode the upscaled image
#   Stage 4: inject scheduler-consistent low-strength noise + short refine pass
#
# Works with any loader that outputs a normal MODEL (GGUF, NF4, FP8, safetensors).

from __future__ import annotations

import math

import torch

import comfy.sample
import comfy.samplers
import comfy.utils
import folder_paths  # noqa: F401  (kept for parity / future model-dir use)

try:
    import latent_preview
except Exception:  # pragma: no cover
    latent_preview = None

from nodes import MAX_RESOLUTION


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _resize_image(image: torch.Tensor, width: int, height: int, method: str = "bicubic") -> torch.Tensor:
    samples = image.movedim(-1, 1)
    resized = comfy.utils.common_upscale(samples, width, height, method, "disabled")
    return resized.movedim(1, -1)


def _flowmatch_shift(t: torch.Tensor, mu: float, sigma: float = 1.0) -> torch.Tensor:
    exp_mu = math.exp(mu)
    return exp_mu / (exp_mu + (1.0 / t - 1.0) ** sigma)


def _shifted_sigmas(first_sigma: float, steps: int, device) -> torch.Tensor:
    # Matches upstream ComfyUI-MrFlow "direct sigma" path (flowmatch-shifted).
    if steps == 1:
        return torch.tensor([float(first_sigma), 0.0], dtype=torch.float32, device=device)
    base = torch.linspace(1.0, 0.0, steps + 1, dtype=torch.float32, device=device)
    mu = 0.25 * float(steps - 1)
    shifted = _flowmatch_shift(base.clamp(1.0e-6, 1.0 - 1.0e-6), mu=mu)
    shifted = shifted - shifted[-1]
    shifted = shifted / shifted[0]
    shifted = shifted * float(first_sigma)
    shifted[0] = float(first_sigma)
    shifted[-1] = 0.0
    return shifted


def _linear_sigmas(first_sigma: float, steps: int, device) -> torch.Tensor:
    # Matches upstream Z-Image diffusers demo (plain linear ramp from strength -> 0).
    return torch.linspace(float(first_sigma), 0.0, steps + 1, dtype=torch.float32, device=device)


def _build_sigmas(schedule: str, first_sigma: float, steps: int, device) -> torch.Tensor:
    if not 0.0 < first_sigma < 1.0:
        raise ValueError(f"refine denoise must be in (0, 1), got {first_sigma}")
    if steps <= 0:
        raise ValueError(f"refine steps must be positive, got {steps}")
    if schedule == "shifted":
        return _shifted_sigmas(first_sigma, steps, device)
    return _linear_sigmas(first_sigma, steps, device)


def _run_upscale_model(upscale_model, image):
    # Compat shim across ComfyUI versions (V3 classmethod vs legacy instance method).
    from comfy_extras.nodes_upscale_model import ImageUpscaleWithModel
    if hasattr(ImageUpscaleWithModel, "execute"):
        try:
            return ImageUpscaleWithModel.execute(upscale_model, image)[0]
        except TypeError:
            return ImageUpscaleWithModel().execute(upscale_model, image)[0]
    return ImageUpscaleWithModel().upscale(upscale_model, image)[0]


def _fix_latent_channels(model, latent_samples, latent_dict):
    # Newer ComfyUI takes downscale ratios; older takes (model, latent) only.
    try:
        return comfy.sample.fix_empty_latent_channels(
            model,
            latent_samples,
            latent_dict.get("downscale_ratio_spacial", None),
            latent_dict.get("downscale_ratio_temporal", None),
        )
    except TypeError:
        return comfy.sample.fix_empty_latent_channels(model, latent_samples)


def _round16(value: float) -> int:
    return max(16, int(round(value / 16.0)) * 16)


# ---------------------------------------------------------------------------
# preset nodes
# ---------------------------------------------------------------------------

class RebelsMrFlowPresetBase:
    """Outputs the MrFlow staged-sampling numbers for a target resolution."""

    PRESETS: dict = {}
    DEFAULT_PRESET: str = ""
    CATEGORY = "Rebels/MrFlow"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "target_width": ("INT", {"default": 1024, "min": 64, "max": MAX_RESOLUTION, "step": 16}),
                "target_height": ("INT", {"default": 1024, "min": 64, "max": MAX_RESOLUTION, "step": 16}),
                "preset": (list(cls.PRESETS.keys()), {"default": cls.DEFAULT_PRESET}),
                "upscale_factor": ("FLOAT", {"default": 2.0, "min": 1.0, "max": 8.0, "step": 0.05}),
            }
        }

    RETURN_TYPES = ("INT", "INT", "INT", "INT", "FLOAT", "INT", "INT", "FLOAT")
    RETURN_NAMES = (
        "low_width",
        "low_height",
        "target_width",
        "target_height",
        "refine_denoise",
        "stage1_steps",
        "refine_steps",
        "cfg",
    )
    FUNCTION = "build"

    def build(self, target_width: int, target_height: int, preset: str, upscale_factor: float):
        low_width = _round16(target_width / upscale_factor)
        low_height = _round16(target_height / upscale_factor)
        cfg = self.PRESETS[preset]
        return (
            low_width,
            low_height,
            target_width,
            target_height,
            cfg["denoise"],
            cfg["stage1_steps"],
            cfg["refine_steps"],
            cfg["cfg"],
        )


class RebelsMrFlowZITPreset(RebelsMrFlowPresetBase):
    # Z-Image Turbo. "9plus1" matches the official MrFlow Z-Image Turbo demo:
    # 9 low-res steps, 1 refine step at strength 0.11, no CFG (cfg 1.0 in Comfy).
    PRESETS = {
        "9plus1 (paper)": {"denoise": 0.11, "stage1_steps": 9, "refine_steps": 1, "cfg": 1.0},
        "9plus2 (detail)": {"denoise": 0.13, "stage1_steps": 9, "refine_steps": 2, "cfg": 1.0},
        "12plus1 (quality)": {"denoise": 0.11, "stage1_steps": 12, "refine_steps": 1, "cfg": 1.0},
    }
    DEFAULT_PRESET = "9plus1 (paper)"
    CATEGORY = "Rebels/MrFlow/ZIT"


class RebelsMrFlowKrea2Preset(RebelsMrFlowPresetBase):
    # Krea-2. Starting points following the MrFlow "12plus1"/"20plus1" regime for
    # full CFG base models, plus a distilled/turbo preset mirroring the ZIT numbers.
    PRESETS = {
        "base_12plus1": {"denoise": 0.12, "stage1_steps": 12, "refine_steps": 1, "cfg": 4.0},
        "base_20plus1": {"denoise": 0.15, "stage1_steps": 20, "refine_steps": 1, "cfg": 4.0},
        "turbo_8plus1": {"denoise": 0.11, "stage1_steps": 8, "refine_steps": 1, "cfg": 1.0},
    }
    DEFAULT_PRESET = "base_12plus1"
    CATEGORY = "Rebels/MrFlow/Krea-2"


# ---------------------------------------------------------------------------
# upscale + re-encode (shared, backbone-neutral)
# ---------------------------------------------------------------------------

class RebelsMrFlowUpscaleEncode:
    CATEGORY = "Rebels/MrFlow"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "vae": ("VAE",),
                "upscale_model": ("UPSCALE_MODEL",),
                "target_width": ("INT", {"default": 1024, "min": 64, "max": MAX_RESOLUTION, "step": 16}),
                "target_height": ("INT", {"default": 1024, "min": 64, "max": MAX_RESOLUTION, "step": 16}),
                "resize_method": (["bicubic", "bilinear", "area", "nearest-exact"], {"default": "bicubic"}),
            }
        }

    RETURN_TYPES = ("IMAGE", "LATENT")
    RETURN_NAMES = ("upscaled_image", "prepared_latent")
    FUNCTION = "prepare"

    def prepare(self, image, vae, upscale_model, target_width: int, target_height: int, resize_method: str):
        # Stage 2: pixel-space super resolution.
        upscaled = _run_upscale_model(upscale_model, image)
        if upscaled.shape[2] != target_width or upscaled.shape[1] != target_height:
            upscaled = _resize_image(upscaled, target_width, target_height, method=resize_method)

        # Stage 3: re-encode for the refine pass. Encode per-image to keep 8GB cards happy.
        if upscaled.shape[0] > 1:
            latent_batches = []
            for i in range(upscaled.shape[0]):
                latent_batches.append(vae.encode(upscaled[i:i + 1]))
            encoded_latent = torch.cat(latent_batches, dim=0)
        else:
            encoded_latent = vae.encode(upscaled)
        return (upscaled, {"samples": encoded_latent})


# ---------------------------------------------------------------------------
# refine nodes
# ---------------------------------------------------------------------------

class RebelsMrFlowRefineBase:
    """Stage 4: inject matched noise and denoise along an explicit sigma path."""

    CATEGORY = "Rebels/MrFlow"
    DEFAULT_DENOISE = 0.12
    DEFAULT_STEPS = 1
    DEFAULT_CFG = 4.0
    DEFAULT_SCHEDULE = "linear"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "vae": ("VAE",),
                "positive": ("CONDITIONING",),
                "negative": ("CONDITIONING",),
                "latent_image": ("LATENT",),
                "seed": ("INT", {"default": 2026, "min": 0, "max": 0xFFFFFFFFFFFFFFFF, "control_after_generate": True}),
                "steps": ("INT", {"default": cls.DEFAULT_STEPS, "min": 1, "max": 10000}),
                "cfg": ("FLOAT", {"default": cls.DEFAULT_CFG, "min": 0.0, "max": 100.0, "step": 0.1, "round": 0.01}),
                "sampler_name": (comfy.samplers.KSampler.SAMPLERS,),
                "denoise": ("FLOAT", {"default": cls.DEFAULT_DENOISE, "min": 0.0, "max": 1.0, "step": 0.01, "round": 0.001}),
                "schedule": (["linear", "shifted"], {"default": cls.DEFAULT_SCHEDULE}),
                "print_schedule": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("LATENT", "IMAGE")
    RETURN_NAMES = ("refined_latent", "refined_image")
    FUNCTION = "refine"

    def refine(self, model, vae, positive, negative, latent_image, seed, steps, cfg,
               sampler_name, denoise, schedule, print_schedule):
        latent = latent_image.copy()
        latent_samples = _fix_latent_channels(model, latent["samples"], latent)
        latent["samples"] = latent_samples

        noise = comfy.sample.prepare_noise(latent_samples, seed, latent.get("batch_index", None))
        noise_mask = latent.get("noise_mask", None)

        sigmas = _build_sigmas(schedule, denoise, steps, device=model.load_device)
        if print_schedule:
            print(f"[Rebels MrFlow] refine sigmas ({schedule}): {sigmas.tolist()}")

        sampler = comfy.samplers.sampler_object(sampler_name)
        callback = None
        if latent_preview is not None:
            try:
                callback = latent_preview.prepare_callback(model, sigmas.shape[-1] - 1)
            except Exception:
                callback = None
        disable_pbar = not comfy.utils.PROGRESS_BAR_ENABLED

        refined_samples = comfy.sample.sample_custom(
            model,
            noise,
            cfg,
            sampler,
            sigmas,
            positive,
            negative,
            latent_samples,
            noise_mask=noise_mask,
            callback=callback,
            disable_pbar=disable_pbar,
            seed=seed,
        )

        refined_latent = latent.copy()
        refined_latent.pop("downscale_ratio_spacial", None)
        refined_latent.pop("downscale_ratio_temporal", None)
        refined_latent["samples"] = refined_samples

        refined_image = vae.decode(refined_samples)
        if len(refined_image.shape) == 5:
            refined_image = refined_image.reshape(
                -1, refined_image.shape[-3], refined_image.shape[-2], refined_image.shape[-1]
            )
        return (refined_latent, refined_image)


class RebelsMrFlowZITRefine(RebelsMrFlowRefineBase):
    # Z-Image Turbo defaults match the official MrFlow demo: strength 0.11, no CFG,
    # linear sigma ramp (what their diffusers Z-Image pipeline actually runs).
    CATEGORY = "Rebels/MrFlow/ZIT"
    DEFAULT_DENOISE = 0.11
    DEFAULT_STEPS = 1
    DEFAULT_CFG = 1.0
    DEFAULT_SCHEDULE = "linear"


class RebelsMrFlowKrea2Refine(RebelsMrFlowRefineBase):
    CATEGORY = "Rebels/MrFlow/Krea-2"
    DEFAULT_DENOISE = 0.12
    DEFAULT_STEPS = 1
    DEFAULT_CFG = 4.0
    DEFAULT_SCHEDULE = "linear"


# ---------------------------------------------------------------------------
# registration
# ---------------------------------------------------------------------------

NODE_CLASS_MAPPINGS = {
    "RebelsMrFlowZITPreset": RebelsMrFlowZITPreset,
    "RebelsMrFlowKrea2Preset": RebelsMrFlowKrea2Preset,
    "RebelsMrFlowUpscaleEncode": RebelsMrFlowUpscaleEncode,
    "RebelsMrFlowZITRefine": RebelsMrFlowZITRefine,
    "RebelsMrFlowKrea2Refine": RebelsMrFlowKrea2Refine,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RebelsMrFlowZITPreset": "ZIT Mr. Flow Preset",
    "RebelsMrFlowKrea2Preset": "Krea-2 Mr. Flow Preset",
    "RebelsMrFlowUpscaleEncode": "Mr. Flow Upscale + Encode (Rebels)",
    "RebelsMrFlowZITRefine": "ZIT Mr. Flow Refine",
    "RebelsMrFlowKrea2Refine": "Krea-2 Mr. Flow Refine",
}
