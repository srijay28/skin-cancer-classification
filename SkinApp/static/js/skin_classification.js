let model;
const labels = ["Benign", "Malignant"];

// Function to show loading spinner
function showLoading() {
  const predictionResult = document.getElementById("prediction-result");
  predictionResult.innerHTML = `<div class="loading-spinner"></div><p class="analyzing">Analyzing...</p>`;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function loadModel() {
  const modelUrl = document.body.getAttribute("data-model-url");
  if (!modelUrl) {
    console.error("Model URL not found.");
    return;
  }

  try {
    model = await tf.loadLayersModel(modelUrl);
    console.log("Model loaded successfully!");

    const imageElement = document.getElementById("uploaded-image");
    if (imageElement && imageElement.src && imageElement.src !== "") {
      imageElement.style.display = "block"; // Show the image container
      if (imageElement.complete) {
        predict();
      } else {
        imageElement.onload = predict;
      }
    }
  } catch (error) {
    console.error("Error loading model:", error);
  }
}

async function predict() {
  const imageElement = document.getElementById("uploaded-image");

  // Hide the image container if there's no valid image source
  if (!imageElement || !imageElement.src || imageElement.naturalWidth === 0) {
    imageElement.style.display = "none";
    console.error("No valid image source.");
    return;
  }

  showLoading();
  await sleep(1000);

  try {
    const tensor = tf.browser
      .fromPixels(imageElement)
      .resizeNearestNeighbor([128, 128])
      .toFloat()
      .div(tf.scalar(255.0))
      .expandDims();

    const predictions = await model.predict(tensor).data();
    const maxIndex = predictions.indexOf(Math.max(...predictions));
    const score = Math.max(...predictions).toFixed(5);

    const predictionResult = document.getElementById("prediction-result");
    predictionResult.innerHTML = `
      <p id="prediction-label"></p>
      <div class="progress-bar-background">
        <div id="progress-bar" class="progress-bar-fill"></div>
      </div>
    `;
    const predictionLabel = document.getElementById("prediction-label");
    const progressBar = document.getElementById("progress-bar");

    predictionLabel.textContent = `${labels[maxIndex]} : ${score}`;
    setTimeout(() => {
      progressBar.style.width = `${(score * 100).toFixed(2)}%`;
    }, 50);

    const imageUrl = imageElement.getAttribute("src");
    if (imageUrl) {
      await fetch(`/delete_image?image_url=${encodeURIComponent(imageUrl)}`, {
        method: "GET",
      });
      console.log("Image deleted from server after prediction.");
    }
  } catch (error) {
    console.error("Error during prediction:", error);
  }
}

window.onload = loadModel;
