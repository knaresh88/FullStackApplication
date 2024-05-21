// jest.config.js
module.exports = {
  setupFilesAfterEnv: ['<rootDir>/setupTests.js'],

  testEnvironment: 'jest-environment-jsdom',
  moduleNameMapper: {
    '\\.(css|less)$': 'identity-obj-proxy',
  },
  "moduleFileExtensions": [
    "js",
    "jsx",
    "json",
    "node"
  ],  
  transform: {
    '^.+\\.(js|jsx)$': 'babel-jest',
  },
};