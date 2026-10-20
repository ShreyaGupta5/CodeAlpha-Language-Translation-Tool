# 🌐 CodeAlpha AI Internship — Task 1: Language Translation Tool

![CodeAlpha Internship](https://img.shields.io/badge/CodeAlpha-AI%20Internship-blue.svg?style=for-the-badge)
![Task](https://img.shields.io/badge/Task-1%3A%20Language%20Translation%20Tool-success.svg?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0%2B-black.svg?style=for-the-badge&logo=flask)
![Languages](https://img.shields.io/badge/Supported%20Languages-100%2B-purple.svg?style=for-the-badge)

---

## 📌 Project Overview

This repository contains the complete implementation of **Task 1: Language Translation Tool** developed for the **CodeAlpha Artificial Intelligence Internship**.

The tool bridges language barriers by translating text across **over 100+ global languages** in real time. It features a modern **dual-interface design**:
1. **Interactive Web Application (Flask + Glassmorphic UI)** with live voice recognition (Speech-to-Text), audio pronunciation (Text-to-Speech), clipboard copy, translation history, and theme customization.
2. **Native Desktop GUI Application (Tkinter)** for offline-friendly, high-DPI desktop usage.
3. **Standalone Web Mode (`index.html`)** which functions directly in any web browser without requiring a backend server.

---

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| **100+ Global Languages** | Translates between English, Hindi, Spanish, French, German, Japanese, Chinese, Arabic, Russian, and 90+ other languages. |
| **Auto Language Detection** | Automatically identifies the input language and displays a badge with the detected language name. |
| **Dual Translation Engine** | Utilizes **Google Translate API** as primary neural translation with **MyMemory API** as automatic fallback. |
| **🔊 Text-to-Speech (TTS)** | Crystal-clear audio pronunciation of both source and translated text with natural accents. |
| **🎙️ Voice Input (Speech-to-Text)** | Speak directly into the microphone to dictate sentences into the translator. |
| **📋 One-Click Copy & Export** | Instant copy to clipboard with toast feedback, plus export translation to `.txt`. |
| **⇄ Quick Language Swap** | Swap source and target languages (and text) with 1 click or keyboard shortcut (`Ctrl + Shift + S`). |
| **🕒 Translation History** | Automatically stores recent translations with timestamps, 1-click restore, and favorite bookmarks. |
| **🎨 Glassmorphic Aesthetic** | Modern glassmorphism UI with Dark, Light, and Cyberpunk neon themes. |
| **🖥️ Dual Platform (Web + GUI)** | Run either as a full-stack Flask web application or a standalone Python Tkinter desktop GUI. |

---

## 🏗️ Project Architecture

```
CodeAlpha_Task 1_Language Translation Tool/
│
├── app.py                      # Flask Web Application Server & API endpoints
├── gui_app.py                  # Tkinter Desktop GUI Application
├── translator_engine.py        # Core Translation Engine (Google + MyMemory fallback)
├── index.html                  # Standalone Web Application (Double-click ready)
├── requirements.txt            # Python dependencies (Flask, requests)
├── run_web.bat                 # 1-Click launcher for Web Application
├── run_gui.bat                 # 1-Click launcher for Desktop GUI Application
├── .gitignore                  # Git ignore rules
├── README.md                   # Complete documentation & submission guide
│
├── templates/
│   └── index.html              # Jinja2 template for Flask web server
│
└── static/
    ├── css/
    │   └── style.css           # Glassmorphism design system & theme styling
    └── js/
        └── app.js              # Client-side reactivity, Web Speech API, TTS, History
```

---

## 🚀 How to Run the Project

### Prerequisites
Make sure **Python 3.9+** is installed on your system.

### 1. Clone or Open the Repository
```bash
cd "CodeAlpha_Task 1_Language Translation Tool"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

### Option A: Run the Modern Web Application (Recommended)
You can double-click **`run_web.bat`** OR execute:
```bash
python app.py
```
> The browser will automatically open at: **`http://127.0.0.1:5000`**

---

### Option B: Run the Desktop GUI Application
You can double-click **`run_gui.bat`** OR execute:
```bash
python gui_app.py
```
> Opens a native desktop window with Tkinter dark theme.

---

### Option C: Run Standalone in Browser (No Server Needed)
Simply double-click the **`index.html`** file in Windows File Explorer. It opens directly in Google Chrome, Microsoft Edge, or Firefox and translates via client-side APIs!

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
| :--- | :--- |
| `Ctrl + Enter` | Translate input text immediately |
| `Ctrl + Shift + S` | Swap source and target languages |
| `Esc` | Close history drawer |

---

## 🎬 LinkedIn Video & Presentation Guide (CodeAlpha Submission)

According to CodeAlpha guidelines:
1. Push your code to GitHub with a repository named: `CodeAlpha_LanguageTranslationTool`.
2. Record a **1 to 2 minute video demonstration** of your tool.
3. Post the video on LinkedIn tagging **@CodeAlpha** with the GitHub repository link.

### 📝 LinkedIn Post Template

```markdown
🚀 Excited to share my first task as an Artificial Intelligence Intern at CodeAlpha! 🤖

For Task 1, I built a comprehensive "Language Translation Tool" (LinguaFlow AI) that supports 100+ languages in real time.

🌟 Key Features:
✅ High-performance translation using Google Translate API with automatic fallback
✅ Automatic source language detection
✅ Text-to-Speech (audio pronunciation) & Speech-to-Text (voice typing)
✅ 1-click clipboard copy, swap, and translation history
✅ Built with both a modern Glassmorphism Web App (Flask/JS) and a Desktop GUI (Python Tkinter)

📂 GitHub Repository: [Insert Your GitHub Repo Link Here]

Special thanks to @CodeAlpha for this valuable hands-on learning opportunity! 💡

#CodeAlpha #ArtificialIntelligence #MachineLearning #Python #NLP #LanguageTranslation #Flask #WebDevelopment #Internship #StudentDeveloper
```

---

## 📄 License
Developed for educational and portfolio demonstration during the **CodeAlpha Artificial Intelligence Internship**.
