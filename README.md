

# ComfyUI-Rebels-MrFlow

**ZIT Mr. Flow** and **Krea-2 Mr. Flow** — MrFlow training-free staged sampling
(low-res generate → pixel SR upscale → re-encode → 1-step refine) ported to
Z-Image Turbo and Krea-2 for ComfyUI.

Method credit: [MrFlow by Xingyu-Zheng et al.](https://github.com/Xingyu-Zheng/MrFlow)
(arXiv:2607.01642). Port by RealRebelAI. Works with GGUF / NF4 / FP8 / safetensors
loaders — anything that outputs a normal MODEL. No extra dependencies.

# Examples
<table>
  <tr>
    <th>Krea-2 - 1024</th>
    <th>Krea-2 - 2048</th>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/06050fd0-684a-402e-bd33-03da89e41d1b" width="350"/></td>
    <td><img src="https://github.com/user-attachments/assets/4bcdda12-26c9-4f1f-b85c-b27359c2364a" width="350"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/f9ddade7-6cdb-4ce9-9b17-eacc8722a0ea" width="350"/></td>
    <td><img src="https://github.com/user-attachments/assets/050f132c-177c-4119-aee7-40096308b483" width="350"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/dd54a6fa-a567-4c42-a794-d04cb8fe8c71" width="350"/></td>
    <td><img src="https://github.com/user-attachments/assets/21a414c1-4b09-4fc2-9764-a7b31ddc35ec" width="350"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/b014c7d6-8468-4b93-9401-93fa298ddcc8" width="350"/></td>
    <td><img src="https://github.com/user-attachments/assets/8cf1b305-0d16-4c66-b695-5cd3596ef88c" width="350"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/71579182-9b1c-483b-be1f-3bd7912ac9a0" width="350"/></td>
    <td><img src="https://github.com/user-attachments/assets/ca03461d-ed17-46ce-9806-de9cb8944bed" width="350"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/fdd19135-a25a-4edb-a34f-6a717cd5d6a8" width="350"/></td>
    <td><img src="https://github.com/user-attachments/assets/cc7dfbb5-f925-4cc8-b0cb-ca2f89670c33" width="350"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/bb866627-4cac-4699-ac98-bfd5d2292e68" width="350"/></td>
    <td><img src="https://github.com/user-attachments/assets/eb625d55-c1bd-43ba-91ce-be5e7e5056ae" width="350"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/eddaa207-e1b7-4c5d-bcc0-7e0d3bdef2dc" width="350"/></td>
    <td><img src="https://github.com/user-attachments/assets/c4d3805b-8630-4935-bf48-31f774e8adfd" width="350"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/6416c0c5-508d-4c6e-8227-34c5825cce0e" width="350"/></td>
    <td><img src="https://github.com/user-attachments/assets/b14c00ee-5bd1-4ca8-86fb-743eff39254a" width="350"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/3aad0d0b-c596-43b6-aff8-9487246d6f87" width="350"/></td>
    <td><img src="https://github.com/user-attachments/assets/f1a916cb-7e76-4119-a021-1b8c7ddffda6" width="350"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/f36303cf-3546-459e-9dc7-16b558143654" width="350"/></td>
    <td><img src="https://github.com/user-attachments/assets/09d2aa2e-4873-4c6a-889f-90c8e5fcc80f" width="350"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/80f36023-6966-40ed-bc1e-5b47f763bb2f" width="350"/></td>
    <td><img src="https://github.com/user-attachments/assets/3c3a5075-bc88-4701-93f9-4dfb96dda8d8" width="350"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/02d3a46a-216f-4ca2-9fa5-d5bd1ed819cf" width="350"/></td>
    <td><img src="https://github.com/user-attachments/assets/105c9b29-49d7-4d0b-a0a2-eaa16984ef7f" width="350"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/078b3200-f399-4af3-b70c-b2b8404e6561" width="350"/></td>
    <td><img src="https://github.com/user-attachments/assets/5568cb59-1776-4da5-a21a-a166656da497" width="350"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/7bc1d80f-2136-4bd9-a95f-7a542ad2c64a" width="350"/></td>
    <td><img src="https://github.com/user-attachments/assets/a092d701-dc54-4266-a0f3-1c7e81b762e1" width="350"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/24ba613e-b2c0-4d6b-ad38-b832fe87a31f" width="350"/></td>
    <td><img src="https://github.com/user-attachments/assets/e8693d44-f99d-4ada-a79f-b604554679f4" width="350"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/d4529288-fd0e-4c96-9074-9eeaa0fc361d" width="350"/></td>
    <td><img src="https://github.com/user-attachments/assets/69a5dd31-1357-4092-bf1b-b89b97a5f8b0" width="350"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/c053e5c9-7b40-4531-badb-cb3634f5fb1d" width="350"/></td>
    <td><img src="https://github.com/user-attachments/assets/8ae3e541-f0be-438b-82f6-a7d7dfc9e20c" width="350"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/5f90cb62-3739-4012-8e52-826d0d2b9969" width="350"/></td>
    <td><img src="https://github.com/user-attachments/assets/eaeec259-274a-4c44-841e-231d8623191b" width="350"/></td>
  </tr>
</table>




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
5. **Load Upscale Model** — RealESRGAN x2 for 1024 → **Mr. Flow Upscale + Encode**
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

- Use a real SR model for stage 2 (RealESRGAN x2 for 1024)
  Plain latent upscaling defeats the whole method.
  
  - grab `RealESRGAN_x2plus.pth` from the [official releases page](https://huggingface.co/rklaumbach/RealESRGAN_x2/blob/main/RealESRGAN_x2.pth)
  

  and place it in `ComfyUI/models/upscale_models/` yourself.
  
- The Qwen `reference_latents` attach from upstream is intentionally omitted —
  it's a Qwen-Image-specific conditioning mechanism that Z-Image and Krea-2 don't use.
- Total budget: dominated by the cheap low-res pass; the refine is 1 step at
  full res. On 8GB VRAM this is a big win vs. sampling at target res directly.
