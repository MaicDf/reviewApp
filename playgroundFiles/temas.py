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
        self.temas_frame.pack(fill="both", expand=True)

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

        filas, columnas = 3, 4  # Configuración de 3 filas x 4 columnas
        for index, tema in enumerate(self.datos["temas"]):
            fila = index // columnas
            columna = index % columnas

            btn_tema = tk.Button(self.frame_contenido, text=tema["nombre"], 
                                 bg=self.calcular_color(tema["subtemas"]), 
                                 #command=lambda tema=tema: self.abrir_subtemas(tema)
                                )
            btn_tema.grid(row=fila, column=columna, sticky="nsew", padx=5, pady=5)

        # Ajustar el peso de las columnas y filas para un diseño uniforme
        for i in range(filas):
            self.frame_contenido.grid_rowconfigure(i, weight=2)
        for j in range(columnas):
            self.frame_contenido.grid_columnconfigure(j, weight=1)

    def anadir_tema(self):
        # Crear una ventana para ingresar el nombre del nuevo tema
        ventana_entrada = tk.Toplevel(self.master)
        ventana_entrada.title("Ingrese el nombre del nuevo tema")

        label = tk.Label(ventana_entrada, text="Nombre del Tema:")
        label.pack(pady=10)

        entry_nombre = tk.Entry(ventana_entrada)
        entry_nombre.pack(pady=10)

        def guardar_tema():
            nombre_tema = entry_nombre.get()
            if nombre_tema.strip():  # Verificar si el nombre no está vacío
                nuevo_tema = {"nombre": nombre_tema ,"subtemas": []}
                self.datos["temas"].append(nuevo_tema)
                print(self.datos)
                self.guardar_datos(self.datos)
                self.mostrar_temas()
            ventana_entrada.destroy()

        btn_guardar = tk.Button(ventana_entrada, text="Guardar", command=guardar_tema)
        btn_guardar.pack(pady=10)

    def abrir_subtemas(self, tema):
        ventana_subtemas = tk.Toplevel(self.master)
        app_subtemas = PantallaSubtemas(ventana_subtemas, tema, self.datos, self.guardar_datos)
        app_subtemas.pack()

    def calcular_color(self, subtemas):
        # Calcular color basado en los subtemas
        total = len(subtemas)
        sumEstados = 0
        for subtema in subtemas:
            # Asumimos que "estado" está representado como un valor numérico.
            sumEstados += float(subtema["estado"])

        proporción_verde = sumEstados / total if total > 0 else 0
        proporción_rojo = 1 - proporción_verde if total > 0 else 0

        # Utilizar una escala de color de verde claro a rojo claro
        color = self.lerp_color((144, 238, 144), (255, 182, 193), proporción_rojo)
        return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"

    def lerp_color(self, color1, color2, t):
        return (
            int(color1[0] + (color2[0] - color1[0]) * t),
            int(color1[1] + (color2[1] - color1[1]) * t),
            int(color1[2] + (color2[2] - color1[2]) * t),
        )
