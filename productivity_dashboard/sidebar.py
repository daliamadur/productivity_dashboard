import customtkinter as ctk
from .assets import load_icon

class HoverButton(ctk.CTkButton):
    def __init__(self, *args, **kwargs):
        self.normal_color = kwargs.pop("fg_color", "transparent")
        self.hover_color = kwargs.pop("hover_color", "#151515")

        super().__init__(
            *args,
            **kwargs,
            fg_color=self.normal_color,
            corner_radius=12,
            border_width=0,
            hover=False
        )

        #bind event to method :3
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    #change colour to hover colour on mouseover/hover
    def on_enter(self, _):
        self.configure(fg_color=self.hover_color)

    def on_leave(self, _):
        self.configure(fg_color=self.normal_color)

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, pages, menu, switch_page, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.pages = pages
        self.menu_config = menu
        self.switch_page = switch_page

        #start condensed
        self.expanded = False
        self.FULL_WIDTH = 180
        self.CONDENSED_WIDTH = 60
        self.buttons = {}

        #size of frame
        self.configure(width=self.FULL_WIDTH)
        #doesn't shrink to fit
        self.grid_propagate(False)

        self.toggle_button = HoverButton(
            self,
            text=self.menu_config.name,
            image=load_icon(self.menu_config.icon),
            anchor="w",
            command=self.toggle
            
        )

        self.buttons[self.menu_config.name] = self.toggle_button

        self.toggle_button.grid(row=0, column=0, sticky="ew", padx=8, pady=4)

        nav_items = [(page.name, page.icon, page.builder) for page in pages.values()]

        for i, (name, icon, builder) in enumerate(nav_items):
            nav_button = HoverButton(
                self,
                text = name,
                image=load_icon(icon, category="tabs"),
                anchor="w",
                #call switch page with the builder
                command=lambda b=builder: self.switch_page(b),
            )
            nav_button.grid(row=i + 1, column=0, sticky="ew", padx=8, pady=4)
            self.buttons[name] = nav_button
        
        self.rowconfigure(list(range(len(self.buttons))), weight=1)

    def toggle(self):
        #switch states
        self.expanded = not self.expanded
        
        if self.expanded:
            #set width to full
            self.configure(width=self.FULL_WIDTH)
            #set text to label names
            self.toggle_button.configure(text=self.menu_config.name)
            for name, button in self.buttons.items():
                button.configure(text=name)
        else:
            #set width to full
            self.configure(width=self.CONDENSED_WIDTH)
            #set text to label names
            self.toggle_button.configure(text="")
            for button in self.buttons.values():
                button.configure(text="")

        self.event_generate("<<SidebarToggled>>")