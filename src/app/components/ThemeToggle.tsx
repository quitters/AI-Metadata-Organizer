"use client";
import React, { useEffect, useState } from "react";

export default function ThemeToggle() {
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem("aiimgmgr-darkmode");
    let enabled: boolean;
    if (stored !== null) {
      enabled = stored === "true";
    } else {
      enabled = window.matchMedia("(prefers-color-scheme: dark)").matches;
    }
    setDarkMode(enabled);
    if (enabled) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, []);

  const toggleDarkMode = () => {
    setDarkMode((prev) => {
      const newMode = !prev;
      localStorage.setItem("aiimgmgr-darkmode", newMode.toString());
      if (newMode) {
        document.documentElement.classList.add("dark");
      } else {
        document.documentElement.classList.remove("dark");
      }
      return newMode;
    });
  };

  return (
    <button
      style={{
        position: "fixed",
        top: 16,
        right: 16,
        zIndex: 1000,
        padding: "6px 16px",
        borderRadius: 8,
        border: "1px solid var(--foreground)",
        background: "var(--background)",
        color: "var(--foreground)",
        cursor: "pointer",
        boxShadow: "0 1px 6px rgba(0,0,0,0.07)",
        transition: "background 0.2s, color 0.2s, border 0.2s",
      }}
      onClick={toggleDarkMode}
      aria-label="Toggle night mode"
    >
      {darkMode ? "☀️ Light" : "🌙 Night"}
    </button>
  );
}
