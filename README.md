# ComfyUI-Rebels-MrFlow

**ZIT Mr. Flow** and **Krea-2 Mr. Flow** — MrFlow training-free staged sampling
(low-res generate → pixel SR upscale → re-encode → 1-step refine) ported to
Z-Image Turbo and Krea-2 for ComfyUI.

Method credit: [MrFlow by Xingyu-Zheng et al.](https://github.com/Xingyu-Zheng/MrFlow)
(arXiv:2607.01642). Port by RealRebelAI. Works with GGUF / NF4 / FP8 / safetensors
loaders — anything that outputs a normal MODEL. No extra dependencies.

# Examples
- Krea-2 (1024)
<img width="1024" height="1024" alt="output_00046_" src="https://github.com/user-attachments/assets/c7a20973-d538-400d-85bd-40ccc90ec0f1" />
<img width="1024" height="1024" alt="output_00045_" src="https://github.com/user-attachments/assets/de591deb-dbdb-4255-a7f1-9b4ef7018180" />
<img width="1024" height="1024" alt="output_00044_" src="https://github.com/user-attachments/assets/dc07eba3-0a6c-467f-9583-6d57667e732b" />
<img width="1024" height="1024" alt="output_00043_" src="https://github.com/user-attachments/assets/76c2c693-2628-4d52-8794-cd5d76774e18" />
<img width="1024" height="1024" alt="output_00042_" src="https://github.com/user-attachments/assets/ced8d9db-750e-419e-8400-c61305774f7d" />
<img width="1024" height="1024" alt="output_00041_" src="https://github.com/user-attachments/assets/7a22909f-63c8-48ed-aea8-d6866d11b916" />
<img width="1024" height="1024" alt="output_00040_" src="https://github.com/user-attachments/assets/0878367d-560f-47b0-92a3-d5fcbcb1552a" />
<img width="1024" height="1024" alt="output_00039_" src="https://github.com/user-attachments/assets/f527834e-b225-476e-b14d-e080a2749d7c" />
<img width="1024" height="1024" alt="output_00038_" src="https://github.com/user-attachments/assets/4b143ad3-ebb5-47f0-afc9-aee7dd3987f6" />
<img width="1024" height="1024" alt="output_00037_" src="https://github.com/user-attachments/assets/629876aa-7468-4399-9368-e51242731580" />
<img width="1024" height="1024" alt="output_00036_" src="https://github.com/user-attachments/assets/3d74bec9-d080-43f5-9dbe-2c30de93dca6" />
<img width="1024" height="1024" alt="output_00035_" src="https://github.com/user-attachments/assets/65a2d4ee-aed8-4d2f-8300-71c7ffef73c2" />
<img width="1024" height="1024" alt="output_00034_" src="https://github.com/user-attachments/assets/24e4f177-633e-4403-9b49-cce29af08037" />
<img width="1024" height="1024" alt="output_00033_" src="https://github.com/user-attachments/assets/c762889d-fb2f-4440-b7d7-267669ba256b" />
<img width="1024" height="1024" alt="output_00032_" src="https://github.com/user-attachments/assets/9c104f0a-acef-447c-af9a-837bb41be633" />
<img width="1024" height="1024" alt="output_00031_" src="https://github.com/user-attachments/assets/0810e7e6-fde4-46db-959b-bdf8aca4c430" />
<img width="1024" height="1024" alt="output_00030_" src="https://github.com/user-attachments/assets/7210a44a-c743-4003-82fa-28e0469bd5fc" />
<img width="1024" height="1024" alt="output_00029_" src="https://github.com/user-attachments/assets/45d1bde5-c3a3-4ae4-8efc-bafbbbfcc025" />
<img width="1024" height="1024" alt="output_00047_" src="https://github.com/user-attachments/assets/585719aa-06fb-4cd0-bd60-97b67eabb4f0" />




- Krea-2 (2048)
<img width="2048" height="2048" alt="output_00066_" src="https://github.com/user-attachments/assets/67ae1d77-c726-4d0c-b66d-2f4d733d145a" />
<img width="2048" height="2048" alt="output_00065_" src="https://github.com/user-attachments/assets/c2e96932-111e-4d1b-b203-579f2e0ee186" />
<img width="2048" height="2048" alt="output_00064_" src="https://github.com/user-attachments/assets/40b0ba0f-c3eb-4a99-bc0d-70b0cb712746" />
<img width="2048" height="2048" alt="output_00063_" src="https://github.com/user-attachments/assets/eda14123-7dc6-4d55-aa2e-2ce89697cd8d" />
<img width="2048" height="2048" alt="output_00062_" src="https://github.com/user-attachments/assets/9960ef93-708a-44fb-a5a0-3d7de5c38a5c" />
<img width="2048" height="2048" alt="output_00061_" src="https://github.com/user-attachments/assets/8100568f-78be-453c-bed8-c0104b9b65c2" />
<img width="2048" height="2048" alt="output_00060_" src="https://github.com/user-attachments/assets/3ac52328-9f33-4d02-be9e-3b4fc441945e" />
<img width="2048" height="2048" alt="output_00059_" src="https://github.com/user-attachments/assets/73a9a5c5-a37e-46df-819e-c2920add0fef" />
<img width="2048" height="2048" alt="output_00072_" src="https://github.com/user-attachments/assets/9dd459e6-44f8-4e5d-84c8-e72712fc00c6" />
<img width="2048" height="2048" alt="output_00071_" src="https://github.com/user-attachments/assets/cdbf8abc-0159-436d-bf97-53a3ee087d32" />
<img width="2048" height="2048" alt="output_00070_" src="https://github.com/user-attachments/assets/cd5dc6d7-1619-4b9b-b457-218878914012" />
<img width="2048" height="2048" alt="output_00069_" src="https://github.com/user-attachments/assets/1abeedeb-df5c-45bd-b662-accf4b399b6b" />
<img width="2048" height="2048" alt="output_00068_" src="https://github.com/user-attachments/assets/8ccbe2e2-da07-43d7-ad2e-f59792e2aea6" />
<img width="2048" height="2048" alt="output_00067_" src="https://github.com/user-attachments/assets/c7a176d4-b2c2-43b9-ae30-bd98fd55efda" />




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
