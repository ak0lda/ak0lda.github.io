/**
 * Единая дизайн-система сайта (раньше в каждой странице была своя копия).
 * @type {import('tailwindcss').Config}
 */
module.exports = {
  content: ['./*.html', './*/index.html', './en/*/index.html', './assets/js/**/*.js'],
  theme: {
    // Палитра Tailwind по умолчанию отключена: доступны только цвета ниже.
    colors: {
      transparent: 'transparent',
      current: 'currentColor',
      background: '#141313',
      surface: '#141313',
      'surface-container-lowest': '#0f0e0e',
      'surface-container-low': '#1c1b1b',
      'surface-container': '#201f1f',
      'surface-container-high': '#2b2a2a',
      'surface-variant': '#363434',
      'surface-bright': '#3a3939',
      'on-background': '#e6e1e1',
      'on-surface': '#e6e1e1',
      'on-surface-variant': '#e3bfb3',
      'electric-orange': '#ff5f1f',
      'stroke-soft': '#3a3939',
      'status-online': '#34d399',
    },
    // Шкала размеров Tailwind по умолчанию отключена: доступны только размеры ниже.
    fontSize: {
      'body-lg': ['18px', { lineHeight: '1.6', letterSpacing: '0.01em', fontWeight: '400' }],
      'body-md': ['16px', { lineHeight: '1.5', fontWeight: '400' }],
      'headline-lg': ['48px', { lineHeight: '1.1', letterSpacing: '0.01em', fontWeight: '600' }],
      'headline-md': ['24px', { lineHeight: '1.3', fontWeight: '500' }],
      'headline-lg-mobile': ['32px', { lineHeight: '1.1', letterSpacing: '0.01em', fontWeight: '600' }],
      metadata: ['13px', { lineHeight: '1.0', letterSpacing: '0.05em', fontWeight: '500' }],
      display: ['80px', { lineHeight: '1.0', letterSpacing: '0.02em', fontWeight: '700' }],
      index: ['11px', { lineHeight: '1.0', letterSpacing: '0.1em', fontWeight: '700' }],
      // Плотная шкала для карточек кейсов (страница Work)
      'title-lg': ['30px', { lineHeight: '36px' }],
      'body-sm': ['14px', { lineHeight: '20px' }],
      caption: ['12px', { lineHeight: '16px' }],
      micro: ['11px', { lineHeight: '16px' }],
      'headline-sm': '26px',
      nano: '10px',
      // Иконки Material Symbols
      'icon-sm': ['14px', { lineHeight: '20px' }],
      'icon-md': ['16px', { lineHeight: '24px' }],
      'icon-lg': ['18px', { lineHeight: '28px' }],
      'icon-xl': ['20px', { lineHeight: '28px' }],
      'icon-2xl': ['24px', { lineHeight: '32px' }],
      // Крупные декоративные иконки и глифы
      'glyph-sm': '64px',
      'glyph-lg': '120px',
    },
    extend: {
      borderRadius: {
        DEFAULT: '0.25rem',
        lg: '0.5rem',
        xl: '0.75rem',
      },
      spacing: {
        'stack-xs': '0.25rem',
        'stack-sm': '1rem',
        'stack-md': '2.5rem',
        'stack-lg': '5rem',
        'margin-mobile': '1.25rem',
        'margin-desktop': '3rem',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
        headline: ['Manrope', 'system-ui', 'sans-serif'],
        display: ['Manrope', 'system-ui', 'sans-serif'],
        'body-lg': ['Inter', 'system-ui', 'sans-serif'],
        'body-md': ['Inter', 'system-ui', 'sans-serif'],
        'headline-lg': ['Manrope', 'system-ui', 'sans-serif'],
        'headline-md': ['Manrope', 'system-ui', 'sans-serif'],
        'headline-lg-mobile': ['Manrope', 'system-ui', 'sans-serif'],
        metadata: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
        index: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
      },
    },
  },
  plugins: [],
};
