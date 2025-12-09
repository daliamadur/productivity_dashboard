from PIL import Image, ImageColor
from customtkinter import CTkImage
from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent

def hex_to_rgb(code):
    return ImageColor.getcolor(code, "RGBA")

def recolor_image(image, color):
    #iterate through pixels and change colour values
    pixel_map = image.convert("RGBA")
    w, h = image.size

    for x in range(w):
        for y in range(h):
            _, _, _, alpha = image.getpixel((x, y))

            if alpha != 0:
                image.putpixel((x, y), hex_to_rgb(color))
    return image

def resolve_icon_path(path_str):
    return BASE_DIR / path_str

#category e.g. tabs, name e.g. home
def load_icon(name, size = 20, category=None):
    with open(BASE_DIR / "assets_icons.yaml", "r", encoding="utf-8") as icons_file:
        icons = yaml.safe_load(icons_file)
    
    path = resolve_icon_path(icons[category][name]['path']) if category else resolve_icon_path(icons[name]['path'])
    icon_color_light = icons[category][name]['light_color'] if category else icons[name]['light_color']
    icon_color_dark = icons[category][name]['dark_color'] if category else icons[name]['dark_color']

    img = Image.open(path).resize((size, size))

    return CTkImage(light_image=recolor_image(img, icon_color_light), 
                    dark_image=recolor_image(img, icon_color_dark),
                    size=(size, size))