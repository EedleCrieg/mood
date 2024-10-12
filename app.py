from flask import Flask, request, render_template
import os
import sys

# Add the CLIP repository to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'CLIP-main'))

import torch
from PIL import Image
import clip  # Now this should work

app = Flask(__name__)

# Load CLIP model and processor
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)  # Load the CLIP model

# Set the upload folder
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'images' not in request.files:
        return "No images uploaded", 400

    images = request.files.getlist('images')
    descriptions = []

    for img in images:
        if img:
            img_path = os.path.join(UPLOAD_FOLDER, img.filename)
            img.save(img_path)

            # Load the image
            image = preprocess(Image.open(img_path)).unsqueeze(0).to(device)

            # Generate description
            text_inputs = clip.tokenize(["a photo of a "]).to(device)
            with torch.no_grad():
                image_features = model.encode_image(image)
                text_features = model.encode_text(text_inputs)

                logits_per_image = (image_features @ text_features.T).softmax(dim=-1)
                description = f"This image is likely to be a photo of something with a score of {logits_per_image[0][0].item():.2f}."

            descriptions.append({"filename": img.filename, "description": description})  # Include filename

    return {"descriptions": descriptions}

if __name__ == '__main__':
    app.run(debug=True)