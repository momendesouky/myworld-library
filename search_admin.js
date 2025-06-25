document.getElementById('search').addEventListener('input', function () {
    const term = this.value.toLowerCase();
    const cards = document.querySelectorAll('.book-card');

    cards.forEach(card => {
        const id=card.querySelector('.book-id').textContent.toLowerCase();
        const title = card.querySelector('.book-title').textContent.toLowerCase();
        const author = card.querySelector('.book-author').textContent.toLowerCase();
        card.style.display = (title.includes(term) || author.includes(term)|| id.includes(term)) ? '' : 'none';
    });
});