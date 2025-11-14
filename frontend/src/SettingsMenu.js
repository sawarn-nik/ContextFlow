// src/components/SettingsMenu.js
import React, { useState, useEffect, useRef } from "react";
import LanguageSelector from "./LanguageSelector";

const SettingsMenu = ({ language, setLanguage, showHistory, setShowHistory }) => {
  const [open, setOpen] = useState(false);
  const menuRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <div className="relative" ref={menuRef}>
      <button
        className="p-2 focus:outline-none"
        onClick={() => setOpen((prev) => !prev)}
      >
        <span className="text-2xl">⋮</span>
      </button>
      {open && (
        <div className="absolute left-0 mt-2 w-56 bg-white rounded shadow-lg z-10">
          <div className="px-4 py-2 border-b">
            <LanguageSelector language={language} setLanguage={setLanguage} />
          </div>
          <button
            onClick={() => setShowHistory((prev) => !prev)}
            className="w-full text-left px-4 py-2 hover:bg-gray-100"
          >
            {showHistory ? "Hide History" : "Show History"}
          </button>
        </div>
      )}
    </div>
  );
};

export default SettingsMenu;