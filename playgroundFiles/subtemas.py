import tkinter as tk
#from subsubtemas import PantallaSubsubtemas

class PantallaSubtemas(tk.Frame):
    def __init__(self, master, tema, datos, guardar_datos):
        super().__init__(master)
        self.master = master
        self.tema = tema
        self.datos = datos
        self.guardar_datos = guardar_datos
        self.crear_widgets()

    def crear_widgets(self):
        self.frame_subtemas = tk.Frame(self)
        self.frame_subtemas.pack()

        self.scrollbar = tk.Scrollbar(self.frame_subtemas, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.canvas = tk.Canvas(self.frame_subtemas, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar.config(command=self.canvas.yview)

        self.frame_contenido = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_contenido, anchor="nw")

        # Crear botones de subtemas
        self.mostrar_subtemas()

        self.btn_anadir_subtema = tk.Button(self, text="Añadir Subtema", command=self.anadir_subtema)
        self.btn_anadir_subtema.pack()

        self.frame_contenido.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))

    def mostrar_subtemas(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

        for subtema in self.tema["subtemas"]:
            btn_subtema = tk.Button(self.frame_contenido, text=subtema["nombre"], 
                                    bg=self.calcular_color(subtema["subsubtemas"]),
                                    command=lambda subtema=subtema: self.abrir_subsubtemas(subtema))
            btn_subtema.pack(fill="x")

    def anadir_subtema(self):
        nuevo_subtema = {"nombre": "Nuevo Subtema", "subsubtemas": []}
        self.tema["subtemas"].append(nuevo_subtema)
        self.guardar_datos(self.datos)
        self.mostrar_subtemas()

    def abrir_subsubtemas(self, subtema):
        ventana_subsubtemas = tk.Toplevel(self.master)
        app_subsubtemas = PantallaSubsubtemas(ventana_subsubtemas, subtema, self.datos, self.guardar_datos)
        app_subsubtemas.pack()

    def calcular_color(self, subsubtemas):
        # Calcular color basado en los subsubtemas
        total = len(subsubtemas)
        verde = rojo = 0
        for subsubtema in subsubtemas:
            if subsubtema["estado"] == "onTime":
                verde += 1
            elif subsubtema["estado"] == "overDue":
                rojo += 1

        proporción_verde = verde / total if total > 0 else 0
        proporción_rojo = rojo / total if total > 0 else 0

        color = self.lerp_color((0, 255, 0), (255, 0, 0), proporción_rojo)
        return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"

    def lerp_color(self, color1, color2, t):
        return (
            int(color1[0] + (color2[0] - color1[0]) * t),
            int(color1[1] + (color2[1] - color1[1]) * t),
            int(color1[2] + (color2[2] - color1[2]) * t),
        )
