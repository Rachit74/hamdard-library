document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('navbar-toggle');
    const navbarLinks = document.querySelector('.navbar-links');

    toggleButton.addEventListener('click', function() {
        navbarLinks.classList.toggle('show');
    });
});

function closeFlashMessage(button) {
    // Find the parent flash message and fade it out
    var flashMessage = button.parentElement;
    flashMessage.style.opacity = 0;
    setTimeout(function() {
        flashMessage.remove();
    }, 500); // Match the CSS animation duration
};
