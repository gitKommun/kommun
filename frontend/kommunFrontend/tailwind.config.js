/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  safelist: [
    {pattern: /bg-./},
    {pattern: /text-./},
    {pattern: /border-./},
  ],
  theme: {
    extend: {
      width: {
        100: '25rem',
        110: '27.5rem',
        112: '28rem',
        114: '28.5rem',
        116: '29rem',
        118: '29.5rem',
        120: '30rem',
        124: '31rem',
        126: '31.5rem',
        128: '32rem',
        136: '34rem',
        140: '35rem',
        144: '36rem',
        148: '37rem',
        150: '37.5rem',
        152: '38rem',
        156: '39rem',
        160: '40rem',
      }
    },
  },
  plugins: [require('tailwindcss-primeui')],
}

