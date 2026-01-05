import customtkinter as ctk
import yaml, requests

from PIL import Image, ImageColor, ImageChops
from dataclasses import dataclass
from urllib.parse import urlparse
from datetime import datetime, timedelta
from pathlib import Path
from io import BytesIO
from math import floor

@dataclass
class IconPalette():
    light: str
    light_hover: str
    dark: str
    dark_hover: str

class HoverImage(ctk.CTkImage):
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

class HoverButton(ctk.CTkButton):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            fg_color="transparent",
            border_width=0,
            hover=False
        )

        self.icon = self.cget("image")
        self.selected = False

        #bind event to method :3
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    #change colour to hover colour on mouseover/hover
    def on_enter(self, _):
        mode = ctk.get_appearance_mode()

        if not self.selected:
            change_icon_color(self.icon, True)
            color = self.icon.palette.light_hover if mode == "Light" else self.icon.palette.dark_hover
            self.configure(text_color=color)

    def on_leave(self, _):
        mode = ctk.get_appearance_mode()

        if not self.selected:
            change_icon_color(self.icon)
            color = self.icon.palette.light if mode == "Light" else self.icon.palette.dark
            self.configure(text_color=color)

    def configure(self, **kwargs):
        if "selected" in kwargs:
            self.selected = kwargs.pop("selected")

            if self.selected:
                change_icon_color(self.icon, True)
                self.configure(state=ctk.DISABLED)
            else:
                change_icon_color(self.icon)
                self.configure(state=ctk.NORMAL)
                
        return super().configure(**kwargs)

class HyperLink(ctk.CTkLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    #change colour to hover colour on mouseover/hover
    def on_enter(self, _):
        font = self.cget("font")
        self.underlined = font.configure(underline=True)

    def on_leave(self, _):
        font = self.cget("font")
        self.underlined = font.configure(underline=False)

BASE_DIR = Path(__file__).resolve().parent.parent

def hex_to_rgba(code):
    return ImageColor.getcolor(code, "RGBA")

def rgba_to_hex(rgba):
    r, g, b, a = rgba
    return "#{:02x}{:02x}{:02x}{:02x}".format(r, g, b, a)

#for light mode icon
def invertRGBA(image: Image):
    r, g, b, a = image.split()
    rgb = Image.merge('RGB', (r, g, b))

    inverted = ImageChops.invert(rgb)
    r, g, b = inverted.split()

    return Image.merge('RGBA', (r, g, b, a))

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
        return ctk.CTkImage(light_image=recolor_image(img, icon_hover_color_light), 
                        dark_image=recolor_image(img, icon_hover_color_dark),
                        size=(size, size),
                        )

#for links
def load_favicon(url: str, size: int) -> Image.Image | None:
    try:
        parsed_url = urlparse(url)
        favicon_url = f"{parsed_url.scheme}://{parsed_url.netloc}/favicon.ico"

        res = requests.get(favicon_url, timeout=3)
        res.raise_for_status()
        image = Image.open(BytesIO(res.content)).convert("RGBA")

        github = 'github' in url

        if github:
            dark_img = invertRGBA(image)
            #more like image CHOPPED :x - fix please
        
        return ctk.CTkImage(
            light_image=image,
            dark_image=dark_img if github else None,
            size=(size, size)
        )
    except:
        return None

def change_icon_color(icon : HoverImage, hover=False):
    light = icon.light_hover_color if hover else icon.light_color
    dark = icon.dark_hover_color if hover else icon.dark_color
    
    icon.configure(light_image=light, dark_image=dark)

def pulse(hex_code : str):
    ADD = 2894892
    hex = hex_code.strip("#")
    int_code = int(hex, 16)

    new_color = int_code + ADD

    return "#{:06x}".format(new_color).upper()

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

    day_str = str(day)
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

    return f"{hour:02}:{minute:02}"

def format_duration(time : timedelta):
    total = time.seconds

    hours = total // 3600
    minutes = (total // 60) % 60
    seconds = total % 60

    components = []
    flags = []

    if hours:
        components.extend([str(hours), " hours" if hours > 1 else " hour"])
        flags.append(True)
    if minutes:
        components.extend([str(minutes), " minutes" if minutes != 1 else " minute"])
        flags.append(True)
    if seconds:
        components.extend([str(seconds), " seconds" if seconds != 1 else " second"])
        flags.append(True)

    #sentence builder
    if len(flags) == 3:
        components.insert(2, ", ")

    if len(flags) > 1:
        components.insert(-2, " and ")

    return "".join(components)


def format_pomodoro(time_remaining: int):
    #split into mins and seconds
    m_remaining = floor(time_remaining / 60)
    s_remaining = time_remaining % 60
    
    #format 00:00
    return f"{m_remaining:02}:{s_remaining:02}"

def create_grid(widget : ctk.CTkBaseClass, *, rows=None, columns=None, parent=True):
    
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