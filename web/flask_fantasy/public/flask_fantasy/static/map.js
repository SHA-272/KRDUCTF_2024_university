document.addEventListener('DOMContentLoaded', (event) => {
    const points = document.querySelectorAll('.point');
    points.forEach((point) => {
        point.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            window.location.href = '/object/id=' + id;
        });
    });
});
