import tkinter as tk
from detalles import PantallaDetalles
import json
from datetime import datetime, timedelta

class PantallaSubsubtemas(tk.Frame):
    def __init__(self, master, subtema, datos, guardar_datos):
        super().__init__(master)
        self.master = master
        self.subtema = subtema
        self.datos = datos
        self.guardar_datos = guardar_datos
        self.crear_widgets()

    def crear_widgets(self):
        self.frame_subsubtemas = tk.Frame(self)
        self.frame_subsubtemas.pack()

        self.scrollbar = tk.Scrollbar(self.frame_subsubtemas, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.canvas = tk.Canvas(self.frame_subsubtemas, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar.config(command=self.canvas.yview)

        self.frame_contenido = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_contenido, anchor="nw")

        # Crear botones de subsubtemas
        self.mostrar_subsubtemas()

        self.btn_anadir_subsubtema = tk.Button(self, text="Añadir Subsubtema", command=self.anadir_subsubtema)
        self.btn_anadir_subsubtema.pack()

        self.frame_contenido.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))

    def mostrar_subsubtemas(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

        for subsubtema in self.subtema["subsubtemas"]:
            btn_subsubtema = tk.Button(self.frame_contenido, text=subsubtema["nombre"], 
                                       bg=self.calcular_color(subsubtema),
                                       command=lambda subsubtema=subsubtema: self.abrir_detalles(subsubtema))
            btn_subsubtema.pack(fill="x")

    def anadir_subsubtema(self):
        nuevo_subsubtema = {"nombre": "Nuevo Subsubtema", "estado": "onTime", "fecha_repaso": None}
        self.subtema["subsubtemas"].append(nuevo_subsubtema)
        self.guardar_datos(self.datos)
        self.mostrar_subsubtemas()

    def abrir_detalles(self, subsubtema):
        ventana_detalles = tk.Toplevel(self.master)
        app_detalles = PantallaDetalles(ventana_detalles, subsubtema, self.datos, self.guardar_datos)
        app_detalles.pack()

    def calcular_color(self, subsubtema):
        # Cálculo del color basado en la fecha de repaso
        if subsubtema["fecha_repaso"]:
            dias_restantes = (subsubtema["fecha_repaso"] - datetime.date.today()).days
            if dias_restantes >= 10:
                return "lightgreen"
            elif dias_restantes >= 0:
                return "lightyellow"
            else:
                return "lightcoral"
        return "lightgreen"

# Función para cargar datos desde el archivo
def cargar_datos():
    try:
        with open("data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # Si el archivo no existe, devolvemos una estructura vacía
        return {"temas": []}

# Función para guardar datos en el archivo
def guardar_datos(datos):
    with open("data.json", "w") as file:
        json.dump(datos, file, indent=4)

# Función para cargar los subsubtemas de un tema y subtema específicos
def cargar_subsubtemas(tema, subtema):
    datos = cargar_datos()
    for t in datos["temas"]:
        if t["nombre"] == tema:
            for st in t["subtemas"]:
                if st["nombre"] == subtema:
                    return st["subsubtemas"]
    return []  # Si no se encuentra el subtema, retornamos una lista vacía

# Función para agregar un nuevo subsubtema
def agregar_subsubtema(tema, subtema, nombre_subsubtema):
    datos = cargar_datos()
    for t in datos["temas"]:
        if t["nombre"] == tema:
            for st in t["subtemas"]:
                if st["nombre"] == subtema:
                    st["subsubtemas"].append({
                        "nombre": nombre_subsubtema,
                        "estado": "onTime",  # Estado inicial
                        "fecha_repaso": None
                    })
                    break
    guardar_datos(datos)  # Guardamos los cambios en el archivo

# Función para actualizar la fecha de repaso de un subsubtema
def actualizar_fecha_repaso(tema, subtema, nombre_subsubtema, fecha_repaso):
    datos = cargar_datos()
    for t in datos["temas"]:
        if t["nombre"] == tema:
            for st in t["subtemas"]:
                if st["nombre"] == subtema:
                    for ss in st["subsubtemas"]:
                        if ss["nombre"] == nombre_subsubtema:
                            ss["fecha_repaso"] = fecha_repaso
                            break
    guardar_datos(datos)  # Guardamos los cambios en el archivo

# Función para calcular el estado de un subsubtema según la fecha de repaso
def calcular_estado(fecha_repaso):
    if not fecha_repaso:
        return "onTime"  # Si no tiene fecha de repaso, se considera en tiempo
    fecha_repaso = datetime.strptime(fecha_repaso, "%Y-%m-%d")
    hoy = datetime.now()
    diferencia = (fecha_repaso - hoy).days
    if diferencia > 10:
        return "onTime"
    elif 0 <= diferencia <= 10:
        return "dueSoon"
    else:
        return "overDue"

# Función para calcular el color de fondo basado en el estado
def calcular_color_fondo(estado):
    if estado == "onTime":
        return "#90EE90"  # Verde claro
    elif estado == "dueSoon":
        return "#FFFF99"  # Amarillo claro
    elif estado == "overDue":
        return "#FFCCCB"  # Rojo claro