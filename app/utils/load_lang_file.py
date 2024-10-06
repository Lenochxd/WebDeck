import os

def load_lang_file(lang):
    lang_dictionary = {}
    lang_path = f"webdeck/translations/{lang}.lang"
    if not os.path.isfile(f"webdeck/translations/{lang}.lang"):
        for root, dirs, files in os.walk("webdeck/translations"):
            for file in files:
                if file.endswith(".lang") and file.startswith(lang):
                    lang_path = f"webdeck/translations/{file}"

    with open(lang_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if (
                line.replace(" ", "").replace("\n", "") != ""
                and not line.startswith("//")
                and not line.startswith("#")
            ):
                try:
                    key, value = line.strip().split("=")
                    lang_dictionary[key] = value.strip()
                except:
                    print(line)
    return lang_dictionary