import React, { useState, useRef, useEffect, useCallback } from "react";
import "./App.css";

function App() {
  const [showMenu, setShowMenu] = useState(false);
  const menuRef = useRef(null);
  const [inputText, setInputText] = useState("");
  const [correctedText, setCorrectedText] = useState("");
  const [loading, setLoading] = useState(false); // 🔄 Loading state
  const [statusMsg, setStatusMsg] = useState(""); // 💬

  useEffect(() => {
  document.querySelector(".input-box").focus();
  }, []);

  // Close menu when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setShowMenu(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleRaiseIssue = () => {
    window.location.href =
      "mailto:32kumariruchi@gmail.com?subject=Issue%20with%20CorrectMe&body=Describe%20your%20issue:";
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && e.ctrlKey) handleSubmit();
  };

  // Send input text to backend
  const handleSubmit = useCallback(async () => {
    if (!inputText.trim()) return;

    setLoading(true); // 🌀 Start loading
    setCorrectedText("");

    // 💬 Random AI thinking message
    const thinkingMessages = [
      "🤖 Analyzing grammar...",
      "🧠 Correcting spelling...",
      "✨ Polishing your writing...",
      "📖 Checking sentence flow...",
      "🪄 Refining your text..."
    ];
    // Randomly pick one message
    setStatusMsg(thinkingMessages[Math.floor(Math.random() * thinkingMessages.length)]);

    try {
      const response = await fetch("http://127.0.0.1:8000/spellcheck", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: inputText }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      setCorrectedText(data.correctedText || "No corrections found.");
    } catch (error) {
      console.error("Error correcting spelling:", error.message);
      setCorrectedText("⚠️ Error contacting AI service.");
    } finally {
      setLoading(false); // ✅ Stop loading
    }
  }, [inputText]);

  return (
    <div className="container">
      {/* Menu */}
      <div className="menu-container" ref={menuRef}>
        <button
          className="menu-button"
          onClick={() => setShowMenu(!showMenu)}
          aria-label="Menu Button"
        >
          ⋮
        </button>
        {showMenu && (
          <div className="dropdown-menu">
            <button className="menu-item">English</button>
            <button className="menu-item">हिंदी</button>
            <button className="menu-item raise-issue" onClick={handleRaiseIssue}>
              Raise an Issue
            </button>
          </div>
        )}
      </div>

      <h1 className="title">Correct Me</h1>
      <img src="./logo.png" alt="Logo" className="logo" />

      {/* Input Box */}
      <textarea
        className="input-box"
        placeholder="Type here..."
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
      ></textarea>

      <div className="mic-container">
        <button
          className="mic-button"
          onClick={() => {
            const recognition = new (window.SpeechRecognition ||
              window.webkitSpeechRecognition)();
            recognition.lang = "en-US";
            recognition.start();
            recognition.onresult = (event) => {
              const transcript = event.results[0][0].transcript;
              setInputText((prev) => `${prev} ${transcript}`);
            };
          }}
        >
          🎤 Speak
        </button>
      </div>

      {/* Submit and Clear Buttons */}
      <div className="button-container">
        <button
          className="submit-button"
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? "Processing..." : "Submit"}
        </button>

        <button
          className="clear-button"
          onClick={() => {
            setInputText("");
            setCorrectedText("");
          }}
        >
          Clear
        </button>
      </div>

      <p className="loading-text">{statusMsg}</p>


      {/* Output Box */}
      {!loading && correctedText && (
        <div className="output-container">
          <h3>Corrected Text:</h3>
          <textarea
            className="output-box"
            value={correctedText}
            readOnly
          ></textarea>
        </div>
      )}

      <div className="copyright">© {new Date().getFullYear()}</div>
    </div>
  );


}

export default App;
