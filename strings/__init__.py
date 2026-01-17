import os
from typing import Dict

import yaml

languages: Dict[str, dict] = {}
languages_present: Dict[str, str] = {}


def get_string(lang: str) -> dict:
    # fallback to english if lang missing
    return languages.get(lang) or languages.get("en") or {}


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LANG_DIR = os.path.join(BASE_DIR, "langs")
EN_FILE = os.path.join(LANG_DIR, "en.yml")


def _load_yaml(path: str) -> dict:
    try:
        with open(path, encoding="utf8") as f:
            data = yaml.safe_load(f) or {}
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


# Load English first (must exist)
languages["en"] = _load_yaml(EN_FILE)
languages_present["en"] = languages["en"].get("name", "English")

# Load other languages
try:
    for filename in os.listdir(LANG_DIR):
        if not filename.endswith(".yml"):
            continue

        language_name = filename[:-4]
        if language_name == "en":
            continue

        lang_path = os.path.join(LANG_DIR, filename)
        languages[language_name] = _load_yaml(lang_path)

        # Fill missing keys from English
        for key, val in languages["en"].items():
            if key not in languages[language_name]:
                languages[language_name][key] = val

        # Register language display name
        languages_present[language_name] = languages[language_name].get("name", language_name)

except Exception as e:
    # Don't crash bot because of language files
    print(f"There is some issue with the language file inside bot: {e}")
