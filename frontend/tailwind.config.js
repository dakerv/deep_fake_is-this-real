export default {content: [
  './index.html',
  './src/**/*.{js,ts,jsx,tsx}'
],
  theme: {
    extend: {
      colors: {
        paper: '#f7f5ef',
        ivory: '#f2efe7',
        ivorydeep: '#e9e5d9',
        ink: '#17191b',
        graphite: '#33373a',
        gray: {
          soft: '#8a8880',
        },
        rule: '#d5d0c3',
        ruledark: '#3d4348',
        slate: {
          plate: '#59636c',
          deep: '#464f57',
          tint: '#7d868e',
        },
        accent: '#8c3b2e',
      },
      fontFamily: {
        display: ['"Instrument Serif"', 'Georgia', 'serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
      },
      letterSpacing: {
        label: '0.14em',
      },
      maxWidth: {
        spread: '90rem',
      },
    },
  },
}
