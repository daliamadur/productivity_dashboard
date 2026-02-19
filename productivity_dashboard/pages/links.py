import customtkinter as ctk
from ..models import Link, Layout
from ..utils import HyperLink, create_grid, load_favicon, load_icon, callback
from ..CTkScrollableDropdown import ctk_scrollable_dropdown as ctk_sd
from .page import Tab

class LinksTab(Tab):
    def __init__(self, parent, name, links_list):
        super().__init__(
            parent=parent,
            name=name,
            state=links_list,
            layout=Layout(
                body_columns=[3,2]
            )
        )

        self.state: list[Link]

    def _build(self):
        self._build_links_list()
        self._build_settings_panel()
    
    def _build_links_list(self):
        frame = ctk.CTkFrame(self.body, fg_color="transparent")
        frame.grid(column=0, row=0, sticky="nesw")

        cols = len(self.state) // 10
        
        create_grid(frame, rows=10, columns=cols)
        
        for i, link in enumerate(self.state):
            link_frame = ctk.CTkFrame(frame, fg_color="transparent")
            create_grid(link_frame, columns=2)
            link.icon

            icon = load_favicon(link.url, 20) if load_favicon(link.url, 20) else load_icon(link.icon, size=20, hover_image=False)
            image = ctk.CTkLabel(link_frame, text="", image=icon)
            label = HyperLink(link_frame, text=link.name, cursor="hand2")
            
            label.bind(f"<Button-1>", lambda _: callback(link.url))
            image.grid(row=0, column=0, sticky="e", padx=2)
            label.grid(row=0, column=1, sticky="w", padx=2)

            link_frame.grid(row=i%10, column=i//10, sticky="nsw", padx=24, pady=8)

    def _build_add_link_buttons(self, frame, start):
        add_link_label = ctk.CTkLabel(frame, text="Add Link")
        add_link_name_label = ctk.CTkLabel(frame, text="Name:")
        add_link_name_input = ctk.CTkEntry(frame)
        add_link_url_label = ctk.CTkLabel(frame, text="URL:")
        add_link_url_input = ctk.CTkEntry(frame)
        add_link_button = ctk.CTkButton(frame, text="Add Link")

        add_link_label.grid(row=start, column=0, columnspan=2)

        add_link_name_label.grid(row=start + 1, column=0)
        add_link_name_input.grid(row=start + 1, column=1)
        
        add_link_url_label.grid(row=start + 2, column=0)
        add_link_url_input.grid(row=start + 2, column=1)
        
        add_link_button.grid(row=start + 3, column=0, columnspan=2)

    def _build_edit_link_buttons(self, frame, start):
        edit_link_label = ctk.CTkLabel(frame, text="Edit Link")
        edit_link_select = ctk.CTkComboBox(frame)
        edit_link_name_label = ctk.CTkLabel(frame, text="Name:")
        edit_link_name_input = ctk.CTkEntry(frame)
        edit_link_url_label = ctk.CTkLabel(frame, text="URL:")
        edit_link_url_input = ctk.CTkEntry(frame)
        edit_link_button = ctk.CTkButton(frame, text="Edit Link")

        edit_link_label.grid(row=start, column=0, columnspan=2)

        edit_link_select.grid(row=start + 1, column=0, columnspan=2)
        edit_link_select.set(self.state[0].name)
        
        #use command= parameter later for functionality
        ctk_sd.CTkScrollableDropdown(edit_link_select, values=[link.name for link in self.state])

        edit_link_name_label.grid(row=start + 2, column=0)
        edit_link_name_input.grid(row=start + 2, column=1)
        
        edit_link_url_label.grid(row=start + 3, column=0)
        edit_link_url_input.grid(row=start + 3, column=1)
        
        edit_link_button.grid(row=start + 4, column=0, columnspan=2)
    
    def _build_delete_link_buttons(self, frame, start):
        delete_link_label = ctk.CTkLabel(frame, text="Delete Link")
        delete_link_select = ctk.CTkComboBox(frame)
        delete_link_button = ctk.CTkButton(frame, text="Delete Link")

        delete_link_label.grid(row=start, column=0, columnspan=2)

        delete_link_select.grid(row=start + 1, column=0, columnspan=2)
        delete_link_select.set(self.state[0].name)
        
        #use command= parameter later for functionality
        ctk_sd.CTkScrollableDropdown(delete_link_select, values=[link.name for link in self.state])
        
        delete_link_button.grid(row=start + 2, column=0, columnspan=2)

    def _build_settings_panel(self):
        frame = ctk.CTkFrame(self.body, fg_color="transparent")
        frame.grid(column=1, row=0, sticky="nesw", pady=16)

        create_grid(frame, rows=14, columns=2)

        #add link
        self._build_add_link_buttons(frame, 0)

        #edit link
        self._build_edit_link_buttons(frame, 5)

        #delete link
        self._build_delete_link_buttons(frame, 11)




