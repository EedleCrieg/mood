import torch
from diffusers import StableDiffusionPipeline

# Set device for Stable Diffusion
device = "mps" if torch.backends.mps.is_available() else "cpu"

# Load the Stable Diffusion model
model_id = "CompVis/stable-diffusion-v1-4"  # Use the appropriate model ID
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32).to(device)

# Generate an image from a prompt
prompt = "A fantasy landscape with mountains and a river"
with torch.no_grad():
    image = pipe(prompt, num_inference_steps=50, guidance_scale=7.5).images[0]

# Save the generated image
image.save("generated_image.png")
print("Image generated and saved as 'generated_image.png'")