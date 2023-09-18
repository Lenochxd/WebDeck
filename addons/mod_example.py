from webdeck_custom_module import *

webdeck = WebDeckAddon("MyMod")
command1 = webdeck.define_command(name='My command', description='Command for doing something')
command1.button.button_names.en = "Do the thing"
command1.button.image = "image.png"
@command1.make
def my_command( #webdeck:Screen,
               text: INPUT_TYPE.text = ArgNames(en='A text choice'),
               a_number: INPUT_TYPE.number[1:3] = ArgNames(en='A nunber between 1 and 3'),
               b_number: INPUT_TYPE.number[2, 10] = ArgNames(en='A nunber between 2 and 10')):
    ...



command2 = webdeck.define_command(name='My j', description='Command jj')
command2.button.button_names.en = "Do jjj"
command2.button.image = "image.png"
@command2.make
def j(arg: str = ArgChoice(
        (INPUT_TYPE.NONE, ArgNames(en='A none choice')),
        (INPUT_TYPE.text, ArgNames(en='A text choice')),
        ArgNames = ArgNames(en='Choose between None and a text choice')
    )):
    ...

