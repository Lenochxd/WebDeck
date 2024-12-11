import customtkinter as ctk
from PIL import Image, ImageTk

from .settings.get_config import get_config, save_config
from .platform import is_windows
from .logger import log
from .languages import text


def show_popup():
    config = get_config()
    if not config["settings"].get("show_popup", True):
        return
    
    # Create a popup window
    try:
        popup = ctk.CTk()
    except Exception as e:
        log.exception(e, message="Failed to create popup window. Skipping welcome message.", print_log=False)
        return
    popup.wm_title(text("welcome_message_window_title"))
    popup.configure(bg='black')
    try:
        if is_windows:
            popup.iconbitmap('./static/icons/icon.ico')
        else:
            logo_image = Image.open("./static/icons/icon.ico")
            logo_photo = ImageTk.PhotoImage(logo_image)
            popup.iconphoto(True, logo_photo)
    except Exception as e:
        log.exception(e, message="Failed to set window icon.", print_log=False)
    popup.geometry("450x220")
    popup.resizable(False, False)

    # Position the window in the bottom right corner
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    x = screen_width - (450+50)
    y = screen_height - (220+100)
    popup.geometry(f"450x220+{x}+{y}")

    # Add the WebDeck logo
    logo_image = Image.open("static/img/webdeck.png")
    logo = ctk.CTkImage(logo_image, size=(373, 78))  # Reduce size to 50%
    logo_label = ctk.CTkLabel(popup, image=logo, text="")
    logo_label.pack(side="top", pady=(20, 10))

    label_text_1 = text("welcome_message_label_1")
    label_text_2 = text("welcome_message_label_2")
    label = ctk.CTkLabel(
        popup,
        text=f"{label_text_1}\n {label_text_2}",
        text_color='white'
    )
    label.pack(side="top", fill="x", pady=10)

    def disable_message():
        log.info("Disabling popup message")
        config["settings"]["show_popup"] = False
        save_config(config)
        popup.destroy()

    def ok():
        popup.destroy()

    # Create a frame to center the buttons
    button_frame = ctk.CTkFrame(popup, fg_color=popup.cget("fg_color"))
    button_frame.pack(side="bottom", pady=10)

    disable_button = ctk.CTkButton(button_frame, text=text("welcome_message_button_dont_show_again"), command=disable_message)
    disable_button.pack(side="left", padx=10)

    ok_button = ctk.CTkButton(button_frame, text=text("welcome_message_button_ok"), command=ok)
    ok_button.pack(side="right", padx=10)

    popup.mainloop()
