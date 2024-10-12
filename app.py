from flask import Flask, request, render_template
import os
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

app = Flask(__name__)

# Load the BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

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

            # Load and preprocess the image
            image = Image.open(img_path).convert("RGB")

            # Preprocess the image and generate caption
            inputs = processor(images=image, return_tensors="pt")
            out = model.generate(**inputs)
            description = processor.decode(out[0], skip_special_tokens=True)

            descriptions.append({"filename": img.filename, "description": description})

    return {"descriptions": descriptions}

if __name__ == '__main__':
    app.run(debug=True)