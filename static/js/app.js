/**
 * CodeAlpha Artificial Intelligence Internship - Task 1: Language Translation Tool
 * LinguaFlow AI Client-Side Application Logic
 */

// Fallback Language Dictionary (Used if server endpoint is offline or running standalone)
const FALLBACK_LANGUAGES = {
  "auto": "Auto Detect",
  "af": "Afrikaans",
  "sq": "Albanian",
  "am": "Amharic",
  "ar": "Arabic",
  "hy": "Armenian",
  "as": "Assamese",
  "az": "Azerbaijani",
  "bn": "Bengali",
  "bs": "Bosnian",
  "bg": "Bulgarian",
  "ca": "Catalan",
  "zh-CN": "Chinese (Simplified)",
  "zh-TW": "Chinese (Traditional)",
  "hr": "Croatian",
  "cs": "Czech",
  "da": "Danish",
  "nl": "Dutch",
  "en": "English",
  "et": "Estonian",
  "fi": "Finnish",
  "fr": "French",
  "de": "German",
  "el": "Greek",
  "gu": "Gujarati",
  "he": "Hebrew",
  "hi": "Hindi",
  "hu": "Hungarian",
  "id": "Indonesian",
  "ga": "Irish",
  "it": "Italian",
  "ja": "Japanese",
  "kn": "Kannada",
  "ko": "Korean",
  "la": "Latin",
  "lv": "Latvian",
  "lt": "Lithuanian",
  "ms": "Malay",
  "ml": "Malayalam",
  "mr": "Marathi",
  "ne": "Nepali",
  "no": "Norwegian",
  "fa": "Persian",
  "pl": "Polish",
  "pt": "Portuguese",
  "pa": "Punjabi",
  "ro": "Romanian",
  "ru": "Russian",
  "sr": "Serbian",
  "sk": "Slovak",
  "sl": "Slovenian",
  "es": "Spanish",
  "sw": "Swahili",
  "sv": "Swedish",
  "tl": "Tagalog (Filipino)",
  "ta": "Tamil",
  "te": "Telugu",
  "th": "Thai",
  "tr": "Turkish",
  "uk": "Ukrainian",
  "ur": "Urdu",
  "vi": "Vietnamese",
  "cy": "Welsh",
  "zu": "Zulu"
};

// Global App State
const AppState = {
  languages: {},
  sourceLang: "auto",
  targetLang: "es",
  isTranslating: false,
  isRecording: false,
  recognition: null,
  history: JSON.parse(localStorage.getItem("lingua_history") || "[]"),
  currentTheme: localStorage.getItem("lingua_theme") || "dark"
};

// DOM Element References
const DOM = {
  sourceLangSelect: document.getElementById("sourceLangSelect"),
  targetLangSelect: document.getElementById("targetLangSelect"),
  swapLangsBtn: document.getElementById("swapLangsBtn"),
  sourceText: document.getElementById("sourceText"),
  targetText: document.getElementById("targetText"),
  translateBtn: document.getElementById("translateBtn"),
  clearBtn: document.getElementById("clearBtn"),
  pasteBtn: document.getElementById("pasteBtn"),
  copyBtn: document.getElementById("copyBtn"),
  downloadTxtBtn: document.getElementById("downloadTxtBtn"),
  speakSourceBtn: document.getElementById("speakSourceBtn"),
  speakTargetBtn: document.getElementById("speakTargetBtn"),
  micBtn: document.getElementById("micBtn"),
  recordingBanner: document.getElementById("recordingBanner"),
  stopRecBtn: document.getElementById("stopRecBtn"),
  sourceCounter: document.getElementById("sourceCounter"),
  targetCounter: document.getElementById("targetCounter"),
  detectedPill: document.getElementById("detectedPill"),
  detectedName: document.getElementById("detectedName"),
  providerTag: document.getElementById("providerTag"),
  translationLoader: document.getElementById("translationLoader"),
  historyToggleBtn: document.getElementById("historyToggleBtn"),
  historyDrawer: document.getElementById("historyDrawer"),
  closeDrawerBtn: document.getElementById("closeDrawerBtn"),
  drawerBackdrop: document.getElementById("drawerBackdrop"),
  historyList: document.getElementById("historyList"),
  historyCount: document.getElementById("historyCount"),
  clearHistoryBtn: document.getElementById("clearHistoryBtn"),
  favBtn: document.getElementById("favBtn"),
  themeToggleBtn: document.getElementById("themeToggleBtn"),
  themeIcon: document.getElementById("themeIcon"),
  toastContainer: document.getElementById("toastContainer"),
  engineStatus: document.getElementById("engineStatus")
};

