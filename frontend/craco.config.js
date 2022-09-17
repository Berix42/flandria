module.exports = {
  style: {
    postcssOptions: {
      plugins: [
        require('tailwindcss'), //eslint-disable-line
        require('autoprefixer'), //eslint-disable-line
      ],
    },
  },
  eslint: null,
};
