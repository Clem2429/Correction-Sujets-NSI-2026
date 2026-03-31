const btn = document.querySelector('.lien-top');

window.addEventListener('scroll', () => {
    if (window.scrollY > 200) {
        btn.classList.add('visible');
    } else {
        btn.classList.remove('visible');
    }
});

btn.addEventListener('click', e => {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: 'smooth' });
});