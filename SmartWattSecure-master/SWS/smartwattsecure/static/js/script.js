document.querySelectorAll('.cancel-button').forEach(button => {
    button.addEventListener('click', () => {
        window.location.href = 'index.html'; // Redirect to the home page or the previous page
    });
});
