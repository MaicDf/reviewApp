import tkinter as tk
from datetime import timedelta, date

class PantallaDetalles(tk.Frame):
    def __init__(self, master, subsubtema, datos, guardar_datos):
        super().__init__(master)
        self.master = master
        self.subsubtema = subsubtema
        self.datos = datos
        self.guardar_datos = guardar_datos
        self.crear_widgets()

    def crear_widgets(self):
        self.atomic_task_label = tk.Label(self, text="Atomic Task")
        self.atomic_task_label.pack()

        self.atomic_task_entry = tk.Entry(self)
        self.atomic_task_entry.pack()

        self.concept_label = tk.Label(self, text="Concept, Active Recall")
        self.concept_label.pack()

        self.concept_entry = tk.Entry(self)
        self.concept_entry.pack()

        self.show_button = tk.Button(self, text="Show", command=self.mostrar_conceptos)
        self.show_button.pack()

        self.done_button = tk.Button(self, text="Done (Default)", command=self.configurar_repaso_default)
        self.done_button.pack()

        self.done_custom_button = tk.Button(self, text="Done (Custom)", command=self.configurar_repaso_custom)
        self.done_custom_button.pack()

    def mostrar_conceptos(self):
        self.concept_entry.config(state="normal")

    def configurar_repaso_default(self):
        self.subsubtema["fecha_repaso"] = date.today() + timedelta(days=30)
        self.guardar_datos(self.datos)

    def configurar_repaso_custom(self):
        dias = int(self.ask_custom_days())
        self.subsubtema["fecha_repaso"] = date.today() + timedelta(days=dias)
        self.guardar_datos(self.datos)

    def ask_custom_days(self):
        return tk.simpledialog.askstring("Custom Days", "Enter the number of days:")
