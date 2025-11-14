import React from "react";

const TextInput = ({ text, setText }) => {
  return (
    <textarea
      value={text}
      onKeyDown={handleKeyPress}
      placeholder="Type here... (Press Ctrl+Enter to submit)"
    />
  );
};

export default TextInput;