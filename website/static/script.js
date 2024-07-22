document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('navbar-toggle');
    const navbarLinks = document.querySelector('.navbar-links');

    toggleButton.addEventListener('click', function() {
        navbarLinks.classList.toggle('show');
    });
});

function closeFlashMessage() {
    var flashMessage = document.getElementById('flashMessage');
    flashMessage.style.display = 'none';
}