document.addEventListener("DOMContentLoaded", function() {
    var lazyImage = document.getElementById('objectImage');
    if (lazyImage.dataset.src) {
        lazyImage.src = lazyImage.dataset.src;
    }
});