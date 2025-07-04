/* Fix per immagini evento che non si caricano o sono rotte */
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.event-image').forEach(function(img) {
        // fallback se l'immagine è già rotta al caricamento
        if (!img.complete || img.naturalWidth === 0) {
            setPlaceholder(img);
        }
        img.onerror = function() {
            setPlaceholder(this);
        };
    });
    function setPlaceholder(img) {
        // Evita duplicati
        if (img.dataset.placeholderSet) return;
        img.style.display = 'none';
        let placeholder = document.createElement('div');
        placeholder.className = 'card-img-top event-image-placeholder d-flex align-items-center justify-content-center bg-light';
        placeholder.innerHTML = '<i class="fas fa-calendar-alt text-muted fa-3x"></i>';
        img.parentNode.insertBefore(placeholder, img.nextSibling);
        img.dataset.placeholderSet = '1';
    }
});
