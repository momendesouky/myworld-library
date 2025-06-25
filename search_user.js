document.getElementById('searchInput').addEventListener('input', function () {
    const term = this.value.toLowerCase();
    const cards = document.querySelectorAll('.book-card');

    cards.forEach(card => {
        const title = card.querySelector('.book-title').textContent.toLowerCase();
        const author = card.querySelector('.book-author').textContent.toLowerCase();
        const category = card.querySelector('.book-category').textContent.toLowerCase();

        card.style.display = (title.includes(term) || author.includes(term) || category.includes(term)) ? '' : 'none';
    });
});