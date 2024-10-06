import webcolors

def get_color_name(hex_code, colors):
    try:
        # Finding the exact color in the JSON file
        for color in colors:
            if color["hex_code"] == hex_code:
                return color["name"]

        # If the exact color is not found, search for the closest color
        closest_color = None
        min_distance = float("inf")
        for color in colors:
            rgb1 = webcolors.hex_to_rgb(hex_code)
            rgb2 = webcolors.hex_to_rgb(color["hex_code"])
            distance = sum((a - b) ** 2 for a, b in zip(rgb1, rgb2))
            if distance < min_distance:
                min_distance = distance
                closest_color = color

        return closest_color["name"]
    except ValueError:
        return "Can not find color"