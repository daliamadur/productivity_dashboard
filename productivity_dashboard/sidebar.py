import customtkinter as ctk
from .assets import load_icon, change_icon_color
from .animations import grow

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

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, pages, menu, switch_page, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        #for colours
        mode = ctk.get_appearance_mode()

        self.pages = pages
        self.menu_config = menu
        self.switch_page = switch_page

        #start condensed
        self.expanded = False
        self.FULL_WIDTH = 180
        self.CONDENSED_WIDTH = 64
        self.buttons = {}
        self.nav_buttons = {}
        self.indicators = {}

        #size of frame
        self.configure(width=self.CONDENSED_WIDTH)
        #doesn't shrink to fit
        self.grid_propagate(False)

        menu_image=load_icon(self.menu_config.icon, hover_image=True)

        self.toggle_button = HoverButton(
            self,
            text="",
            text_color = menu_image.palette.light if mode == "Light" else menu_image.palette.dark,
            image=menu_image,
            anchor="w",
            command=self.toggle
        )

        self.toggle_button.configure(bg_color=self.cget("fg_color"))

        self.buttons[self.menu_config.name] = self.toggle_button

        self.toggle_button.grid(row=0, column=0, sticky="ew", padx=8, pady=4, columnspan=2)

        nav_items = [(page.name, page.icon, page.builder) for page in pages.values()]

        for i, (name, icon, builder) in enumerate(nav_items):
            image = load_icon(icon, category="tabs", hover_image=True)
            
            nav_button = HoverButton(
                self,
                text = "",
                text_color = image.palette.light if mode == "Light" else image.palette.dark,
                text_color_disabled = image.palette.light_hover if mode == "Light" else image.palette.dark_hover,
                image=image,
                anchor="w",
                #call switch page with the builder
                command=lambda n=name, b=builder: self.switch_page(n, b),
            )

            nav_button.configure(bg_color=self.cget("fg_color"))

            border = ctk.CTkFrame(self, fg_color="transparent", width=4, height=20)
            border.grid(row=i+1, column=0, sticky="e", padx=0)
            self.indicators[name] = border
            nav_button.grid(row=i+1, column=1)
            self.buttons[name] = nav_button
            self.nav_buttons[name] = nav_button
        
        self.rowconfigure(list(range(len(self.buttons))), weight=1)

    def set_current_page(self, name):

        for (page, indicator), (_, button) in zip(self.indicators.items(), self.nav_buttons.items()):
            if page == name:
                indicator.configure(fg_color="#C8AA00")
                grow(indicator, start=0, end=indicator.cget("height"), property="HEIGHT", delay=5)
                button.configure(selected=True)
            else:
                indicator.configure(fg_color="transparent")
                button.configure(selected=False)

    def toggle(self):
        #switch states
        self.expanded = not self.expanded
        
        if self.expanded:
            for name, button in self.buttons.items():
                button.configure(text=name)
            
            #set width to full
            self.configure(width=self.FULL_WIDTH)

        else:
            for name, button in self.buttons.items():
                button.configure(text="")

            #self.configure(width=self.CONDENSED_WIDTH)
            grow(self, start=self.FULL_WIDTH, end=self.CONDENSED_WIDTH, property="WIDTH")

        self.event_generate("<<SidebarToggled>>")