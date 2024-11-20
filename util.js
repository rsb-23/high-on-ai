// Get today's date in yyyy-mm/dd format
const today = new Date();
const formattedDate = today.toISOString().slice(0, 10);
const nestedDate = `${formattedDate.slice(0, 7)}/${formattedDate.slice(8, 10)}`;
console.log(formattedDate, nestedDate);

// Configure display elements
fetch("iotd/data.json")
  .then((response) => response.json())
  .then((data) => {
    let imageKey = "default";
    if (data[nestedDate] != undefined) {
      imageKey = nestedDate;
    }
    const description = data[imageKey]["title"] || "no description found";
    document.getElementById("description").textContent = description;
    // Set image source
    const imagePath = `iotd/${imageKey}.png`;
    document.getElementById("image").src = imagePath;
  })
  .catch((error) => {
    console.error("Error loading description:", error);
    document.getElementById("description").textContent = "Failed to load description.";
  });

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

// Update the timer every 2s
setInterval(updateTimer, 2000);
updateTimer();
