window.updateLanguageToggles = function updateLanguageToggles(lang) {
  const activeLang = lang === 'jp' ? 'jp' : 'en';

  document.querySelectorAll('.lang-toggle').forEach(button => {
    if (!button.querySelector('.lang-option')) {
      const english = document.createElement('span');
      english.className = 'lang-option';
      english.dataset.lang = 'en';
      english.textContent = 'EN';

      const japanese = document.createElement('span');
      japanese.className = 'lang-option';
      japanese.dataset.lang = 'jp';
      japanese.textContent = 'JP';

      button.replaceChildren(english, japanese);
    }

    button.dataset.activeLang = activeLang;
    button.setAttribute(
      'aria-label',
      activeLang === 'en'
        ? 'English selected. Switch to Japanese'
        : 'Japanese selected. Switch to English'
    );

    button.querySelectorAll('.lang-option').forEach(option => {
      const isActive = option.dataset.lang === activeLang;
      option.classList.toggle('is-active', isActive);
      option.setAttribute('aria-current', isActive ? 'true' : 'false');
    });
  });
};

document.addEventListener('DOMContentLoaded', () => {
  const currentYear = new Date().getFullYear();
  document.querySelectorAll('[data-current-year]').forEach(element => {
    element.textContent = currentYear;
  });

  window.updateLanguageToggles(localStorage.getItem('lang') || 'en');
});
