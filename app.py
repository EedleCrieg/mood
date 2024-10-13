from flask import Flask, request, jsonify, render_template
import os
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

app = Flask(__name__)

# Load BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Set the folder for uploaded images
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    descriptions = []
    if 'images' not in request.files:
        return "No images uploaded", 400

    images = request.files.getlist('images')

    for img in images:
        if img:
            img_path = os.path.join(UPLOAD_FOLDER, img.filename)
            img.save(img_path)

            # Load and preprocess the image
            image = Image.open(img_path).convert("RGB")
            inputs = processor(images=image, return_tensors="pt")
            
            # Generate a longer description with increased max_length and beam search
            out = model.generate(**inputs, 
                                max_length=200,          # Increase the max length of the description
                                min_length=100,          # Ensure the output is at least 100 tokens
                                num_beams=5,             # Use beam search to improve description quality
                                temperature=1.2,         # Control randomness for more coherent output
                                early_stopping=False,    # Prevent early stopping
                                no_repeat_ngram_size=2,  # Avoid repeating bigrams
                                repetition_penalty=1.2   # Penalize repetitions for diverse output
            )
            # Generate description
            description = processor.decode(out[0], skip_special_tokens=True)
            descriptions.append({"filename": img.filename, "description": description})

    return jsonify({"descriptions": descriptions})

if __name__ == '__main__':
    app.run(debug=True)