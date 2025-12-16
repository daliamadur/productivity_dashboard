import customtkinter as ctk
import productivity_dashboard as dash

class App(ctk.CTk):
    def __init__(self, pages, menu, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("This is my new app :3")
        self.geometry("1000x600")

        self.menu = menu
        self.pages = pages

        #import + instantiate sidebar
        self.sidebar = dash.Sidebar(self, self.pages, self.menu, self.switch_page)
        self.sidebar.pack(side="left", fill=ctk.BOTH)

        #get prev background
        current_bg = self.cget("fg_color")
        self.main_window = ctk.CTkFrame(self, fg_color=current_bg)
        self.main_window.pack(expand=True, fill="both")
        self.configure(fg_color=self.sidebar.cget("fg_color"))
    
    def switch_page(self, name, builder):
        print("build this page please :3", builder)
        self.sidebar.set_current_page(name)

app = App(pages=dash.PAGES, menu=dash.MENU)
#get + set home page by default
home_page = dash.PAGES.get("HOME")
app.switch_page(home_page.name, home_page.builder)

app.mainloop()