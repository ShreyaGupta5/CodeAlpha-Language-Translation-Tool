"""
CodeAlpha Artificial Intelligence Internship - Task 1: Language Translation Tool
Flask Web Application Server
"""

import os
import sys
import webbrowser
import threading
import urllib.parse
import urllib.request
from flask import Flask, render_template, request, jsonify, Response

from translator_engine import (
    translate_text,
    detect_language,
    get_supported_languages,
    LANGUAGES
)

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

@app.route("/")
def index():
    """Renders the primary web user interface."""
    return render_template("index.html")

@app.route("/api/languages", methods=["GET"])
def api_languages():
    """Returns sorted dictionary of supported languages."""
    # Place 'auto' first, followed by remaining languages sorted alphabetically
    languages = get_supported_languages()
    auto_item = {"auto": languages.get("auto", "Auto Detect")}
    sorted_others = dict(sorted(
        [(k, v) for k, v in languages.items() if k != "auto"],
        key=lambda item: item[1]
    ))
    combined = {**auto_item, **sorted_others}
    return jsonify({"success": True, "languages": combined})

@app.route("/api/translate", methods=["POST"])
def api_translate():
    """Translates text between selected source and target languages."""
    try:
        data = request.get_json(force=True, silent=True) or {}
        text = data.get("text", "")
        source_lang = data.get("source_lang", "auto")
        target_lang = data.get("target_lang", "es")

        if not text or not text.strip():
            return jsonify({"success": False, "error": "Please enter text to translate."}), 400

        result = translate_text(text, source_lang=source_lang, target_lang=target_lang)
        return jsonify(result)
    except Exception as exc:
        return jsonify({"success": False, "error": f"Server translation error: {str(exc)}"}), 500

@app.route("/api/detect", methods=["POST"])
def api_detect():
    """Detects the language of the supplied text."""
    try:
        data = request.get_json(force=True, silent=True) or {}
        text = data.get("text", "")
        if not text or not text.strip():
            return jsonify({"success": False, "error": "No text provided for detection."}), 400

        result = detect_language(text)
        return jsonify(result)
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500

@app.route("/api/tts", methods=["GET"])
def api_tts():
    """
    Proxies Google TTS speech audio stream for accurate pronunciation in any language.
    Parameters:
      - text: string to speak
      - lang: language code (e.g. en, es, fr, hi)
    """
    text = request.args.get("text", "").strip()
    lang = request.args.get("lang", "en").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Truncate to 200 characters max for standard TTS chunk
    speech_text = text[:200]
    encoded_text = urllib.parse.quote(speech_text)
    tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={encoded_text}&tl={lang}&client=tw-ob"

    try:
        req = urllib.request.Request(
            tts_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            }
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            audio_data = response.read()
            return Response(audio_data, mimetype="audio/mpeg")
    except Exception as exc:
        return jsonify({"error": f"TTS audio unavailable: {str(exc)}"}), 502

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "CodeAlpha Language Translation Tool"})

def open_browser():
    """Automatically launches default browser once server is running."""
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("=" * 65)
    print("  CodeAlpha AI Internship - TASK 1: Language Translation Tool")
    print("  Web Server running at: http://127.0.0.1:5000")
    print("=" * 65)
    
    # Auto-open browser in background thread
    if os.environ.get("NO_BROWSER") != "1":
        threading.Timer(1.2, open_browser).start()
        
    app.run(host="127.0.0.1", port=port, debug=False)
