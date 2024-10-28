// Store the current scroll position in localStorage before the page reloads
window.addEventListener("beforeunload", function() {
  localStorage.setItem("scrollPosition", window.scrollY);
});

// Restore the scroll position after the page reloads
window.addEventListener("load", function() {
  const scrollPosition = localStorage.getItem("scrollPosition");
  if (scrollPosition) {
    window.scrollTo(0, parseInt(scrollPosition));
    localStorage.removeItem("scrollPosition"); // Remove after using it
  }
});