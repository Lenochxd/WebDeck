from webdeck_custom_module import *

import base64

# First, we define the add on.
webdeck = WebDeckAddon("MyAddOnName")

# We define the first button.
command1 = webdeck.define_command(name='Print in Console', description='Print something in the developer console')
command1.button.button_names.en = "A Print Button"
command1.button.button_names.fr = "Un Bouton Pour Print"
command1.button.image = "print_icon.png"


# When the button is pressed:
@command1.make
def printer():
    print(text)

#############

# We define the second button (you can create buttons as many as you want).
command2 = webdeck.define_command(name='Base64 Converter', description='Convert text to base64')
command2.button.button_names.en = "Encode to base64"
command2.button.button_names.fr = "Encoder en base64"
command2.button.image = "base_64_icon.png"

def encode_to_base64(string_to_encode):

    """
    This function takes string as input and returns its Base64 encoded representation.
    
    Args:
        string_to_encode (str): The string to encode.
        
    Returns:
        str: Encoded string.
    """

    encoded_bytes = base64.b64encode(string_to_encode.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string



@command2.make
def base_64_encoder(text: INPUT_TYPE.text = ArgNames(en='Text to encode in base 64 and print into the developer console', fr="Texte à encoder en base 64 a et print dans la console")):
    print(encode_to_base64(text))

#############
    

command3 = webdeck.define_command(name='Example name', description='Example description')
command3.button.button_names.en = "Example english button name"
command3.button.image = "example_icon.png"

@command3.make
def example_button(arg: str = ArgChoice(
        (INPUT_TYPE.NONE, ArgNames(en='A none choice')),
        (INPUT_TYPE.text, ArgNames(en='A text choice')),
        ArgNames = ArgNames(en='Choose between None and a text choice')
    )):
    ...