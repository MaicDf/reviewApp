import tkinter as tk
from subtemas import PantallaSubtemas

class PantallaTemas(tk.Frame):
    def __init__(self, master, datos, guardar_datos):
        super().__init__(master)
        self.master = master
        self.datos = datos
        self.guardar_datos = guardar_datos
        self.crear_widgets()

    def crear_widgets(self):
        self.temas_frame = tk.Frame(self)
        self.temas_frame.pack()

        self.scrollbar = tk.Scrollbar(self.temas_frame, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.canvas = tk.Canvas(self.temas_frame, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar.config(command=self.canvas.yview)

        self.frame_contenido = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_contenido, anchor="nw")

        # Crear botones de temas
        self.mostrar_temas()

        # Botón "Añadir Tema"
        self.btn_anadir_tema = tk.Button(self, text="Añadir Tema", command=self.anadir_tema)
        self.btn_anadir_tema.pack()

        self.frame_contenido.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))

    def mostrar_temas(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

        for tema in self.datos["temas"]:
            btn_tema = tk.Button(self.frame_contenido, text=tema["nombre"], 
                                 bg=self.calcular_color(tema["subtemas"]), 
                                 command=lambda tema=tema: self.abrir_subtemas(tema))
            btn_tema.pack(fill="x")

    def anadir_tema(self):
        nuevo_tema = {"nombre": "Nuevo Tema", "subtemas": []}
        self.datos["temas"].append(nuevo_tema)
        self.guardar_datos(self.datos)
        self.mostrar_temas()

    def abrir_subtemas(self, tema):
        ventana_subtemas = tk.Toplevel(self.master)
        app_subtemas = PantallaSubtemas(ventana_subtemas, tema, self.datos, self.guardar_datos)
        app_subtemas.pack()

    def calcular_color(self, subtemas):
        # Calcular color basado en los subtemas
        total = len(subtemas)
        verde = rojo = 0
        for subtema in subtemas:
            if subtema["estado"] == "onTime":
                verde += 1
            elif subtema["estado"] == "overDue":
                rojo += 1

        proporción_verde = verde / total if total > 0 else 0
        proporción_rojo = rojo / total if total > 0 else 0

        # Utilizar una escala de color de verde a rojo
        color = self.lerp_color((0, 255, 0), (255, 0, 0), proporción_rojo)
        return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"

    def lerp_color(self, color1, color2, t):
        return (
            int(color1[0] + (color2[0] - color1[0]) * t),
            int(color1[1] + (color2[1] - color1[1]) * t),
            int(color1[2] + (color2[2] - color1[2]) * t),
        )
