module.exports = {
  env: {
    browser: true,
    es2021: true,
  },
  extends: [
    'plugin:react/recommended',
    'airbnb',
  ],
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 12,
    sourceType: 'module',
  },
  plugins: [
    'react',
  ],
  rules: {
    'linebreak-style': 0,
    'react/prop-types': 0,
    'no-console': 'off',
    'prefer-destructuring': ['error', { object: false, array: false }],
    'import/no-extraneous-dependencies': ['error', { devDependencies: false }],
    'react/function-component-definition': [2, { namedComponents: 'arrow-function', unnamedComponents: 'arrow-function' }],
    'no-unused-expressions': ['error', { allowTernary: true }],
  },
};
