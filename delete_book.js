document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('deleteForm');
    const input = document.getElementById('confirm');
    if (form && input) {
        const actualId = form.action.split('/').filter(Boolean).pop();
        form.addEventListener('submit', function (e) {
            if (input.value.trim() !== actualId) {
                e.preventDefault();
                alert("Incorrect book ID. Deletion cancelled.");
            }
        });
    }
});