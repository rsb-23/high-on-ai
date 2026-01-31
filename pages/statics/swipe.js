// Get element reference
const element = document.getElementById("swipe-area");
// Create Hammer instance
const hammer = new Hammer(element);

hammer.on("swipe", function (ev) {
  const direction = ev.direction;
  if (direction === Hammer.DIRECTION_LEFT) {
    triggerUpdate(1);
  } else if (direction === Hammer.DIRECTION_RIGHT) {
    triggerUpdate(-1);
  }
});

hammer.get("swipe").set({ direction: Hammer.DIRECTION_ALL });

// Using keys
document.addEventListener("DOMContentLoaded", () => {
  document.addEventListener("keydown", (event) => {
    // Check for left and right arrow keys
    if (event.key === "ArrowLeft") {
      triggerUpdate(-1);
    } else if (event.key === "ArrowRight") {
      triggerUpdate(1);
    }
  });
});

function triggerUpdate(diff) {
  const direction = diff === 1 ? "left" : "right";

  const swipeArea = document.getElementById("swipe-area");

  // // Add swipe animation
  // swipeArea.classList.add(`swipe-${direction}`);
  // setTimeout(() => {
  //   swipeArea.classList.remove(`swipe-${direction}`);
  // }, 300); // Match the CSS transition duration

  // Adds loading indicator
  swipeArea.classList.add("loading");
  displayDate.setDate(displayDate.getDate() + diff);
  updateImageDetails();
  swipeArea.classList.remove("loading");
}
