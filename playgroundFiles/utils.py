from datetime import datetime
from tkinter import font
import tkinter as tk

#update estados
def update_estados(datos,guardar_datos):
    for tema in datos["temas"]:
        for subtema in tema["subtemas"]:
            # Update the estado of subsubtemas
            for subsubtema in subtema["subsubtemas"]:
                deadline = datetime.strptime(subsubtema["deadline"], '%Y-%m-%d')
                delta = (deadline - datetime.today()).days
                
                # Calculate the estado based on the deadline
                if delta >= 30:
                    estado = 1.0
                elif delta >= 0:  # Ensure we handle deadlines in the past
                    estado = delta / 30
                else:
                    estado = 0.0
                
                subsubtema["estado"] = estado
                #print(f"Subsubtema estado: {estado}")

            # Update the estado of subtema
            total_subsubtemas = len(subtema["subsubtemas"])
            if total_subsubtemas > 0:
                subtema["estado"] = sum(subsubtema["estado"] for subsubtema in subtema["subsubtemas"]) / total_subsubtemas
            else:
                subtema["estado"] = 0.0
            #print(f"Subtema estado: {subtema['estado']}")

        # Update the estado of tema
        total_subtemas = len(tema["subtemas"])
        if total_subtemas > 0:
            tema["estado"] = sum(subtema["estado"] for subtema in tema["subtemas"]) / total_subtemas
        else:
            tema["estado"] = 0.0
        #print(f"Tema estado: {tema['estado']}")

    # Save the updated data
    guardar_datos(datos)


def assign_positions(datos):
    # Iterate over each 'tema'
    for tema_index, tema in enumerate(datos["temas"]):
        # Assign position to 'tema'
        tema["pos"] = tema_index

        # Iterate over each 'subtema' in the current 'tema'
        for subtema_index, subtema in enumerate(tema["subtemas"]):
            # Assign position to 'subtema'
            subtema["pos"] = subtema_index

            # Iterate over each 'subsubtema' in the current 'subtema'
            for subsubtema_index, subsubtema in enumerate(subtema["subsubtemas"]):
                # Assign position to 'subsubtema'
                subsubtema["pos"] = subsubtema_index

    # Return the updated data structure with positions
    return datos
    

#improve text editor.
import tkinter as tk
from tkinter import font

class RichTextEditor(tk.Text):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(undo=True, wrap="word")  # Enable undo/redo
        self.base_font = font.Font(family="Arial", size=12)

        # Create bold and italic fonts
        self.bold_font = font.Font(family="Arial", size=12, weight="bold")
        self.italic_font = font.Font(family="Arial", size=12, slant="italic")

        # Default tags for text formatting
        self.tag_configure("bold", font=self.bold_font)
        self.tag_configure("italic", font=self.italic_font)
        self.tag_configure("highlight", background="yellow")

        # Bind shortcuts
        self.bind("<Control-b>", self.toggle_bold)
        self.bind("<Control-i>", self.toggle_italic)
        self.bind("<Control-z>", lambda e: self.edit_undo())
        self.bind("<Control-y>", lambda e: self.edit_redo())

    def toggle_bold(self, event=None):
        self.toggle_tag("bold")
        return "break"

    def toggle_italic(self, event=None):
        self.toggle_tag("italic")
        return "break"

    def toggle_tag(self, tag):
        try:
            start, end = self.index("sel.first"), self.index("sel.last")
            if tag in self.tag_names("sel.first"):
                self.tag_remove(tag, start, end)
            else:
                self.tag_add(tag, start, end)
        except tk.TclError:
            pass  # No selection
