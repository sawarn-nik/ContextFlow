// src/components/LanguageSelector.js
import React from "react";

const LanguageSelector = ({ language, setLanguage }) => {
  return (
    <div>
      <label htmlFor="language-select" className="mr-2">
        Language:
      </label>
      <select
        id="language-select"
        value={language}
        onChange={(e) => setLanguage(e.target.value)}
        className="p-1 border rounded"
      >
        <option value="en">English</option>
        <option value="hi">Hindi</option>
      </select>
    </div>
  );
};

export default LanguageSelector;
