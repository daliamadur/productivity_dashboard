import customtkinter as ctk
import productivity_dashboard as dash

class App(ctk.CTk):
    def __init__(self, pages, menu):
        super().__init__()
        self.title("This is my new app :3")
        self.geometry("1000x600")

        self.menu = menu
        self.pages = pages

        #import + instantiate sidebar
        self.sidebar = dash.Sidebar(self, self.pages, self.menu, self.switch_page)
        self.sidebar.pack(side="left", fill="y")
    
    def switch_page(builder):
        print("build this page please :3", builder)

app = App(pages=dash.PAGES, menu=dash.MENU)
app.mainloop()