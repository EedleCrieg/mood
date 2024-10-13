const imageUpload = document.getElementById('imageUpload');
const imageGallery = document.getElementById('imageGallery');
const descriptionColumn = document.getElementById('descriptionColumn');
const generateButton = document.getElementById('generateButton');
const remixButton = document.getElementById('remixButton');
const remixedParagraph = document.getElementById('remixedParagraph');
const counter = document.getElementById('counter');
const generateImagesButton = document.getElementById('generateImagesButton');
let uploadedImages = [];

// Handle image upload and display the selected images
imageUpload.onchange = () => {
    imageGallery.innerHTML = ''; // Clear previous images
    uploadedImages = Array.from(imageUpload.files); // Store selected images

    counter.innerText = `${uploadedImages.length}/5 images uploaded`;

    uploadedImages.forEach((imgFile, index) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            const div = document.createElement('div');
            const img = document.createElement('img');
            const label = document.createElement('div');

            img.src = e.target.result; // Show the image
            label.textContent = `Image ${index + 1}`;

            div.appendChild(img);
            div.appendChild(label);
            imageGallery.appendChild(div);
        };
        reader.readAsDataURL(imgFile);
    });

    if (uploadedImages.length > 0) {
        generateButton.classList.add('active');
        generateButton.style.cursor = 'pointer';
        generateButton.disabled = false;
    } else {
        generateButton.classList.remove('active');
        generateButton.style.cursor = 'not-allowed';
        generateButton.disabled = true;
    }
};

// Handle description generation when the button is pressed
generateButton.onclick = async () => {
    if (!generateButton.classList.contains('active')) {
        alert('Please upload at least one image before generating descriptions.');
        return;
    }

    const formData = new FormData();
    uploadedImages.forEach((image) => {
        formData.append('images', image);
    });

    const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
    });

    const result = await response.json();
    displayDescriptions(result.descriptions);
};

// Display the generated descriptions in the right column
function displayDescriptions(descriptions) {
    descriptionColumn.innerHTML = ''; // Clear previous descriptions
    descriptions.forEach(({ description }, index) => {
        const div = document.createElement('div');
        const label = document.createElement('label');
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.name = `description-${index}`;
        checkbox.value = description;
        label.textContent = `Description for Image ${index + 1}: ${description}`;
        
        div.classList.add('checkbox-description');
        div.appendChild(checkbox);
        div.appendChild(label);
        descriptionColumn.appendChild(div);
    });
}

// Remix the selected descriptions and display them as a paragraph
remixButton.onclick = () => {
    const selectedDescriptions = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
        .map(checkbox => checkbox.value);

    if (selectedDescriptions.length === 0) {
        alert("Please select at least one description.");
        return;
    }

    // Shuffle the selected descriptions to create a remixed paragraph
    const remixed = shuffleArray(selectedDescriptions).join(' ');

    // Display the remixed paragraph
    remixedParagraph.innerHTML = `<p>${remixed}</p>`;
};

// Function to shuffle the array of selected descriptions
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]]; // Swap elements
    }
    return array;
}

// Generate images and display them in the gallery
generateImagesButton.onclick = async () => {
    const remixedDescription = remixedParagraph.innerText;
    if (!remixedDescription) {
        alert("Please generate a remixed description first.");
        return;
    }

    const response = await fetch('/generate-images', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: remixedDescription }),
    });

    const result = await response.json();
    if (result.success) {
        loadGeneratedImages(); // Load the generated images after creation
    } else {
        alert("Error generating images: " + result.error);
    }
};

// Function to load generated images from the server
async function loadGeneratedImages() {
    const response = await fetch('/generated-images');
    const images = await response.json();
    generatedImagesGallery.innerHTML = ''; // Clear previous images

    images.forEach(image => {
        const imgElement = document.createElement('img');
        imgElement.src = `static/generated/${image}`; // Update path to generated images
        generatedImagesGallery.appendChild(imgElement);
    });
}