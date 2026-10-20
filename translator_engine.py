"""
CodeAlpha Artificial Intelligence Internship - Task 1: Language Translation Tool
Translator Engine Module
Handles API communication, language detection, and fallbacks.
"""

import urllib.parse
import urllib.request
import json
import logging
from typing import Dict, Any, Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Comprehensive mapping of ISO language codes to English names
LANGUAGES: Dict[str, str] = {
    "auto": "Auto Detect",
    "af": "Afrikaans",
    "sq": "Albanian",
    "am": "Amharic",
    "ar": "Arabic",
    "hy": "Armenian",
    "as": "Assamese",
    "az": "Azerbaijani",
    "eu": "Basque",
    "be": "Belarusian",
    "bn": "Bengali",
    "bs": "Bosnian",
    "bg": "Bulgarian",
    "ca": "Catalan",
    "ceb": "Cebuano",
    "zh-CN": "Chinese (Simplified)",
    "zh-TW": "Chinese (Traditional)",
    "co": "Corsican",
    "hr": "Croatian",
    "cs": "Czech",
    "da": "Danish",
    "nl": "Dutch",
    "en": "English",
    "eo": "Esperanto",
    "et": "Estonian",
    "fi": "Finnish",
    "fr": "French",
    "fy": "Frisian",
    "gl": "Galician",
    "ka": "Georgian",
    "de": "German",
    "el": "Greek",
    "gu": "Gujarati",
    "ht": "Haitian Creole",
    "ha": "Hausa",
    "haw": "Hawaiian",
    "he": "Hebrew",
    "hi": "Hindi",
    "hmn": "Hmong",
    "hu": "Hungarian",
    "is": "Icelandic",
    "ig": "Igbo",
    "id": "Indonesian",
    "ga": "Irish",
    "it": "Italian",
    "ja": "Japanese",
    "jv": "Javanese",
    "kn": "Kannada",
    "kk": "Kazakh",
    "km": "Khmer",
    "rw": "Kinyarwanda",
    "ko": "Korean",
    "ku": "Kurdish",
    "ky": "Kyrgyz",
    "lo": "Lao",
    "la": "Latin",
    "lv": "Latvian",
    "lt": "Lithuanian",
    "lb": "Luxembourgish",
    "mk": "Macedonian",
    "mg": "Malagasy",
    "ms": "Malay",
    "ml": "Malayalam",
    "mt": "Maltese",
    "mi": "Maori",
    "mr": "Marathi",
    "mn": "Mongolian",
    "my": "Myanmar (Burmese)",
    "ne": "Nepali",
    "no": "Norwegian",
    "ny": "Nyanja (Chichewa)",
    "or": "Odia (Oriya)",
    "ps": "Pashto",
    "fa": "Persian",
    "pl": "Polish",
    "pt": "Portuguese",
    "pa": "Punjabi",
    "ro": "Romanian",
    "ru": "Russian",
    "sm": "Samoan",
    "gd": "Scots Gaelic",
    "sr": "Serbian",
    "st": "Sesotho",
    "sn": "Shona",
    "sd": "Sindhi",
    "si": "Sinhala (Sinhalese)",
    "sk": "Slovak",
    "sl": "Slovenian",
    "so": "Somali",
    "es": "Spanish",
    "su": "Sundanese",
    "sw": "Swahili",
    "sv": "Swedish",
    "tl": "Tagalog (Filipino)",
    "tg": "Tajik",
    "ta": "Tamil",
    "tt": "Tatar",
    "te": "Telugu",
    "th": "Thai",
    "tr": "Turkish",
    "tk": "Turkmen",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "ug": "Uyghur",
    "uz": "Uzbek",
    "vi": "Vietnamese",
    "cy": "Welsh",
    "xh": "Xhosa",
    "yi": "Yiddish",
    "yo": "Yoruba",
    "zu": "Zulu"
}

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

