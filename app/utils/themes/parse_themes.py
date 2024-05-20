import os

def parse_css_file(text, css_file_path):
    css_data = {}
    with open(css_file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.replace(" ", "").startswith("/*-------"):
                break
            if '=' in line:
                key, value = line.split('=')
                key = key.strip()
                value = value.strip()
                css_data[key.lower()] = value
        for info in [
            "theme-icon",
            "theme-name",
            "theme-description",
            "theme-author-github",
            "page-preview"
        ]:
            if info not in css_data.keys():
                css_data[info] = text["not_specified"]
        
        if css_data["theme-icon"] == "Not specified":
            css_data["theme-icon"] = ""
        if css_data["theme-name"] == text["not_specified"]:
            css_data["theme-name"] = os.path.basename(css_file_path)
        if css_data["theme-description"] == text["not_specified"]:
            css_data["theme-description"] = css_file_path
        if css_data["page-preview"] == "Not specified":
            css_data["page-preview"] = ['all']
        
    return css_data

def parse_themes(text):
    parsed_themes = {}
    for file_name in os.listdir("static/themes/"):
        if file_name.endswith(".css"):
            parsed_themes[file_name] = parse_css_file(text, f"static/themes/{file_name}")
            
    return parsed_themes