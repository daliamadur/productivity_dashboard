from PIL import Image, ImageColor
from customtkinter import CTkImage
from pathlib import Path
import yaml

class HoverImage(CTkImage):
    def __init__(self, img, light_color, light_hover_color, dark_color, dark_hover_color, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs
        )
        self.img = img
        self.light_color = light_color
        self.light_hover_color = light_hover_color 
        self.dark_color = dark_color
        self.dark_hover_color = dark_hover_color

BASE_DIR = Path(__file__).resolve().parent.parent

def hex_to_rgba(code):
    return ImageColor.getcolor(code, "RGBA")

def rgba_to_hex(rgba):
    r, g, b, a = rgba
    return "#{:02x}{:02x}{:02x}{:02x}".format(r, g, b, a)

def recolor_image(image, color):
    #iterate through pixels and change colour values
    pixel_map = image.convert("RGBA")
    w, h = image.size

    for x in range(w):
        for y in range(h):
            _, _, _, alpha = pixel_map.getpixel((x, y))

            if alpha != 0:
                pixel_map.putpixel((x, y), hex_to_rgba(color))
    return pixel_map

def resolve_icon_path(path_str):
    return BASE_DIR / path_str

#category e.g. tabs, name e.g. home
def load_icon(name, size = 20, category=None):
    with open(BASE_DIR / "assets_icons.yaml", "r", encoding="utf-8") as icons_file:
        icons = yaml.safe_load(icons_file)
    
    path = resolve_icon_path(icons[category][name]['path']) if category else resolve_icon_path(icons[name]['path'])
    
    icon_color_light = icons[category][name]['light_color'] if category else icons[name]['light_color']
    icon_color_dark = icons[category][name]['dark_color'] if category else icons[name]['dark_color']
    
    icon_hover_color_light = icons[category][name]['light_hover_color'] if category else icons[name]['light_hover_color']
    icon_hover_color_dark = icons[category][name]['dark_hover_color'] if category else icons[name]['dark_hover_color']

    img = Image.open(path)

    return HoverImage(light_image=recolor_image(img, icon_color_light), 
                    dark_image=recolor_image(img, icon_color_dark),
                    size=(size, size),
                    light_color=icon_color_light,
                    light_hover_color=icon_hover_color_light,
                    dark_color=icon_color_dark,
                    dark_hover_color=icon_hover_color_dark,
                    img=img
                    )

def change_icon_color(icon : HoverImage, hover=False):
    size = icon.cget("size")

    light = icon.light_hover_color if hover else icon.light_color

    dark = icon.dark_hover_color if hover else icon.dark_color

    new_dark_image = recolor_image(icon.img, dark)
    new_light_image = recolor_image(icon.img, light)

    return HoverImage(light_image = new_light_image,
        dark_image = new_dark_image,
        light_color=icon.light_color,
        light_hover_color=icon.light_hover_color,
        dark_color=icon.dark_color,
        dark_hover_color=icon.dark_hover_color,
        img=icon.img,
        size=size
        )

    