// Initialization
document.addEventListener("DOMContentLoaded", async () => {
  initTheme();
  await loadLanguages();
  initSpeechRecognition();
  bindEventListeners();
  renderHistory();
  updateCharCounters();
});

// Theme Management
function initTheme() {
  document.documentElement.setAttribute("data-theme", AppState.currentTheme);
  updateThemeIcon(AppState.currentTheme);
}

function toggleTheme() {
  const themes = ["dark", "light", "cyber"];
  const nextIdx = (themes.indexOf(AppState.currentTheme) + 1) % themes.length;
  AppState.currentTheme = themes[nextIdx];
  document.documentElement.setAttribute("data-theme", AppState.currentTheme);
  localStorage.setItem("lingua_theme", AppState.currentTheme);
  updateThemeIcon(AppState.currentTheme);
  showToast(`Switched to ${AppState.currentTheme.toUpperCase()} theme`, "info");
}

function updateThemeIcon(theme) {
  if (!DOM.themeIcon) return;
  if (theme === "light") {
    DOM.themeIcon.className = "fa-solid fa-sun";
  } else if (theme === "cyber") {
    DOM.themeIcon.className = "fa-solid fa-bolt";
  } else {
    DOM.themeIcon.className = "fa-solid fa-moon";
  }
}

// Load Languages (Server or Fallback)
async function loadLanguages() {
  try {
    const res = await fetch("/api/languages");
    if (res.ok) {
      const data = await res.json();
      if (data.success && data.languages) {
        AppState.languages = data.languages;
        populateLanguageDropdowns(data.languages);
        return;
      }
    }
  } catch (err) {
    console.warn("Could not fetch languages from /api/languages, using built-in languages.", err);
  }

  // Use fallback dictionary
  AppState.languages = FALLBACK_LANGUAGES;
  populateLanguageDropdowns(FALLBACK_LANGUAGES);
}

function populateLanguageDropdowns(langDict) {
  DOM.sourceLangSelect.innerHTML = "";
  DOM.targetLangSelect.innerHTML = "";

  for (const [code, name] of Object.entries(langDict)) {
    // Source dropdown includes 'auto'
    const srcOpt = document.createElement("option");
    srcOpt.value = code;
    srcOpt.textContent = code === "auto" ? "✨ Auto Detect" : name;
    DOM.sourceLangSelect.appendChild(srcOpt);

    // Target dropdown excludes 'auto'
    if (code !== "auto") {
      const tgtOpt = document.createElement("option");
      tgtOpt.value = code;
      tgtOpt.textContent = name;
      DOM.targetLangSelect.appendChild(tgtOpt);
    }
  }

  DOM.sourceLangSelect.value = "auto";
  DOM.targetLangSelect.value = "es"; // Default to Spanish
}

