import os

lang_files = {}
languages_info = []
default_lang = 'en_US'
lang_files_dir = ''


def load_lang_file(lang) -> dict:
    lang_dictionary = {}
    lang_path = f"{lang_files_dir}/{lang}.lang"

    if not os.path.isfile(lang_path):
        for root, dirs, files in os.walk(lang_files_dir):
            for file in files:
                if file.endswith(".lang") and file.startswith(lang):
                    lang_path = os.path.join(lang_files_dir, file)
                    break
            if lang_path != os.path.join(lang_files_dir, f"{lang}.lang"):
                break

    with open(lang_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith(("//", "#")):
                try:
                    key, value = line.split("=", 1)
                    lang_dictionary[key.strip()] = value.strip()
                except ValueError as e:
                    raise ValueError(f'Invalid line format: {line}') from e

    return lang_dictionary


def get_language(lang=None) -> str:
    if lang is None:
        lang = default_lang
    
    for available_lang in lang_files:
        if available_lang.lower().startswith(lang.lower()):
            return available_lang
    
    return default_lang

def language_exists(lang=None) -> bool:
    return get_language(lang) in lang_files

def set_default_language(lang: str) -> None:
    global default_lang
    if language_exists(lang):
        default_lang = lang
    else:
        raise ValueError(f"Language '{lang}' does not exist. Default language remains '{default_lang}'.")

def load_all_lang_files() -> dict:
    lang_files = {}
    for root, dirs, files in os.walk("webdeck/translations"):
        for file in files:
            if file.endswith(".lang"):
                lang = file.split(".")[0]
                lang_files[lang] = load_lang_file(lang)
    return lang_files

def reload_all_lang_files() -> None:
    global lang_files
    lang_files = load_all_lang_files()
    
def get_languages_info(lang_files=lang_files) -> list:
    if not lang_files:
        lang_files = load_all_lang_files()
    
    languages_info = []
    for lang, lang_data in lang_files.items():
        languages_info.append({
            'code': lang,
            'code_short': lang_data['lang_code'],
            'native_name': lang_data['lang_name'],
            'credits': lang_data['credits'],
        })
    
    return languages_info

def init(lang_files_directory=None, default_language=None):
    global languages_info, default_lang, lang_files_dir
    
    if lang_files_directory is None:
        raise ValueError("'lang_files_directory' must be specified")
    
    lang_files_dir = lang_files_directory
    default_language = default_language or default_lang
    
    reload_all_lang_files()
    set_default_language(default_language)
    
    languages_info = get_languages_info()
    
    return languages_info

def text(text=None, lang=None) -> str:
    global default_lang
    lang = get_language(lang or default_lang)
    
    if text is None:
        return ""

    if lang not in lang_files:
        raise KeyError(f"Language '{lang}' not found in lang_files")
    
    return lang_files[lang].get(text, text)