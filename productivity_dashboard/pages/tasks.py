import customtkinter as ctk
from ..utils import create_grid
from ..models import Task, Layout
from .page import Tab

class TasksTab(Tab):
    def __init__(self, parent, name, task_list):
        super().__init__(
            parent=parent,
            name=name,
            state=task_list,
            layout=Layout(
                body_columns=[3,2]
            )
        )

        self.state: list[Task]

    def _build(self):
        self._build_task_list_column()
        self._build_add_task_column()
    
    def _build_task_list_column(self):
        frame = ctk.CTkFrame(self.body, fg_color="transparent")
        frame.grid(row=0, column=0, rowspan=6, sticky="nesw", padx=16)
        create_grid(frame, rows=len(self.state) + 2, columns=6)

        label = ctk.CTkLabel(frame, text="Task List")
        label.grid(row=0, column=0, columnspan=6, sticky="nesw")

        for i, task in enumerate(self.state):
            checkbox = ctk.CTkCheckBox(frame,
                                       text=task.name,
                                       border_width=2,
                                       border_color="white",
                                       corner_radius=24,
                                       checkbox_height=20,
                                       checkbox_width=20,
                                       hover_color="#808080",
                                       )

            expand_button = ctk.CTkButton(frame, text="↗️", fg_color="transparent")

            checkbox.grid(row=i + 1, column=0, columnspan=2, sticky="nsw")
            expand_button.grid(row=i + 1, column=2, sticky="nes")

        example_steps_object = [
            "Identify folders to be decluttered",
            "Open and review contents of each folder",
            "Delete files that are no longer needed",
            "Move important files to appropriate locations",
            "Empty recycle bin"
        ]

        steps = ctk.CTkFrame(frame, fg_color="#404040")
        steps.grid(row=1, column=3, rowspan=len(self.state), columnspan=3, sticky="nesw")

        create_grid(steps, rows=len(example_steps_object))

        for i, step in enumerate(example_steps_object):
            checkbox = ctk.CTkCheckBox(steps,
                                       text=step,
                                       border_width=2,
                                       border_color="white",
                                       corner_radius=24,
                                       checkbox_height=20,
                                       checkbox_width=20,
                                       hover_color="#808080",
                                       )

            checkbox.grid(row=i, column=0, sticky="nesw", padx=8)

        clear_completed_button = ctk.CTkButton(frame, text="Clear Completed")
        reorder_button = ctk.CTkButton(frame, text="Re-order Tasks")
        save_button = ctk.CTkButton(frame, text="Save Task List")

        buttons = [clear_completed_button, reorder_button, save_button]

        for i, button in enumerate(buttons):
            button.grid(row=len(self.state) + 1, column = i*2, columnspan=2, sticky="")

    def _build_add_task_column(self):
        frame = ctk.CTkFrame(self.body, fg_color="transparent")
        frame.grid(row=0, column=1, rowspan=6, sticky="nesw", padx=16)
                   
        create_grid(frame, rows=[1, 1, 1, 2, 1, 1, 1], columns=[2, 1])

        label = ctk.CTkLabel(frame, text="Add New Task")
        label.grid(row=0, column=0, columnspan=2, sticky="nesw")

        task_textarea = ctk.CTkEntry(frame, placeholder_text="Task Name")
        task_textarea.grid(row=1, column=0, columnspan=2, sticky="nesw")

        steps_label = ctk.CTkLabel(frame, text="Steps:")
        steps_label.grid(row=2, column=0, columnspan=2, sticky="nsw", padx=8)
        
        steps_textarea = ctk.CTkTextbox(frame)
        steps_textarea.grid(row=3, column=0, columnspan=2, sticky="nesw")

        save_button = ctk.CTkButton(frame, text="Add to task list")
        save_button.grid(row=4, column=1, sticky="e")

        import_button_1 = ctk.CTkButton(frame, text="Import from Task Picker")
        import_button_1.grid(row=5, column=0, columnspan=2, sticky="")

        import_button_2 = ctk.CTkButton(frame, text="Import from Task Picker")
        import_button_2.grid(row=6, column=0, columnspan=2, sticky="")