# ComfyUI-Rebels-MrFlow

**ZIT Mr. Flow** and **Krea-2 Mr. Flow** — MrFlow training-free staged sampling
(low-res generate → pixel SR upscale → re-encode → 1-step refine) ported to
Z-Image Turbo and Krea-2 for ComfyUI.

Method credit: [MrFlow by Xingyu-Zheng et al.](https://github.com/Xingyu-Zheng/MrFlow)
(arXiv:2607.01642). Port by RealRebelAI. Works with GGUF / NF4 / FP8 / safetensors
loaders — anything that outputs a normal MODEL. No extra dependencies.

# Examples
- Krea-2 (1024)
<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/c138d08e-d5aa-4476-83ed-931ad1490db2" width="280"/></td>
    <td><img src="https://github.com/user-attachments/assets/650e06bb-8b54-4036-b6c9-db8c1e788454" width="280"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/5d166223-365a-4452-a727-4626a3d60052" width="280"/></td>
    <td><img src="https://github.com/user-attachments/assets/7c1c3484-55ff-4865-a6c4-a13058ace19b" width="280"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/143576bd-9b94-473c-8a91-f3ea131adc56" width="280"/></td>
    <td><img src="https://github.com/user-attachments/assets/83999bb1-2b03-4fd5-a1cf-e83c1dd3a0e1" width="280"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/6ed924e9-d48b-4625-8551-a378fd5cf455" width="280"/></td>
    <td><img src="https://github.com/user-attachments/assets/b80a4361-aeb6-4134-8b0c-3af117c644ec" width="280"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/f5b60a6b-380c-4bd9-b18d-71f3e50ab9ec" width="280"/></td>
    <td><img src="https://github.com/user-attachments/assets/bd2f2bfb-1419-48e9-add2-0068f67e3242" width="280"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/232e2c82-42e2-494b-b5db-72cdf302b44c" width="280"/></td>
    <td><img src="https://github.com/user-attachments/assets/ef88b306-260d-4c02-b60b-4004ddd40926" width="280"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/657dfb0a-0b01-4e70-aa1c-b7d657d1dc5e" width="280"/></td>
    <td><img src="https://github.com/user-attachments/assets/d3033052-a7e4-4939-8cbb-a6438655144e" width="280"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/d5b86858-2b46-461d-b127-b5de14da088b" width="280"/></td>
    <td><img src="https://github.com/user-attachments/assets/1ea7f636-12cf-4a74-9c44-e21035d46a10" width="280"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/873e2fed-d777-48fc-8183-a4d7a00f7aa0" width="280"/></td>
    <td><img src="https://github.com/user-attachments/assets/2d73a4cc-6978-4d3d-9a4c-fd582397f2a1" width="280"/></td>
  </tr>
</table>
- Krea-2 (2048)

## Nodes

| Node | What it does |
| --- | --- |
| ZIT Mr. Flow Preset / Krea-2 Mr. Flow Preset | Outputs low-res dims + all stage numbers for your target resolution |
| Mr. Flow Upscale + Encode (Rebels) | Stage 2+3: SR-model pixel upscale, snap to target size, VAE re-encode |
| ZIT Mr. Flow Refine / Krea-2 Mr. Flow Refine | Stage 4: matched noise injection + short explicit-sigma refine |

## Wiring (both models, identical graph)

1. **Preset node** → set `target_width/height`, pick preset.
2. **Empty Latent Image** ← `low_width` / `low_height` from preset.
3. **KSampler (stage 1)** — your normal model/CLIP/VAE loaders, steps ← `stage1_steps`,
   cfg ← `cfg`, sampler `euler`, scheduler `simple`, denoise 1.0.
4. **VAE Decode** stage-1 latent.
5. **Load Upscale Model** — RealESRGAN x2 for 1024 or 4x_foolhardy_Remacri for 2048 → **Mr. Flow Upscale + Encode**
   with the decoded image, your VAE, and `target_width/height` from preset.
6. **Refine node** — same model + conditioning as stage 1, `prepared_latent` in,
   steps ← `refine_steps`, denoise ← `refine_denoise`, cfg ← `cfg`, sampler `euler`.
7. **Save Image** from `refined_image`.

## Presets

- **ZIT `9plus1 (paper)`** — exact official MrFlow Z-Image Turbo demo numbers:
  9 low-res steps + 1 refine step at denoise 0.11, cfg 1.0 (no CFG).
- **Krea-2 `base_12plus1` / `base_20plus1`** — MrFlow's full-CFG regime (Qwen-style),
  cfg 4.0. Starting points — tune denoise 0.10–0.16 to taste.
- **Krea-2 `turbo_8plus1`** — for Krea-2 Turbo, cfg 1.0.

`schedule` on the refine node: `linear` (default, matches the official Z-Image
demo) or `shifted` (matches the official Qwen ComfyUI refine — only differs
when refine steps > 1).

## Notes

- Use a real SR model for stage 2 (RealESRGAN x2 for 1024, 4x_foolhardy_Remacri for 2048).
  Plain latent upscaling defeats the whole method.
  
  - grab `RealESRGAN_x2plus.pth` from the [official releases page](https://huggingface.co/rklaumbach/RealESRGAN_x2/blob/main/RealESRGAN_x2.pth)
    
  - grab `4x_foolhardy_remacri` from the [official release page](https://huggingface.co/FacehugmanIII/4x_foolhardy_Remacri/blob/main/4x_foolhardy_Remacri.pth)

  and place it in `ComfyUI/models/upscale_models/` yourself.
  
- The Qwen `reference_latents` attach from upstream is intentionally omitted —
  it's a Qwen-Image-specific conditioning mechanism that Z-Image and Krea-2 don't use.
- Total budget: dominated by the cheap low-res pass; the refine is 1 step at
  full res. On 8GB VRAM this is a big win vs. sampling at target res directly.
