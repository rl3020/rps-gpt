// Close button logic (only when showing errors)
// Error close button
const close = document.getElementById("close-button");
// Listen to click event
close.addEventListener("click", (e) => {
  e.preventDefault();
  console.log("close clicked");
  const errorHeader = document.getElementById("error-header");
  errorHeader.style.display = "none";
});
