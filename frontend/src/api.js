// src/api.js
export const correctText = async (text, language) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(text + " [corrected]");
      }, 1000);
    });
  };