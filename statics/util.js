const today = new Date();
let displayDate = new Date();
let imageData;

imageDiv = document.getElementById("image");
descDiv = document.getElementById("description");

// Load the JSON data
async function loadImageData() {
  console.info("loading json...");
  try {
    const response = await fetch("iotd/data.json");
    if (!response.ok) {
      throw new Error("Failed to load image data");
    }
    const dataJson = await response.json();
    imageData = dataJson;
  } catch (error) {
    console.error("Error loading image data:", error);
    descDiv.innerHTML = `<div class="error-message">Error loading image descriptions</div>`;
  }
}

// Get current date in yyyy-mm/dd format
function getNestedDate(currentDate) {
  const formattedDate = currentDate.toISOString().slice(0, 10);
  const nestedDate = `${formattedDate.slice(0, 7)}/${formattedDate.slice(8, 10)}`;
  console.log(formattedDate, nestedDate);
  return nestedDate;
}

function updateImageDetails() {
  console.info("loading details for --", displayDate.toISOString());
  if (displayDate > today) {
    displayDate.setDate(today.getDate());
    return;
  }
  const nestedDate = getNestedDate(displayDate);
  let imageKey = "default";
  if (imageData[nestedDate] != undefined) {
    imageKey = nestedDate;
  }
  const description = imageData[imageKey]["title"] || "no description found";
  descDiv.textContent = description;

  // Set image source with fallback
  imageDiv.src = `iotd/${imageKey}.webp`;
  imageDiv.onerror = function () {
    if (this.src.includes('.webp')) {
      this.error = null;
      this.src = `iotd/${imageKey}.png`; // fallback
    }
  };

  // preload yesterday's image
  imageDiv.onload = function () {
    const preloadDate = new Date(displayDate);
    preloadDate.setDate(displayDate.getDate() - 1);
    // preloadImage(preloadDate);
  };
}

function preloadImage(imageDate) {
  const imageKey = getNestedDate(imageDate);
  const imagePath = `iotd/${imageKey}.webp`;
  const img = new Image();
  img.src = imagePath; // Browser starts downloading the image
  img.onerror = function () {
    img.src = "iotd/default.webp";
  };
}

function timePad(x) {
  return String(Math.floor(x)).padStart(2, "0");
}

function updateTimer() {
  const now = new Date();
  now.setHours(now.getUTCHours());
  now.setMinutes(now.getUTCMinutes());
  const nextMidnight = new Date(now);
  nextMidnight.setHours(24, 0, 0, 0); // Set time to midnight of the next day

  const timeRemaining = nextMidnight - now;

  const hours = timePad((timeRemaining / (1000 * 60 * 60)) % 24);
  const minutes = timePad((timeRemaining / (1000 * 60)) % 60);
  const seconds = timePad((timeRemaining / 1000) % 60);

  document.getElementById("timer").textContent = `${hours}:${minutes}:${seconds}`;
}

loadImageData().then(() => {
  updateImageDetails();
});

// Update the timer every 2s
setInterval(updateTimer, 2000);
updateTimer();
