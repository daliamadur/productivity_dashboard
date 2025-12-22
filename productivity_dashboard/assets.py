from PIL import Image, ImageColor
from customtkinter import CTkImage, CTkBaseClass
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
import yaml

@dataclass
class IconPalette():
    light: str
    light_hover: str
    dark: str
    dark_hover: str

class HoverImage(CTkImage):
    def __init__(self, light_color, light_hover_color, dark_color, dark_hover_color, palette, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs
        )
        self.light_color = light_color
        self.light_hover_color = light_hover_color
        self.dark_color = dark_color
        self.dark_hover_color = dark_hover_color
        self.palette = palette

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
def load_icon(name, size = 20, category=None, hover_image=False):
    with open(BASE_DIR / "assets_icons.yaml", "r", encoding="utf-8") as icons_file:
        icons = yaml.safe_load(icons_file)
    
    path = resolve_icon_path(icons[category][name]['path']) if category else resolve_icon_path(icons[name]['path'])
    
    icon_color_light = icons[category][name]['light_color'] if category else icons[name]['light_color']
    icon_color_dark = icons[category][name]['dark_color'] if category else icons[name]['dark_color']
    
    icon_hover_color_light = icons[category][name]['light_hover_color'] if category else icons[name]['light_hover_color']
    icon_hover_color_dark = icons[category][name]['dark_hover_color'] if category else icons[name]['dark_hover_color']

    img = Image.open(path)

    if hover_image:
        return HoverImage(light_image=recolor_image(img, icon_color_light), 
                        dark_image=recolor_image(img, icon_color_dark),
                        size=(size, size),
                        light_color = recolor_image(img, icon_color_light),
                        light_hover_color = recolor_image(img, icon_hover_color_light),
                        dark_color = recolor_image(img, icon_color_dark),
                        dark_hover_color = recolor_image(img, icon_hover_color_dark),
                        palette=IconPalette(
                            light=icon_color_light,
                            light_hover=icon_hover_color_light,
                            dark=icon_color_dark,
                            dark_hover=icon_hover_color_dark 
                        )
                        )
    else:
        return CTkImage(light_image=recolor_image(img, icon_hover_color_light), 
                        dark_image=recolor_image(img, icon_hover_color_dark),
                        size=(size, size),
                        )

def change_icon_color(icon : HoverImage, hover=False):
    light = icon.light_hover_color if hover else icon.light_color
    dark = icon.dark_hover_color if hover else icon.dark_color
    
    icon.configure(light_image=light, dark_image=dark)

def format_date(date : datetime):
    weekday = date.weekday()
    day = date.day
    month = date.month
    year = date.year

    days_of_the_week = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    months_of_the_year = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]
    
    weekday_str = days_of_the_week[weekday]

    suffixes = {
        "st": [1, 21, 31],
        "nd": [2, 22],
        "rd": [3, 23]
    }

    suffix = None

    day_str = f"0{day}" if day < 10 else str(day)
    month_str = months_of_the_year[month - 1]
    year_str = str(year)

    for s, dates in suffixes.items():
        if day in dates:
            suffix = s

    if suffix is None:
        suffix = "th"

    return f"{weekday_str}, {day_str}{suffix} {month_str} {year_str}"

def format_time(time : datetime):
    hour = time.hour
    minute = time.minute

    hour_str = f"0{hour}" if hour < 10 else str(hour)
    minute_str = f"0{minute}" if minute < 10 else str(minute)

    return f"{hour_str}:{minute_str}"

#TO-DO helper function to accept list OR int
def create_grid(widget : CTkBaseClass, *, rows=None, columns=None, parent=True):
    
    #number of rows - all even weight
    if isinstance(rows, int): 
        for row in range(rows):
            widget.rowconfigure(row, weight=1)
    #list of row weights
    elif isinstance(rows, (list, tuple)): 
        for row, weight in enumerate(rows):
            widget.rowconfigure(row, weight=weight)

    #number of columns - all even weight
    if isinstance(columns, int):
        for column in range(columns):
            widget.columnconfigure(column, weight=1)
    #list of column weights
    elif isinstance(columns, (list, tuple)):
        for column, weight in enumerate(columns):
            widget.columnconfigure(column, weight=weight)

    #fallback for omitted - deafult to a single row/column
    if rows is None:
        widget.rowconfigure(0, weight=1)
    if columns is None:
        widget.columnconfigure(0, weight=1)

    #only child widgets should adjust size ? I think
    if parent:
        widget.grid_propagate(False)
    else:
        widget.grid_propagate(True)