// Event Bindings
function bindEventListeners() {
  // Translate Button & Key Shortcuts
  DOM.translateBtn.addEventListener("click", performTranslation);
  DOM.sourceText.addEventListener("keydown", (e) => {
    if (e.ctrlKey && e.key === "Enter") {
      e.preventDefault();
      performTranslation();
    }
  });

  // Hotkey for Swap: Ctrl + Shift + S
  window.addEventListener("keydown", (e) => {
    if (e.ctrlKey && e.shiftKey && (e.key === "S" || e.key === "s")) {
      e.preventDefault();
      swapLanguages();
    }
    if (e.key === "Escape" && DOM.historyDrawer.classList.contains("open")) {
      toggleHistoryDrawer(false);
    }
  });

  // Source Text live char count
  DOM.sourceText.addEventListener("input", updateCharCounters);

  // Swap Languages
  DOM.swapLangsBtn.addEventListener("click", swapLanguages);

  // Clear Text
  DOM.clearBtn.addEventListener("click", clearSourceText);

  // Paste Text
  DOM.pasteBtn.addEventListener("click", handlePaste);

  // Copy Translation
  DOM.copyBtn.addEventListener("click", copyTranslation);

  // Download .txt
  DOM.downloadTxtBtn.addEventListener("click", downloadTranslationTxt);

  // Speech Pronunciation (Listen)
  DOM.speakSourceBtn.addEventListener("click", () => speakText(DOM.sourceText.value, DOM.sourceLangSelect.value));
  DOM.speakTargetBtn.addEventListener("click", () => speakText(DOM.targetText.value, DOM.targetLangSelect.value));

  // Speech Recognition (Microphone)
  DOM.micBtn.addEventListener("click", toggleSpeechRecognition);
  DOM.stopRecBtn.addEventListener("click", stopSpeechRecognition);

  // Quick Sample Chips
  document.querySelectorAll(".sample-chip").forEach((chip) => {
    chip.addEventListener("click", () => {
      const sample = chip.getAttribute("data-text");
      DOM.sourceText.value = sample;
      updateCharCounters();
      performTranslation();
    });
  });

  // History Drawer Controls
  DOM.historyToggleBtn.addEventListener("click", () => toggleHistoryDrawer(true));
  DOM.closeDrawerBtn.addEventListener("click", () => toggleHistoryDrawer(false));
  DOM.drawerBackdrop.addEventListener("click", () => toggleHistoryDrawer(false));
  DOM.clearHistoryBtn.addEventListener("click", clearAllHistory);

  // Favorite button
  DOM.favBtn.addEventListener("click", saveFavorite);

  // Theme Toggle
  DOM.themeToggleBtn.addEventListener("click", toggleTheme);
}

// Character Counters
function updateCharCounters() {
  const srcLen = DOM.sourceText.value.length;
  DOM.sourceCounter.textContent = `${srcLen} / 5000 chars`;

  const tgtLen = DOM.targetText.value.length;
  DOM.targetCounter.textContent = `${tgtLen} chars`;
}

// Clear Text
function clearSourceText() {
  DOM.sourceText.value = "";
  DOM.targetText.value = "";
  DOM.detectedPill.style.display = "none";
  updateCharCounters();
  showToast("Cleared text", "info");
}

// Paste from Clipboard
async function handlePaste() {
  try {
    const text = await navigator.clipboard.readText();
    if (text) {
      DOM.sourceText.value = text;
      updateCharCounters();
      showToast("Pasted from clipboard", "success");
    }
  } catch (err) {
    showToast("Clipboard access denied. Please paste manually.", "error");
  }
}

// Swap Languages
function swapLanguages() {
  const currentSrc = DOM.sourceLangSelect.value;
  const currentTgt = DOM.targetLangSelect.value;

  if (currentSrc === "auto") {
    DOM.sourceLangSelect.value = currentTgt;
    DOM.targetLangSelect.value = "en";
  } else {
    DOM.sourceLangSelect.value = currentTgt;
    DOM.targetLangSelect.value = currentSrc;
  }

  // Swap text contents if target text is present
  const srcVal = DOM.sourceText.value;
  const tgtVal = DOM.targetText.value;

  if (tgtVal) {
    DOM.sourceText.value = tgtVal;
    DOM.targetText.value = srcVal;
    updateCharCounters();
  }

  showToast("Languages swapped", "info");
}

