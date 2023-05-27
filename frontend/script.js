function toggleDetails() {
    var detailsSection = document.getElementById("details");
    if (detailsSection.style.display === "none") {
      detailsSection.style.display = "block";
    } else {
      detailsSection.style.display = "none";
    }
  }

document.getElementById('recommendation-form').addEventListener('submit', function(event) {
    event.preventDefault();

     // Display success message
  var successMessage = document.createElement("p");
  successMessage.textContent = "Recommendation Submission Successful!";
  successMessage.classList.add("text-success", "success-message");
  document.getElementById("recommendation-form").appendChild(successMessage);

  // Remove success message after 2 seconds
  setTimeout(function() {
    successMessage.remove();
  }, 2000);
});