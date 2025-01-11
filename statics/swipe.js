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
  displayDate.setDate(displayDate.getDate() + diff);
  updateImageDetails();
}
