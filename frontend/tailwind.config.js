/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'aurora': 'aurora 18s ease infinite alternate',
        'pulse-glow': 'pulse-glow 3s ease infinite',
      },
      keyframes: {
        aurora: {
          '0%': { opacity: 0.7, transform: 'scale(1) rotate(0deg)' },
          '50%': { opacity: 1, transform: 'scale(1.05) rotate(1deg)' },
          '100%': { opacity: 0.8, transform: 'scale(1) rotate(-1deg)' },
        },
        'pulse-glow': {
          '0%, 100%': { filter: 'drop-shadow(0 0 16px rgba(99,102,241,0.5))' },
          '50%': { filter: 'drop-shadow(0 0 28px rgba(139,92,246,0.7))' },
        }
      }
    },
  },
  plugins: [],
}