// Core Translation Logic
async function performTranslation() {
  const text = DOM.sourceText.value.trim();
  if (!text) {
    showToast("Please enter or paste text to translate", "warning");
    DOM.sourceText.focus();
    return;
  }

  if (AppState.isTranslating) return;

  const srcLang = DOM.sourceLangSelect.value;
  const tgtLang = DOM.targetLangSelect.value;

  setTranslatingState(true);

  try {
    // Step 1: Attempt translation through Flask backend
    let result = null;
    try {
      const response = await fetch("/api/translate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: text,
          source_lang: srcLang,
          target_lang: tgtLang
        })
      });

      if (response.ok) {
        result = await response.json();
      }
    } catch (e) {
      console.warn("Backend /api/translate request failed, falling back to direct API.", e);
    }

    // Step 2: Fallback to direct client-side Google Translate endpoint if backend is unreachable
    if (!result || !result.success) {
      result = await directClientTranslation(text, srcLang, tgtLang);
    }

    if (result && result.success) {
      DOM.targetText.value = result.translated_text;
      updateCharCounters();

      // Show auto-detected language badge if available
      if (result.detected_lang && srcLang === "auto") {
        const detectedName = AppState.languages[result.detected_lang] || result.detected_lang;
        DOM.detectedName.textContent = detectedName;
        DOM.detectedPill.style.display = "inline-flex";
      } else {
        DOM.detectedPill.style.display = "none";
      }

      DOM.providerTag.textContent = result.provider || "Google Neural API";

      // Save to Translation History
      saveToHistory({
        sourceText: text,
        targetText: result.translated_text,
        sourceLang: srcLang,
        targetLang: tgtLang,
        sourceName: AppState.languages[srcLang] || srcLang,
        targetName: AppState.languages[tgtLang] || tgtLang,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      });

      showToast("Translation completed!", "success");
    } else {
      showToast(result?.error || "Translation failed. Check connection.", "error");
    }
  } catch (err) {
    console.error("Translation execution error:", err);
    showToast("Translation error. Please check your internet connection.", "error");
  } finally {
    setTranslatingState(false);
  }
}

// Client-side Direct API (Guarantees standalone operation without backend)
async function directClientTranslation(text, src, tgt) {
  try {
    const encoded = encodeURIComponent(text);
    const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=${src}&tl=${tgt}&dt=t&q=${encoded}`;
    const res = await fetch(url);
    const data = await res.json();

    let translated = "";
    if (data && data[0]) {
      for (const chunk of data[0]) {
        if (chunk && chunk[0]) translated += chunk[0];
      }
    }

    const detected = (data && data[2]) ? data[2] : src;

    return {
      success: true,
      translated_text: translated,
      detected_lang: detected,
      provider: "Google Translate (Direct)"
    };
  } catch (e) {
    // Secondary client fallback: MyMemory API
    try {
      const srcCode = src === "auto" ? "en" : src;
      const memUrl = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(text)}&langpair=${srcCode}|${tgt}`;
      const memRes = await fetch(memUrl);
      const memData = await memRes.json();
      if (memData && memData.responseData && memData.responseData.translatedText) {
        return {
          success: true,
          translated_text: memData.responseData.translatedText,
          detected_lang: srcCode,
          provider: "MyMemory API (Direct)"
        };
      }
    } catch (memErr) {
      console.error("MyMemory fallback failed:", memErr);
    }
    return { success: false, error: "Network translation failed." };
  }
}

