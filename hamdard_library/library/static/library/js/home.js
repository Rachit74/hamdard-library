
// file approval info button
const infoButton = document.querySelector('.info-btn');

const modalCloseBtn = document.querySelector('.btn-modal-close');

const infoModal = document.querySelector('.info-modal');

const openInfoModal = function() {
    infoModal.classList.remove('hidden');
}

const closeInfoModal = function() {
    infoModal.classList.add('hidden');
}

infoButton.addEventListener('click', openInfoModal);

modalCloseBtn.addEventListener('click', closeInfoModal);

document.querySelector('.info-modal-overlay').addEventListener('click', closeInfoModal);
