// let model;
// const labels = ["Benign", "Malignant"];

// // Load the TensorFlow.js model using the model URL from the HTML
// async function loadModel() {
//   const modelUrl = document.body.getAttribute("data-model-url");
//   if (!modelUrl) {
//     console.error("Model URL not found.");
//     return;
//   }

//   try {
//     model = await tf.loadLayersModel(modelUrl);
//     console.log("Model loaded successfully!");
//   } catch (error) {
//     console.error("Error loading model:", error);
//   }
// }

// // Function to perform prediction
// async function predict() {
//   if (!model) {
//     console.error("Model not loaded yet!");
//     return;
//   }

//   const imageElement = document.getElementById("uploaded-image");

//   // Verify if the image element exists and is fully loaded
//   if (
//     !imageElement ||
//     !imageElement.complete ||
//     imageElement.naturalWidth === 0
//   ) {
//     console.error("Image failed to load or is broken.");
//     return;
//   }

//   try {
//     const tensor = tf.browser
//       .fromPixels(imageElement)
//       .resizeNearestNeighbor([128, 128])
//       .toFloat()
//       .div(tf.scalar(255.0))
//       .expandDims();
//     console.log("after tensor thing");
//     const predictions = await model.predict(tensor).data();
//     const maxIndex = predictions.indexOf(Math.max(...predictions));
//     const score = Math.max(...predictions).toFixed(2);

//     document.getElementById(
//       "prediction-result"
//     ).textContent = `Prediction: ${labels[maxIndex]} with confidence: ${score}`;
//     console.log("after prediction");
//   } catch (error) {
//     console.error("Error during prediction:", error);
//   }
// }

// // Wait for the page to load fully before running scripts
// window.onload = function () {
//   loadModel();

//   const imageElement = document.getElementById("uploaded-image");
//   console.log("image url obtained", imageElement);
//   if (imageElement) {
//     console.log("calling predict");
//     imageElement.onload = predict; // Run predict when image loads
//   } else {
//     console.error("Uploaded image element not found.");
//   }
// };
let model;
const labels = ["Benign", "Malignant"];

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
    // After model is loaded, run the prediction if the image is already loaded
    const imageElement = document.getElementById("uploaded-image");
    if (imageElement && imageElement.complete) {
      predict(); // Call predict if image is already loaded
    } else {
      // Otherwise, wait for image to load before calling predict
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

  // Verify if the image element exists and is fully loaded
  if (
    !imageElement ||
    !imageElement.complete ||
    imageElement.naturalWidth === 0
  ) {
    console.error("Image failed to load or is broken.");
    return;
  }

  try {
    const tensor = tf.browser
      .fromPixels(imageElement)
      .resizeNearestNeighbor([128, 128]) // Resize to model's input shape
      .toFloat()
      .div(tf.scalar(255.0)) // Normalize
      .expandDims(); // Add batch dimension
    console.log("after tensor thing");
    const predictions = await model.predict(tensor).data();
    console.log(predictions);
    const maxIndex = predictions.indexOf(Math.max(...predictions));
    const score = Math.max(...predictions).toFixed(5);

    document.getElementById(
      "prediction-result"
    ).textContent = `Prediction: ${labels[maxIndex]} with confidence: ${score}`;
    console.log("after prediction");
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

// Wait for the page to load fully before running scripts
window.onload = loadModel;
