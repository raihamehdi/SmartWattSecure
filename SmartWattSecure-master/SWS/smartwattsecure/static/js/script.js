// Function to open the SignUp modal
function openSignupModal(event) {
  event.preventDefault();  // Prevent the default link behavior
  document.getElementById('signupModal').classList.add('show');  // Show the modal
}

// Function to open the Login modal
function openLoginModal(event) {
  event.preventDefault();  // Prevent the default link behavior
  document.getElementById('loginModal').classList.add('show');  // Show the modal
}

// Function to close the modal
function closeModal() {
  document.getElementById('signupModal').classList.remove('show');
  document.getElementById('loginModal').classList.remove('show');
}

function togglePassword() {
  const passwordField = document.getElementById("password");
  const eyeIcon = document.getElementById("toggle-password");

  if (passwordField.type === "password") {
    passwordField.type = "text";
    eyeIcon.textContent = "🙈";  // Change to "hide" eye icon
  } else {
    passwordField.type = "password";
    eyeIcon.textContent = "👁️";  // Change to "show" eye icon
  }
}