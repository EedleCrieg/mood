import sys
import os
import torch
from diffusers import StableDiffusionPipeline

# Create a directory for generated images if it doesn't exist
GENERATED_FOLDER = 'static/generated'
if not os.path.exists(GENERATED_FOLDER):
    os.makedirs(GENERATED_FOLDER)

# This generates a series of 5 images
def generate_images(prompt):
    # Set device for Stable Diffusion
    device = "mps" if torch.backends.mps.is_available() else "cpu"

    # Load the Stable Diffusion model
    model_id = "CompVis/stable-diffusion-v1-4"  # Use the appropriate model ID
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32).to(device)

    # Generate images from the prompt
    for i in range(5):  # Generate 5 images
        with torch.no_grad():
            image = pipe(prompt, num_inference_steps=20, guidance_scale=7.5).images[0]

        # Save the generated image
        image_path = os.path.join(GENERATED_FOLDER, f"generated_image_{i + 1}.png")
        image.save(image_path)
        print(f"Image generated and saved as '{image_path}'")

if __name__ == '__main__':
    import sys
    prompt = " ".join(sys.argv[1:])  # Join all command-line arguments as the prompt
    generate_images(prompt)