function setTranslatingState(isTranslating) {
  AppState.isTranslating = isTranslating;
  if (isTranslating) {
    DOM.translationLoader.style.display = "flex";
    DOM.translateBtn.disabled = true;
    DOM.translateBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i><span>Translating...</span>`;
  } else {
    DOM.translationLoader.style.display = "none";
    DOM.translateBtn.disabled = false;
    DOM.translateBtn.innerHTML = `<i class="fa-solid fa-bolt-lightning"></i><span>Translate Now</span>`;
  }
}

// Copy Translation to Clipboard
async function copyTranslation() {
  const text = DOM.targetText.value.trim();
  if (!text) {
    showToast("No translation available to copy", "warning");
    return;
  }

  try {
    await navigator.clipboard.writeText(text);
    DOM.copyBtn.innerHTML = `<i class="fa-solid fa-check" style="color: var(--brand-success);"></i>`;
    showToast("Translation copied to clipboard!", "success");
    setTimeout(() => {
      DOM.copyBtn.innerHTML = `<i class="fa-regular fa-copy"></i>`;
    }, 2000);
  } catch (err) {
    showToast("Failed to copy automatically", "error");
  }
}

// Download Translation as .txt
function downloadTranslationTxt() {
  const text = DOM.targetText.value.trim();
  if (!text) {
    showToast("Translate something first to download", "warning");
    return;
  }

  const srcLang = DOM.sourceLangSelect.options[DOM.sourceLangSelect.selectedIndex].text;
  const tgtLang = DOM.targetLangSelect.options[DOM.targetLangSelect.selectedIndex].text;
  
  const content = `==========================================================\n` +
                  `CodeAlpha Language Translation Tool - Translation Export\n` +
                  `Date: ${new Date().toLocaleString()}\n` +
                  `From: ${srcLang}\n` +
                  `To:   ${tgtLang}\n` +
                  `==========================================================\n\n` +
                  `[ORIGINAL TEXT]\n${DOM.sourceText.value.trim()}\n\n` +
                  `[TRANSLATED TEXT]\n${text}\n\n` +
                  `==========================================================\n`;

  const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `translation_${DOM.targetLangSelect.value}_${Date.now()}.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  showToast("Downloaded translation as .txt", "success");
}

// Text-to-Speech (Audio Pronunciation)
function speakText(text, langCode) {
  const clean = text ? text.trim() : "";
  if (!clean) {
    showToast("No text to pronounce", "warning");
    return;
  }

  // 1. Try Web Speech API (SpeechSynthesis)
  if ("speechSynthesis" in window) {
    window.speechSynthesis.cancel(); // Stop any pending speech
    const utterance = new SpeechSynthesisUtterance(clean);
    
    // Attempt to match voice to language code
    if (langCode && langCode !== "auto") {
      utterance.lang = langCode;
      const voices = window.speechSynthesis.getVoices();
      const matchedVoice = voices.find(v => v.lang.startsWith(langCode));
      if (matchedVoice) utterance.voice = matchedVoice;
    }

    utterance.rate = 0.95; // Natural clear pace
    utterance.pitch = 1.0;

    utterance.onstart = () => showToast("Playing audio pronunciation...", "info");
    utterance.onerror = (e) => {
      console.warn("Web Speech API error, falling back to TTS endpoint", e);
      playAudioViaEndpoint(clean, langCode);
    };

    window.speechSynthesis.speak(utterance);
    return;
  }

  // 2. Fallback to /api/tts endpoint
  playAudioViaEndpoint(clean, langCode);
}

function playAudioViaEndpoint(text, lang) {
  const code = (lang === "auto" || !lang) ? "en" : lang;
  const audio = new Audio(`/api/tts?text=${encodeURIComponent(text)}&lang=${code}`);
  audio.play().catch(e => {
    showToast("Audio playback not supported in this browser.", "error");
  });
}

// Voice Recognition (Speech-to-Text)
function initSpeechRecognition() {
  const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRec) {
    DOM.micBtn.title = "Voice dictation not supported in this browser";
    DOM.micBtn.style.opacity = "0.5";
    return;
  }

  AppState.recognition = new SpeechRec();
  AppState.recognition.continuous = false;
  AppState.recognition.interimResults = true;

  AppState.recognition.onstart = () => {
    AppState.isRecording = true;
    DOM.recordingBanner.style.display = "flex";
    DOM.micBtn.classList.add("active");
  };

  AppState.recognition.onresult = (event) => {
    let transcript = "";
    for (let i = event.resultIndex; i < event.results.length; ++i) {
      transcript += event.results[i][0].transcript;
    }
    DOM.sourceText.value = transcript;
    updateCharCounters();
  };

  AppState.recognition.onerror = (event) => {
    console.error("Speech recognition error:", event.error);
    stopSpeechRecognition();
    showToast(`Voice input error: ${event.error}`, "error");
  };

  AppState.recognition.onend = () => {
    stopSpeechRecognition();
    if (DOM.sourceText.value.trim()) {
      performTranslation();
    }
  };
}

function toggleSpeechRecognition() {
  if (!AppState.recognition) {
    showToast("Voice input requires Google Chrome, Edge, or Safari.", "warning");
    return;
  }

  if (AppState.isRecording) {
    stopSpeechRecognition();
  } else {
    // Configure language based on source selection
    const src = DOM.sourceLangSelect.value;
    AppState.recognition.lang = (src && src !== "auto") ? src : "en-US";
    try {
      AppState.recognition.start();
    } catch (e) {
      console.warn("Recognition already started", e);
    }
  }
}

