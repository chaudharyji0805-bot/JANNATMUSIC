\import os
from typing import List

import yaml

languages = {}
languages_present = {}


def get_string(lang: str):
    return languages.get(lang, languages["en"])


LANG_PATH = "./strings/langs/"


# Load English first (base language)
try:
    languages["en"] = yaml.safe_load(
        open(f"{LANG_PATH}en.yml", encoding="utf8")
    )
    languages_present["en"] = languages["en"]["name"]
except Exception as e:
    print(f"[LANG ERROR] Failed to load en.yml : {e}")
    exit()


for filename in os.listdir(LANG_PATH):

    if not filename.endswith(".yml"):
        continue

    language_name = filename[:-4]

    if language_name == "en":
        continue

    try:
        languages[language_name] = yaml.safe_load(
            open(LANG_PATH + filename, encoding="utf8")
        )

        # Fill missing keys from English
        for item in languages["en"]:
            if item not in languages[language_name]:
                languages[language_name][item] = languages["en"][item]

        # Save language display name
        languages_present[language_name] = languages[language_name]["name"]

    except Exception as e:
        print(f"[LANG ERROR] Issue in {filename} : {e}")
        print("Skipping this language file and continuing...")
        continue
