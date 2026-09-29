(function () {
  'use strict';

  var CONTACTS = {
    github: 'https://github.com/ak0lda',
    telegram: 'https://t.me/ak0lda_contact_bot?start=site',
    linkedin: 'https://www.linkedin.com/in/%D0%B8%D0%BB%D1%8C%D1%8F-%D1%82%D0%B8%D1%86%D0%BA%D0%B8%D0%B9-69297043a/',
    email: 'ilya.tick.dev@gmail.com' 
  };

  document.querySelectorAll('[data-contact]').forEach(function (link) {
    var key = link.getAttribute('data-contact');
    var value = CONTACTS[key];
    if (!value) return;
    link.setAttribute('href', key === 'email' ? 'mailto:' + value : value);
  });
})();
