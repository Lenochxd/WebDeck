try: from deep_translator import GoogleTranslator
except SyntaxError: pass

def translate(word, target_language):
    # Separate words with spaces before each capital letter
    word = "".join([f" {i}" if i.isupper() else i for i in word]).strip()
    
    if word == "Discord" or target_language.upper() == "EN":
        return word
        
    try:
        return GoogleTranslator(source="en", target=target_language).translate(word)
    except NameError:
        return word