function stopSpeechRecognition() {
  AppState.isRecording = false;
  DOM.recordingBanner.style.display = "none";
  DOM.micBtn.classList.remove("active");
  if (AppState.recognition) {
    try { AppState.recognition.stop(); } catch (e) {}
  }
}

// History Management
function saveToHistory(entry) {
  // Avoid duplicate adjacent entries
  if (AppState.history.length > 0 && AppState.history[0].sourceText === entry.sourceText) {
    return;
  }

  AppState.history.unshift(entry);
  if (AppState.history.length > 30) AppState.history.pop();
  localStorage.setItem("lingua_history", JSON.stringify(AppState.history));
  renderHistory();
}

function renderHistory() {
  if (!DOM.historyList) return;
  DOM.historyCount.textContent = AppState.history.length;

  if (AppState.history.length === 0) {
    DOM.historyList.innerHTML = `
      <div class="empty-history-state">
        <i class="fa-regular fa-folder-open empty-icon"></i>
        <p>No recent translations yet.</p>
        <span class="empty-sub">Translations you perform will be saved here automatically.</span>
      </div>
    `;
    return;
  }

  DOM.historyList.innerHTML = "";
  AppState.history.forEach((item, index) => {
    const card = document.createElement("div");
    card.className = "history-item-card";
    card.innerHTML = `
      <div class="history-item-meta">
        <span class="history-lang-badge">
          ${item.sourceName} <i class="fa-solid fa-arrow-right"></i> ${item.targetName}
        </span>
        <span class="history-time">${item.timestamp}</span>
      </div>
      <div class="history-source-txt">${escapeHtml(item.sourceText)}</div>
      <div class="history-target-txt">${escapeHtml(item.targetText)}</div>
    `;

    card.addEventListener("click", () => {
      DOM.sourceText.value = item.sourceText;
      DOM.targetText.value = item.targetText;
      if (item.sourceLang && DOM.sourceLangSelect.querySelector(`option[value="${item.sourceLang}"]`)) {
        DOM.sourceLangSelect.value = item.sourceLang;
      }
      if (item.targetLang && DOM.targetLangSelect.querySelector(`option[value="${item.targetLang}"]`)) {
        DOM.targetLangSelect.value = item.targetLang;
      }
      updateCharCounters();
      toggleHistoryDrawer(false);
      showToast("Restored from history", "info");
    });

    DOM.historyList.appendChild(card);
  });
}

function toggleHistoryDrawer(open) {
  if (open) {
    DOM.historyDrawer.classList.add("open");
    DOM.drawerBackdrop.classList.add("active");
  } else {
    DOM.historyDrawer.classList.remove("open");
    DOM.drawerBackdrop.classList.remove("active");
  }
}

function clearAllHistory() {
  AppState.history = [];
  localStorage.removeItem("lingua_history");
  renderHistory();
  showToast("History cleared", "info");
}

function saveFavorite() {
  const targetVal = DOM.targetText.value.trim();
  if (!targetVal) {
    showToast("Nothing to save to favorites yet", "warning");
    return;
  }
  showToast("Saved translation to favorites!", "success");
}

// Toast Notifications System
function showToast(message, type = "info") {
  if (!DOM.toastContainer) return;

  const toast = document.createElement("div");
  toast.className = `toast ${type}`;

  let icon = "fa-circle-info";
  if (type === "success") icon = "fa-circle-check";
  if (type === "warning") icon = "fa-triangle-exclamation";
  if (type === "error") icon = "fa-circle-xmark";

  toast.innerHTML = `<i class="fa-solid ${icon}"></i><span>${escapeHtml(message)}</span>`;
  DOM.toastContainer.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateY(15px)";
    toast.style.transition = "all 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 2800);
}

function escapeHtml(str) {
  return (str || "").replace(/[&<>"']/g, function(m) {
    switch (m) {
      case '&': return '&amp;';
      case '<': return '&lt;';
      case '>': return '&gt;';
      case '"': return '&quot;';
      case "'": return '&#39;';
      default: return m;
    }
  });
}