def _google_translate_request(text: str, source_lang: str, target_lang: str) -> Tuple[str, str]:
    """
    Calls Google Translate public endpoint.
    Returns (translated_text, detected_source_language_code).
    """
    encoded_text = urllib.parse.quote(text)
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_lang}&tl={target_lang}&dt=t&dt=bd&dt=rm&q={encoded_text}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    with urllib.request.urlopen(req, timeout=10) as response:
        content = response.read().decode("utf-8")
        data = json.loads(content)

        translated_parts = []
        if data and isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
            for item in data[0]:
                if item and isinstance(item, list) and len(item) > 0 and item[0]:
                    translated_parts.append(str(item[0]))

        translated_text = "".join(translated_parts).strip()
        detected_lang = source_lang
        if len(data) > 2 and isinstance(data[2], str):
            detected_lang = data[2]

        return translated_text, detected_lang

def _mymemory_translate_request(text: str, source_lang: str, target_lang: str) -> str:
    """
    Calls MyMemory Translated API as reliable fallback.
    """
    src = "en" if source_lang == "auto" else source_lang
    encoded_text = urllib.parse.quote(text)
    url = f"https://api.mymemory.translated.net/get?q={encoded_text}&langpair={src}|{target_lang}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    with urllib.request.urlopen(req, timeout=10) as response:
        content = response.read().decode("utf-8")
        data = json.loads(content)
        if "responseData" in data and "translatedText" in data["responseData"]:
            return data["responseData"]["translatedText"]
        raise RuntimeError("Unexpected response structure from MyMemory API")

def translate_text(text: str, source_lang: str = "auto", target_lang: str = "es") -> Dict[str, Any]:
    """
    Translates input text from source_lang to target_lang.
    Uses Google Translate API primarily, with MyMemory API as automatic fallback.
    """
    clean_text = text.strip() if text else ""
    if not clean_text:
        return {
            "success": False,
            "error": "Input text cannot be empty.",
            "translated_text": ""
        }

    src = source_lang.strip() if source_lang else "auto"
    tgt = target_lang.strip() if target_lang else "en"

    # Attempt 1: Google Translate API
    try:
        translated_text, detected_lang = _google_translate_request(clean_text, src, tgt)
        if translated_text:
            return {
                "success": True,
                "translated_text": translated_text,
                "source_lang": src,
                "detected_lang": detected_lang,
                "target_lang": tgt,
                "source_name": LANGUAGES.get(detected_lang, detected_lang),
                "target_name": LANGUAGES.get(tgt, tgt),
                "provider": "Google Translate API"
            }
    except Exception as e:
        logger.warning(f"Google Translate API failed: {e}. Trying MyMemory fallback...")

    # Attempt 2: MyMemory API Fallback
    try:
        fallback_translated = _mymemory_translate_request(clean_text, src, tgt)
        if fallback_translated:
            return {
                "success": True,
                "translated_text": fallback_translated,
                "source_lang": src,
                "detected_lang": src if src != "auto" else "en",
                "target_lang": tgt,
                "source_name": LANGUAGES.get(src, src),
                "target_name": LANGUAGES.get(tgt, tgt),
                "provider": "MyMemory API (Fallback)"
            }
    except Exception as e:
        logger.error(f"MyMemory API fallback failed: {e}")

    return {
        "success": False,
        "error": "Translation service is currently unreachable. Please check your internet connection and try again.",
        "translated_text": ""
    }

def detect_language(text: str) -> Dict[str, Any]:
    """
    Detects language of provided text.
    """
    result = translate_text(text, source_lang="auto", target_lang="en")
    if result.get("success"):
        detected_code = result.get("detected_lang", "unknown")
        return {
            "success": True,
            "language_code": detected_code,
            "language_name": LANGUAGES.get(detected_code, "Unknown")
        }
    return {
        "success": False,
        "error": result.get("error", "Detection failed")
    }

def get_supported_languages() -> Dict[str, str]:
    """
    Returns dictionary of supported languages.
    """
    return LANGUAGES

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    sample = "Artificial Intelligence is transforming the future of technology."
    print("Testing Translation Engine...")
    print(f"Original Text: {sample}")
    
    res_es = translate_text(sample, "en", "es")
    print(f"\nSpanish: {res_es.get('translated_text')} (Provider: {res_es.get('provider')})")
    
    res_hi = translate_text(sample, "auto", "hi")
    print(f"Hindi: {res_hi.get('translated_text')} (Detected: {res_hi.get('detected_lang')})")
    
    res_fr = translate_text(sample, "auto", "fr")
    print(f"French: {res_fr.get('translated_text')}")
