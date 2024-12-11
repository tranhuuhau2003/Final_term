module.exports = {
  testEnvironment: 'jsdom',
  transform: {
    '^.+\\.js$': 'babel-jest',
  },
  // Xóa dòng extensionsToTreatAsEsm vì Jest tự động suy luận loại module từ package.json
};
