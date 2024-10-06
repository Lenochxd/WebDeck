from sys import platform
if platform == 'win32':
    from win10toast import ToastNotifier
    toaster = ToastNotifier()


def toast(display_type, typestocopy, color_names_final):
    if platform != 'win32':
        return
    icon = "static\\icons\\icon.ico"
    duration = 5
    message = ""
    if display_type and display_type.lower() != "list":
        message = (
            list(color_names_final.values())[0]
            if typestocopy and len(typestocopy.split(";")) == 1
            else ", ".join(color_names_final.values())
        )
    elif typestocopy and len(typestocopy.split(";")) == 1:
        message = str(color_names_final)[:-2][2:].replace("'", "")
    else:
        message = (
            str(color_names_final)
            .replace("', ", ",\n")[:-2][2:]
            .replace("'", "")
        )

    title = "WebDeck Color Picker"
    toaster.show_toast(
        title, message, icon_path=icon, duration=duration, threaded=True
    )