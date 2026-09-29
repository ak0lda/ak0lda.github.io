// Общий скрипт сайта: мобильное меню, часы и язык страницы 404.
(function () {
  'use strict';

  var isEn = document.documentElement.lang === 'en';

  // --- Мобильное меню ---
  var toggle = document.querySelector('[data-menu-toggle]');
  var menu = document.getElementById('mobile-nav');

  if (toggle && menu) {
    var icon = toggle.querySelector('.material-symbols-outlined');

    var setOpen = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open
        ? (isEn ? 'Close menu' : 'Закрыть меню')
        : (isEn ? 'Open menu' : 'Открыть меню'));
      menu.hidden = !open;
      if (icon) icon.textContent = open ? 'close' : 'menu';
    };

    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && !menu.hidden) {
        setOpen(false);
        toggle.focus();
      }
    });

    // При переходе на десктопную ширину меню закрывается
    window.matchMedia('(min-width: 1280px)').addEventListener('change', function (event) {
      if (event.matches) setOpen(false);
    });
  }

  // --- Страница 404: одна на весь сайт, язык берём из адреса ---
  if (document.body.hasAttribute('data-404') && /\/en(\/|$)/.test(location.pathname)) {
    document.documentElement.lang = 'en';
    document.title = '404 — Page Not Found | Ilya Vitalievich';
    document.querySelectorAll('[data-en]').forEach(function (el) {
      el.textContent = el.getAttribute('data-en');
    });
    document.querySelectorAll('[data-en-href]').forEach(function (el) {
      el.setAttribute('href', el.getAttribute('data-en-href'));
    });
  }

  // --- Время на странице 404 ---
  var timeEl = document.getElementById('sys-time');
  if (timeEl) {
    var updateTime = function () {
      timeEl.textContent = new Date().toISOString().slice(11, 19);
    };
    updateTime();
    setInterval(updateTime, 1000);
  }
})();
