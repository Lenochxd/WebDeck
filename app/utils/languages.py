import os
import locale

lang_files = {}
languages_info = []
default_lang = 'en_US'
lang_files_dir = ''
misc_lang_files_dir = ''


def load_lang_file(lang) -> dict:
    lang_dictionary = {}
    lang_path = f"{lang_files_dir}/{lang}.lang"

    if not os.path.isfile(lang_path):
        lang_path = f"{misc_lang_files_dir}/{lang}.lang"
    
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
    if lang is None or lang.lower() == 'system':
        lang = get_system_language()
    
    for available_lang in lang_files:
        if available_lang.lower().startswith(lang.lower()):
            return available_lang
    
    return default_lang

def language_exists(language_code=None) -> bool:
    resolved_language = get_language(language_code)
    if resolved_language.lower() == language_code.lower():
        return resolved_language in lang_files
    
    return False

def set_default_language(lang: str) -> None:
    global default_lang
    if lang.lower() == 'system':
        lang = get_system_language()
    if language_exists(lang):
        default_lang = lang
    else:
        # raise ValueError(f"Language '{lang}' does not exist. Default language remains '{default_lang}'.")
        print(f"Language '{lang}' does not exist. Default language remains '{default_lang}'.")

def load_all_lang_files() -> dict:
    lang_files = {}
    for file in os.listdir(lang_files_dir):
        if file.endswith(".lang"):
            lang = file.split(".")[0]
            lang_files[lang] = load_lang_file(lang)
            lang_files[lang]['misc'] = False

    if misc_lang_files_dir and os.path.isdir(misc_lang_files_dir):
        for file in os.listdir(misc_lang_files_dir):
            if file.endswith(".lang"):
                lang = file.split(".")[0]
                if lang not in lang_files:
                    lang_files[lang] = load_lang_file(lang)
                lang_files[lang]['misc'] = True
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
            'native_name': lang_data['native_name'],
            'english_name': lang_data['english_name'],
            'author_name': lang_data['author_name'],
            'author_github_username': lang_data['author_github_username'],
            'misc': lang_data.get('misc', False),
        })
    
    return languages_info

def get_system_language() -> str:
    """
    Retrieves the system's default language setting.

    Returns:
        str: The system's default language code (e.g., 'en_US'). If the system's default language cannot be determined, returns a default language code.
    """
    system_lang = locale.getdefaultlocale()[0]
    return system_lang if system_lang else default_lang

def init(lang_files_directory=None, misc_lang_files_directory=None, default_language=None):
    global languages_info, default_lang, lang_files_dir, misc_lang_files_dir
    
    if lang_files_directory is None:
        raise ValueError("'lang_files_directory' must be specified")
    
    if not misc_lang_files_directory is None:
        misc_lang_files_dir = misc_lang_files_directory
    
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
        lang = default_lang
        if lang not in lang_files:
            raise KeyError(f"Language '{lang}' not found in lang_files")
        # raise KeyError(f"Language '{lang}' not found in lang_files")
    
    return lang_files[lang].get(text, lang_files.get("en_US", {}).get(text, text))