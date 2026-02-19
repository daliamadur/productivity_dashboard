from ..utils import create_grid, build_top_panel, build_bottom_panel
from ..base_state import BaseState
from ..models import Layout
import customtkinter as ctk

class Tab(ctk.CTkFrame):
    def __init__(self, parent, name: str, state: BaseState, layout: Layout):
        super().__init__(parent)

        self.state = state
        self.name = name
        
        create_grid(widget=self, rows=layout.rows)

        self.head = build_top_panel(name, self)
        self.body = build_bottom_panel(self, rows=layout.body_rows, columns=layout.body_columns)

        self._build()

    def _build(self):
        pass