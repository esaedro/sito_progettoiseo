document.addEventListener('DOMContentLoaded', function() {
// Lightbox immagini eventi con Bootstrap Modal
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.event-image').forEach(function(img) {
        img.style.cursor = 'zoom-in';
        img.addEventListener('click', function(e) {
            e.preventDefault();
            var modal = document.getElementById('eventImageModal');
            var modalImg = document.getElementById('eventImageModalImg');
            var modalTitle = document.getElementById('eventImageModalLabel');
            if (modal && modalImg && modalTitle) {
                modalImg.src = img.src;
                modalImg.alt = img.alt;
                modalTitle.textContent = img.alt || '';
                // Usa Bootstrap Modal
                var bsModal = bootstrap.Modal.getOrCreateInstance(modal);
                bsModal.show();
            }
        });
    });
});
