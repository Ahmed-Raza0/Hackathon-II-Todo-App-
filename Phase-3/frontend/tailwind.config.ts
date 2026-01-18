/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{ts,tsx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#4f46e5', // indigo-600
        },
        secondary: {
          DEFAULT: '#475569', // slate-600
        },
        accent: {
          DEFAULT: '#10b981', // emerald-400
        },
        warning: {
          DEFAULT: '#facc15', // yellow-400
        },
        error: {
          DEFAULT: '#ef4444', // red-500
        },
        background: {
          DEFAULT: '#020617', // slate-950
        },
        text: {
          DEFAULT: '#f1f5f9', // slate-100
        }
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic':
          'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
    },
  },
  plugins: [],
}