import customtkinter as ctk
from .assets import load_icon, change_icon_color

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

        #bind event to method :3
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    #change colour to hover colour on mouseover/hover
    def on_enter(self, _):
        new_icon = change_icon_color(self.icon, True)
        self.configure(image=new_icon)

    def on_leave(self, _):
        new_icon = change_icon_color(self.icon)
        self.configure(image=new_icon)

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
        self.indicators = {}

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

        self.toggle_button.grid(row=0, column=0, sticky="ew", padx=8, pady=4, columnspan=2)

        nav_items = [(page.name, page.icon, page.builder) for page in pages.values()]

        for i, (name, icon, builder) in enumerate(nav_items):
            image = load_icon(icon, category="tabs")
            
            nav_button = HoverButton(
                self,
                text = name,
                image=image,
                anchor="w",
                #call switch page with the builder
                command=lambda n=name, b=builder: self.switch_page(n, b)
            )

            border = ctk.CTkFrame(self, fg_color="transparent", width=4, height=20)
            border.grid(row=i+1, column=0, sticky="e", padx=0)
            self.indicators[name] = border
            nav_button.grid(row=i+1, column=1)
            self.buttons[name] = nav_button
        
        self.rowconfigure(list(range(len(self.buttons))), weight=1)

    def set_current_page(self, name):
        for page, indicator in self.indicators.items():
            if page == name:
                indicator.configure(fg_color="#C8AA00")
            else:
                indicator.configure(fg_color="transparent")
        
        
        

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