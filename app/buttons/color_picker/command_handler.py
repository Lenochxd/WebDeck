import json
import pyperclip


from app.utils.logger import log
from app.utils.translate import translate
from .get_arg import getarg
from .get_color_name import get_color_name
from .get_mouse_pixel_color import get_mouse_pixel_color
from .notification import toast



def handle_command(message):
    # TODO: rewrite
    color = get_mouse_pixel_color()

    target_language = getarg(message, "lang")
    selectedtypes = getarg(message, "type")
    typestocopy = getarg(message, "copy")
    copy_type = getarg(message, "copy_type")
    display_type = getarg(message, "display_type")
    try:
        remove_hex_sharp = getarg(message, "remove_hex_sharp").capitalize()
    except AttributeError:
        remove_hex_sharp = None

    log.debug(
        f"------------------------------------------\n"
        f"{color}\n"
        f"------------------------------------------\n"
        f"{target_language}\n"
        f"{selectedtypes}\n"
        f"{typestocopy}\n"
        f"{copy_type}\n"
        f"{display_type}\n"
        f"{remove_hex_sharp}\n"
        f"------------------------------------------"
    )

    with open("webdeck/colors.json", "r", encoding="utf-8") as f:
        colorsjson = json.load(f)

    color_name_original = get_color_name(color['hex'], colorsjson)
    color_name = color_name_original
    if not target_language is None or target_language == "en":
        color_name = translate(color_name, target_language)

    color_names = {
        "NAME": color_name,
        "TEXT": color_name,
        "NAME-ORIGINAL": color_name_original,
        "TEXT-ORIGINAL": color_name_original,
        "HEX": color['hex'],
        "RGB": color['rgb'],
        "HSL": color['hsl'],
    }

    color_names_final = {}
    if selectedtypes:
        for type in selectedtypes.split(";"):
            for type_found, value in color_names.items():
                if type.upper() in type_found:
                    if "HEX" in type.upper() and remove_hex_sharp == "True":
                        color_names_final[type.upper()] = value.replace("#", "")
                    else:
                        color_names_final[type.upper()] = value
    else:
        for type_found, value in color_names.items():
            if all(elem not in type_found for elem in ["TEXT", "ORIGINAL"]):
                color_names_final[type_found] = value

    if typestocopy:
        # FIXME: WHAT THE FUCK IS THIS
        # copy:text;hex;rgb;hsl copy_type:raw|list
        typestocopy_final = {}
        for type in typestocopy.split(";"):
            for type_found, value in color_names.items():
                if type.upper() in type_found:
                    if "HEX" in type.upper() and remove_hex_sharp == "True":
                        typestocopy_final[type.upper()] = value.replace("#", "")
                    else:
                        typestocopy_final[type.upper()] = value
        if copy_type.lower() == "list":
            if len(typestocopy.split(";")) == 1:
                pyperclip.copy(str(typestocopy_final)[:-2][2:].replace("'", ""))
            else:
                pyperclip.copy(
                    str(typestocopy_final)
                    .replace("', ", ",\n")[:-2][2:]
                    .replace("'", "")
                )
        elif len(typestocopy.split(";")) == 1:
            pyperclip.copy(list(typestocopy_final.values())[0])
        else:
            pyperclip.copy(", ".join(typestocopy_final.values()))

    toast(display_type, typestocopy, color_names_final)