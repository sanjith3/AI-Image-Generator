from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
import torch

# Optimized settings for RTX 3090
torch.backends.cudnn.benchmark = True
torch.backends.cuda.matmul.allow_tf32 = True

# Load model with FP16 precision
model = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    torch_dtype=torch.float16
).to("cuda")

# Use optimized scheduler for better quality & speed
model.scheduler = DPMSolverMultistepScheduler.from_config(model.scheduler.config)

# Enable VRAM optimizations
model.enable_attention_slicing()
model.enable_vae_slicing()
model.to(memory_format=torch.channels_last)

# Use xFormers if available
try:
    model.enable_xformers_memory_efficient_attention()
except:
    print("xFormers not available, continuing without it.")

# Disable safety checker (optional for performance)
model.safety_checker = None

def generate_image(prompt, output_path):
    """Generates a high-quality image optimized for RTX 3090"""
    with torch.inference_mode():
        with torch.cuda.amp.autocast():
            image = model(
                prompt,
                num_inference_steps=150,  # Increased steps for better refinement
                guidance_scale=5.7  # Balanced natural realism
            ).images[0]

    image.save(output_path)
    return output_path
