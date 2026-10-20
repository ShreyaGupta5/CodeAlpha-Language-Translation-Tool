"""
CodeAlpha Artificial Intelligence Internship - Task 1: Language Translation Tool
Desktop GUI Application (Modern Tkinter)
"""

import sys
import threading
import time
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import ctypes

from translator_engine import translate_text, LANGUAGES

# Attempt High-DPI scaling on Windows for crisp typography
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# Theme Color Palette (Modern Dark / Slate)
BG_DARK = "#0B0F19"         # Deep background
BG_PANEL = "#111827"        # Card panel background
BG_SURFACE = "#1E293B"      # Text area / input surface
BG_SURFACE_HOVER = "#334155"# Hover surface
BORDER_COLOR = "#374151"    # Clean subtle border
TEXT_PRIMARY = "#F8FAFC"    # Crisp bright text
TEXT_SECONDARY = "#94A3B8"  # Slate secondary text
ACCENT_PRIMARY = "#4F46E5"  # Indigo button accent
ACCENT_HOVER = "#4338CA"    # Darker indigo hover
ACCENT_CYAN = "#06B6D4"     # Secondary cyan accent
ACCENT_GREEN = "#10B981"    # Success green

SAMPLE_PHRASES = [
    "-- Select a sample phrase to test --",
    "Hello, welcome to CodeAlpha Language Translation Tool!",
    "Artificial Intelligence is transforming how we communicate across borders.",
    "Could you please tell me where the nearest train station is?",
    "Thank you very much for your continuous support and guidance.",
    "Machine learning models are trained on large multilingual datasets."
]

class TranslatorGUIApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("CodeAlpha — Language Translation Tool")
        self.root.geometry("980x680")
        self.root.minsize(860, 580)
        self.root.configure(bg=BG_DARK)

        # Build language lookup lists
        # Sort languages alphabetically by English name, keeping 'auto' at top
        self.lang_name_to_code = {v: k for k, v in LANGUAGES.items()}
        self.sorted_names = ["Auto Detect"] + sorted([v for k, v in LANGUAGES.items() if k != "auto"])
        self.target_names = [name for name in self.sorted_names if name != "Auto Detect"]

        self._configure_styles()
        self._build_ui()
        self._bind_events()

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Custom Combobox Styling
        style.configure(
            "Dark.TCombobox",
            fieldbackground=BG_SURFACE,
            background=BG_SURFACE,
            foreground=TEXT_PRIMARY,
            darkcolor=BORDER_COLOR,
            lightcolor=BORDER_COLOR,
            arrowcolor=TEXT_PRIMARY,
            padding=6,
            relief="flat"
        )
        style.map(
            "Dark.TCombobox",
            fieldbackground=[("readonly", BG_SURFACE)],
            foreground=[("readonly", TEXT_PRIMARY)],
            selectbackground=[("readonly", BG_SURFACE)],
            selectforeground=[("readonly", TEXT_PRIMARY)]
        )

    def _build_ui(self):
        # Top Header Bar
        header_frame = tk.Frame(self.root, bg=BG_PANEL, pady=14, padx=24)
        header_frame.pack(fill=tk.X)

        title_lbl = tk.Label(
            header_frame,
            text="🌐 CodeAlpha Language Translation Tool",
            font=("Segoe UI", 16, "bold"),
            fg=TEXT_PRIMARY,
            bg=BG_PANEL
        )
        title_lbl.pack(side=tk.LEFT)

        badge_lbl = tk.Label(
            header_frame,
            text="Task 1 • AI Powered",
            font=("Segoe UI", 9, "bold"),
            fg=ACCENT_CYAN,
            bg=BG_SURFACE,
            padx=10,
            pady=3
        )
        badge_lbl.pack(side=tk.RIGHT)

        # Main Workspace Container
        main_container = tk.Frame(self.root, bg=BG_DARK, padx=20, pady=16)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Quick Samples Bar
        samples_bar = tk.Frame(main_container, bg=BG_DARK, pady=4)
        samples_bar.pack(fill=tk.X)

        sample_lbl = tk.Label(
            samples_bar,
            text="Quick Test Phrase:",
            font=("Segoe UI", 9),
            fg=TEXT_SECONDARY,
            bg=BG_DARK
        )
        sample_lbl.pack(side=tk.LEFT, padx=(0, 8))

        self.sample_combo = ttk.Combobox(
            samples_bar,
            values=SAMPLE_PHRASES,
            state="readonly",
            style="Dark.TCombobox",
            width=50,
            font=("Segoe UI", 9)
        )
        self.sample_combo.current(0)
        self.sample_combo.bind("<<ComboboxSelected>>", self._on_sample_selected)
        self.sample_combo.pack(side=tk.LEFT)

        # Language Selection Control Bar
        lang_bar = tk.Frame(main_container, bg=BG_PANEL, padx=16, pady=12, highlightbackground=BORDER_COLOR, highlightthickness=1)
        lang_bar.pack(fill=tk.X, pady=(12, 16))

        # Source Language Selector
        src_box = tk.Frame(lang_bar, bg=BG_PANEL)
        src_box.pack(side=tk.LEFT, expand=True, fill=tk.X)

        tk.Label(
            src_box,
            text="Translate from:",
            font=("Segoe UI", 9, "bold"),
            fg=TEXT_SECONDARY,
            bg=BG_PANEL
        ).pack(anchor="w", pady=(0, 4))

        self.src_combo = ttk.Combobox(
            src_box,
            values=self.sorted_names,
            state="readonly",
            style="Dark.TCombobox",
            font=("Segoe UI", 10)
        )
        self.src_combo.set("Auto Detect")
        self.src_combo.pack(fill=tk.X)

        # Swap Button
        swap_btn = tk.Button(
            lang_bar,
            text="⇄",
            font=("Segoe UI", 14, "bold"),
            fg=TEXT_PRIMARY,
            bg=BG_SURFACE,
            activebackground=BG_SURFACE_HOVER,
            activeforeground=ACCENT_CYAN,
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=2,
            command=self._swap_languages
        )
        swap_btn.pack(side=tk.LEFT, padx=16, pady=(16, 0))

        # Target Language Selector
        tgt_box = tk.Frame(lang_bar, bg=BG_PANEL)
        tgt_box.pack(side=tk.LEFT, expand=True, fill=tk.X)

        tk.Label(
            tgt_box,
            text="Translate into:",
            font=("Segoe UI", 9, "bold"),
            fg=TEXT_SECONDARY,
            bg=BG_PANEL
        ).pack(anchor="w", pady=(0, 4))

        self.tgt_combo = ttk.Combobox(
            tgt_box,
            values=self.target_names,
            state="readonly",
            style="Dark.TCombobox",
            font=("Segoe UI", 10)
        )
        self.tgt_combo.set("Spanish")
        self.tgt_combo.pack(fill=tk.X)

        # Translation Text Panels (Dual Box Layout)
        panels_frame = tk.Frame(main_container, bg=BG_DARK)
        panels_frame.pack(fill=tk.BOTH, expand=True)
        panels_frame.columnconfigure(0, weight=1)
        panels_frame.columnconfigure(1, weight=1)
        panels_frame.rowconfigure(0, weight=1)

        # Left: Source Text Card
        left_card = tk.Frame(panels_frame, bg=BG_PANEL, padx=14, pady=12, highlightbackground=BORDER_COLOR, highlightthickness=1)
        left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        left_card_hdr = tk.Frame(left_card, bg=BG_PANEL)
        left_card_hdr.pack(fill=tk.X, pady=(0, 6))

        tk.Label(
            left_card_hdr,
            text="SOURCE TEXT",
            font=("Segoe UI", 9, "bold"),
            fg=TEXT_SECONDARY,
            bg=BG_PANEL
        ).pack(side=tk.LEFT)

        self.src_char_lbl = tk.Label(
            left_card_hdr,
            text="0 chars",
            font=("Segoe UI", 8),
            fg=TEXT_SECONDARY,
            bg=BG_PANEL
        )
        self.src_char_lbl.pack(side=tk.RIGHT)

        self.src_text = tk.Text(
            left_card,
            bg=BG_SURFACE,
            fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY,
            selectbackground=ACCENT_PRIMARY,
            font=("Segoe UI", 11),
            wrap=tk.WORD,
            relief="flat",
            padx=10,
            pady=10,
            undo=True
        )
        self.src_text.pack(fill=tk.BOTH, expand=True)

        # Left Toolbar (Clear & Speak Original)
        left_toolbar = tk.Frame(left_card, bg=BG_PANEL, pady=6)
        left_toolbar.pack(fill=tk.X)

        speak_src_btn = tk.Button(
            left_toolbar,
            text="🔊 Listen",
            font=("Segoe UI", 9),
            fg=TEXT_PRIMARY,
            bg=BG_SURFACE,
            activebackground=BG_SURFACE_HOVER,
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=3,
            command=lambda: self._speak_text(self.src_text.get("1.0", tk.END).strip())
        )
        speak_src_btn.pack(side=tk.LEFT, padx=(0, 6))

        clear_btn = tk.Button(
            left_toolbar,
            text="🗑 Clear",
            font=("Segoe UI", 9),
            fg=TEXT_SECONDARY,
            bg=BG_SURFACE,
            activebackground=BG_SURFACE_HOVER,
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=3,
            command=self._clear_all
        )
        clear_btn.pack(side=tk.LEFT)

        # Right: Target Text Card
        right_card = tk.Frame(panels_frame, bg=BG_PANEL, padx=14, pady=12, highlightbackground=BORDER_COLOR, highlightthickness=1)
        right_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        right_card_hdr = tk.Frame(right_card, bg=BG_PANEL)
        right_card_hdr.pack(fill=tk.X, pady=(0, 6))

        tk.Label(
            right_card_hdr,
            text="TRANSLATED TEXT",
            font=("Segoe UI", 9, "bold"),
            fg=ACCENT_CYAN,
            bg=BG_PANEL
        ).pack(side=tk.LEFT)

        self.detected_lang_badge = tk.Label(
            right_card_hdr,
            text="",
            font=("Segoe UI", 8, "bold"),
            fg=ACCENT_GREEN,
            bg=BG_SURFACE,
            padx=6,
            pady=2
        )
        self.detected_lang_badge.pack(side=tk.RIGHT)

        self.tgt_text = tk.Text(
            right_card,
            bg=BG_SURFACE,
            fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY,
            selectbackground=ACCENT_PRIMARY,
            font=("Segoe UI", 11),
            wrap=tk.WORD,
            relief="flat",
            padx=10,
            pady=10
        )
        self.tgt_text.pack(fill=tk.BOTH, expand=True)

        # Right Toolbar (Copy & Speak Translated)
        right_toolbar = tk.Frame(right_card, bg=BG_PANEL, pady=6)
        right_toolbar.pack(fill=tk.X)

        self.copy_btn = tk.Button(
            right_toolbar,
            text="📋 Copy Translation",
            font=("Segoe UI", 9, "bold"),
            fg=TEXT_PRIMARY,
            bg=BG_SURFACE,
            activebackground=BG_SURFACE_HOVER,
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=3,
            command=self._copy_translation
        )
        self.copy_btn.pack(side=tk.LEFT, padx=(0, 6))

        speak_tgt_btn = tk.Button(
            right_toolbar,
            text="🔊 Listen",
            font=("Segoe UI", 9),
            fg=TEXT_PRIMARY,
            bg=BG_SURFACE,
            activebackground=BG_SURFACE_HOVER,
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=3,
            command=lambda: self._speak_text(self.tgt_text.get("1.0", tk.END).strip())
        )
        speak_tgt_btn.pack(side=tk.LEFT)

        # Primary Action Bar (Translate Button)
        action_bar = tk.Frame(main_container, bg=BG_DARK, pady=12)
        action_bar.pack(fill=tk.X)

        self.translate_btn = tk.Button(
            action_bar,
            text="⚡ Translate Text (Ctrl + Enter)",
            font=("Segoe UI", 11, "bold"),
            fg="#FFFFFF",
            bg=ACCENT_PRIMARY,
            activebackground=ACCENT_HOVER,
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            padx=24,
            pady=9,
            command=self._start_translation_thread
        )
        self.translate_btn.pack(side=tk.RIGHT)

        # Bottom Status Bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready • Select languages and type text to begin translation.",
            font=("Segoe UI", 9),
            fg=TEXT_SECONDARY,
            bg=BG_PANEL,
            anchor="w",
            padx=16,
            pady=6
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _bind_events(self):
        self.src_text.bind("<KeyRelease>", self._update_char_count)
        self.root.bind("<Control-Return>", lambda e: self._start_translation_thread())
        self.root.bind("<Control-s>", lambda e: self._swap_languages())

    def _update_char_count(self, event=None):
        text = self.src_text.get("1.0", tk.END).strip()
        count = len(text)
        words = len(text.split()) if count > 0 else 0
        self.src_char_lbl.config(text=f"{count} chars • {words} words")

    def _on_sample_selected(self, event=None):
        selected = self.sample_combo.get()
        if selected and not selected.startswith("--"):
            self.src_text.delete("1.0", tk.END)
            self.src_text.insert("1.0", selected)
            self._update_char_count()
            self._start_translation_thread()

    def _swap_languages(self):
        current_src = self.src_combo.get()
        current_tgt = self.tgt_combo.get()

        if current_src == "Auto Detect":
            # If source was auto, swap target into source and default target to English
            self.src_combo.set(current_tgt)
            self.tgt_combo.set("English")
        else:
            self.src_combo.set(current_tgt)
            self.tgt_combo.set(current_src)

        # Also swap texts if both exist
        src_val = self.src_text.get("1.0", tk.END).strip()
        tgt_val = self.tgt_text.get("1.0", tk.END).strip()
        if tgt_val:
            self.src_text.delete("1.0", tk.END)
            self.src_text.insert("1.0", tgt_val)
            self.tgt_text.delete("1.0", tk.END)
            self.tgt_text.insert("1.0", src_val)
            self._update_char_count()

        self.status_bar.config(text="Languages swapped.")

    def _copy_translation(self):
        translated = self.tgt_text.get("1.0", tk.END).strip()
        if not translated:
            self.status_bar.config(text="Nothing to copy yet.")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(translated)
        self.root.update()

        # Visual feedback on copy button
        original_text = self.copy_btn.cget("text")
        self.copy_btn.config(text="✓ Copied!", fg=ACCENT_GREEN)
        self.status_bar.config(text="Translated text copied to clipboard successfully.")
        self.root.after(1800, lambda: self.copy_btn.config(text=original_text, fg=TEXT_PRIMARY))

    def _speak_text(self, text_to_speak: str):
        """Speaks text asynchronously using Windows SAPI."""
        if not text_to_speak:
            self.status_bar.config(text="No text available to pronounce.")
            return

        def worker():
            self.status_bar.config(text="Speaking audio...")
            # Sanitize speech text for PowerShell single quotes
            clean_speech = text_to_speak[:250].replace("'", "''")
            ps_cmd = (
                f"Add-Type -AssemblyName System.Speech; "
                f"$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                f"$s.Speak('{clean_speech}')"
            )
            subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True)
            self.status_bar.config(text="Speech playback finished.")

        threading.Thread(target=worker, daemon=True).start()

    def _clear_all(self):
        self.src_text.delete("1.0", tk.END)
        self.tgt_text.delete("1.0", tk.END)
        self.detected_lang_badge.config(text="")
        self._update_char_count()
        self.status_bar.config(text="Cleared all text.")

    def _start_translation_thread(self):
        text = self.src_text.get("1.0", tk.END).strip()
        if not text:
            self.status_bar.config(text="Please enter or paste some text to translate.")
            return

        src_name = self.src_combo.get()
        tgt_name = self.tgt_combo.get()

        src_code = self.lang_name_to_code.get(src_name, "auto")
        tgt_code = self.lang_name_to_code.get(tgt_name, "es")

        # Disable button and update UI
        self.translate_btn.config(text="⏳ Translating...", state=tk.DISABLED)
        self.status_bar.config(text=f"Translating from {src_name} to {tgt_name}...")

        threading.Thread(
            target=self._perform_translation,
            args=(text, src_code, tgt_code),
            daemon=True
        ).start()

    def _perform_translation(self, text: str, src_code: str, tgt_code: str):
        start_time = time.time()
        result = translate_text(text, source_lang=src_code, target_lang=tgt_code)
        elapsed = round(time.time() - start_time, 2)

        def update_gui():
            self.translate_btn.config(text="⚡ Translate Text (Ctrl + Enter)", state=tk.NORMAL)
            if result.get("success"):
                translated = result.get("translated_text", "")
                self.tgt_text.delete("1.0", tk.END)
                self.tgt_text.insert("1.0", translated)

                detected = result.get("detected_lang")
                detected_name = LANGUAGES.get(detected, detected)
                if detected and self.src_combo.get() == "Auto Detect":
                    self.detected_lang_badge.config(text=f"Detected: {detected_name}")
                else:
                    self.detected_lang_badge.config(text="")

                provider = result.get("provider", "API")
                self.status_bar.config(
                    text=f"✓ Translation complete ({elapsed}s) via {provider} • {len(translated)} chars generated."
                )
            else:
                err_msg = result.get("error", "Translation failed.")
                messagebox.showerror("Translation Error", err_msg)
                self.status_bar.config(text=f"Error: {err_msg}")

        self.root.after(0, update_gui)

def main():
    root = tk.Tk()
    app = TranslatorGUIApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
