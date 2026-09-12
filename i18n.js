/* Перемикання мов для статичного сайту ГО «Життєдайна».
   Переклади лежать у i18n/uk.js та i18n/en.js як window.I18N.<код мови>.
   Розмітка позначена атрибутами:
     data-i18n="ключ"                 — текст елемента
     data-i18n-attr="alt:ключ"        — атрибут елемента (можна кілька через ;)
   Вибір мови: ?lang=en у посиланні → localStorage → мова браузера → uk. */
(function () {
  var DEFAULT = 'uk';
  var SUPPORTED = ['uk', 'en'];
  var STORAGE_KEY = 'zd-lang';

  function pickLang() {
    var fromUrl = new URLSearchParams(location.search).get('lang');
    if (SUPPORTED.indexOf(fromUrl) > -1) return fromUrl;
    try {
      var saved = localStorage.getItem(STORAGE_KEY);
      if (SUPPORTED.indexOf(saved) > -1) return saved;
    } catch (e) {}
    var nav = (navigator.language || '').slice(0, 2).toLowerCase();
    return SUPPORTED.indexOf(nav) > -1 ? nav : DEFAULT;
  }

  function apply(lang) {
    var dict = (window.I18N || {})[lang];
    if (!dict) return;

    document.documentElement.lang = lang;

    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var value = dict[el.getAttribute('data-i18n')];
      if (typeof value === 'string') el.textContent = value;
    });

    document.querySelectorAll('[data-i18n-attr]').forEach(function (el) {
      el.getAttribute('data-i18n-attr').split(';').forEach(function (pair) {
        var parts = pair.split(':');
        var attr = (parts[0] || '').trim();
        var value = dict[(parts[1] || '').trim()];
        if (attr && typeof value === 'string') el.setAttribute(attr, value);
      });
    });

    if (dict['meta.title']) document.title = dict['meta.title'];
    var desc = document.querySelector('meta[name="description"]');
    if (desc && dict['meta.description']) desc.setAttribute('content', dict['meta.description']);

    document.querySelectorAll('[data-lang]').forEach(function (btn) {
      btn.setAttribute('aria-pressed', String(btn.getAttribute('data-lang') === lang));
    });

    try { localStorage.setItem(STORAGE_KEY, lang); } catch (e) {}
  }

  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-lang]');
    if (!btn) return;
    e.preventDefault();
    apply(btn.getAttribute('data-lang'));
  });

  apply(pickLang());
})();
