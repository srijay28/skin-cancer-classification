let model;
const labels = ["Benign", "Malignant"];

// Function to show loading spinner
function showLoading() {
  const predictionResult = document.getElementById("prediction-result");
  predictionResult.innerHTML = `<div class="loading-spinner"></div><p>Analyzing...</p>`;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Function to hide loading spinner
// function hideLoading() {
//   const predictionResult = document.getElementById("prediction-result");
//   predictionResult.innerHTML = ""; // Clear the content after analysis
// }

// Load the TensorFlow.js model using the model URL from the HTML
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
    showLoading();
    await sleep(1000);
    if (imageElement && imageElement.complete) {
      predict();
    } else {
      imageElement.onload = predict;
    }
  } catch (error) {
    console.error("Error loading model:", error);
  }
}

// Function to perform prediction
async function predict() {
  if (!model) {
    console.error("Model not loaded yet!");
    return;
  }

  const imageElement = document.getElementById("uploaded-image");
  if (
    !imageElement ||
    !imageElement.complete ||
    imageElement.naturalWidth === 0
  ) {
    console.error("Image failed to load or is broken.");
    return;
  }

  try {
    // Show loading spinner

    const tensor = tf.browser
      .fromPixels(imageElement)
      .resizeNearestNeighbor([128, 128])
      .toFloat()
      .div(tf.scalar(255.0))
      .expandDims();

    const predictions = await model.predict(tensor).data();
    const maxIndex = predictions.indexOf(Math.max(...predictions));
    const score = Math.max(...predictions).toFixed(5);

    document.getElementById(
      "prediction-result"
    ).textContent = `Prediction: ${labels[maxIndex]} with confidence: ${score}`;

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
