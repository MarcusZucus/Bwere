/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./*.{html,js}"], // Escanea archivos HTML y JS en la raíz
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6', // Azul personalizado
        accent: '#f472b6',  // Rosa personalizado
        neutral: '#6b7280', // Gris personalizado
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'], // Fuente personalizada
      },
    },
  },
  plugins: [],
};
