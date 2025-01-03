import tkinter as tk
from subsubtemas import PantallaSubsubtemas

class PantallaSubtemas(tk.Frame):
    def __init__(self, master, tema, datos, guardar_datos):
        super().__init__(master)
        self.master = master
        self.tema = tema
        self.datos = datos
        self.guardar_datos = guardar_datos
        self.crear_widgets()
        self.temas_frame = tk.Frame(self, width=450)
        self.temas_frame.pack(fill="both", expand=True)
        
    def crear_widgets(self):
        self.label_titulo = tk.Label(self, text=self.tema["nombre"], font=("Arial", 16, "bold"))
        self.label_titulo.pack(pady=10)

        self.subtemas_frame = tk.Frame(self)
        self.subtemas_frame.pack(fill="both", expand=True)

        # Scrollbars for horizontal and vertical scrolling
        self.scrollbar_y = tk.Scrollbar(self.subtemas_frame, orient="vertical")
        self.scrollbar_y.pack(side="right", fill="y")

        self.scrollbar_x = tk.Scrollbar(self.subtemas_frame, orient="horizontal")
        self.scrollbar_x.pack(side="bottom", fill="x")

        # Canvas for dynamic content
        self.canvas = tk.Canvas(
            self.subtemas_frame, 
            yscrollcommand=self.scrollbar_y.set, 
            xscrollcommand=self.scrollbar_x.set
        )
        self.canvas.pack(side="left", fill="both", expand=True)

        # Configure scrollbars
        self.scrollbar_y.config(command=self.canvas.yview)
        self.scrollbar_x.config(command=self.canvas.xview)

        self.frame_contenido = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_contenido, anchor="nw")

        # Display subtopics
        self.mostrar_subtemas()

        # Buttons for actions
        self.btn_anadir_subtema = tk.Button(self, text="Añadir Subtema", command=self.anadir_subtema)
        self.btn_anadir_subtema.pack(pady=5)

        self.btn_editar_tema = tk.Button(self, text="Editar Tema", command=self.editar_tema)
        self.btn_editar_tema.pack(pady=5)

        self.btn_eliminar_tema = tk.Button(self, text="Eliminar Tema", command=self.eliminar_tema)
        self.btn_eliminar_tema.pack(pady=5)

        self.frame_contenido.bind("<Configure>", self.actualizar_scrollregion)

    def mostrar_subtemas(self):
        # Clear previous widgets
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

        # Define grid layout
        filas, columnas = 3, 4
        for index, subtema in enumerate(self.tema["subtemas"]):
            fila = index // columnas
            columna = index % columnas

            # Create a button for each subtopic
            btn_subtema = tk.Button(
                self.frame_contenido,
                text=subtema["nombre"],
                bg=self.calcular_color(subtema),
                command=lambda subtema=subtema: self.abrir_subsubtemas(subtema))
            
            btn_subtema.grid(row=fila, column=columna, sticky="nsew", padx=5, pady=5)
            print(self.datos)
            self.guardar_datos(self.datos)
        # Adjust row/column weights for uniform layout
        for i in range(filas):
            self.frame_contenido.grid_rowconfigure(i, weight=1)
        for j in range(columnas):
            self.frame_contenido.grid_columnconfigure(j, weight=1)

        # Dynamically update the canvas size to prevent overflow
        self.frame_contenido.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def actualizar_scrollregion(self, event=None):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def calcular_color(self, subtema):
        # Calculate color based on the subtopic's state
        
        estado = sum(float(subsubtema["estado"]) for subsubtema in subtema["subsubtemas"]) / len(subtema["subsubtemas"]) if subtema["subsubtemas"] else 0
        subtema["estado"] = estado #for updating
        print("subtema\n",subtema)
        proporción_rojo = 1 - estado
        # Interpolate between green and red
        color = self.lerp_color((144, 238, 144), (255, 182, 193), proporción_rojo)
        return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"

    def lerp_color(self, color1, color2, t):
        return (
            int(color1[0] + (color2[0] - color1[0]) * t),
            int(color1[1] + (color2[1] - color1[1]) * t),
            int(color1[2] + (color2[2] - color1[2]) * t),
        )

    def anadir_subtema(self):
        ventana_entrada = tk.Toplevel(self.master)
        ventana_entrada.title("Ingrese el nombre del nuevo subtema")

        label = tk.Label(ventana_entrada, text="Nombre del Subtema:")
        label.pack(pady=10)

        entry_nombre = tk.Entry(ventana_entrada)
        entry_nombre.pack(pady=10)

        def guardar_subtema():
            nombre_subtema = entry_nombre.get()
            if nombre_subtema.strip():
                nuevo_subtema = {"id":len(self.tema["subtemas"]), "nombre": nombre_subtema, "estado": 0.0,"subsubtemas":[]}
                self.tema["subtemas"].append(nuevo_subtema)
                self.guardar_datos(self.datos)
                self.mostrar_subtemas()
            ventana_entrada.destroy()

        btn_guardar = tk.Button(ventana_entrada, text="Guardar", command=guardar_subtema)
        btn_guardar.pack(pady=10)


    def abrir_subsubtemas(self, subtema):
        """Abrir la pantalla de subsubtemas"""
        ventana_subsubtemas = tk.Toplevel(self.master)
        app_subsubtemas = PantallaSubsubtemas(ventana_subsubtemas, self.tema, subtema, self.datos, self.guardar_datos)
        app_subsubtemas.pack()
    

    def editar_tema(self):
        ventana_editar = tk.Toplevel(self.master)
        ventana_editar.title("Editar Tema")

        label = tk.Label(ventana_editar, text="Nuevo Nombre del Tema:")
        label.pack(pady=10)

        entry_nombre = tk.Entry(ventana_editar)
        entry_nombre.insert(0, self.tema["nombre"])
        entry_nombre.pack(pady=10)

        def guardar_cambios():
            nuevo_nombre = entry_nombre.get()
            if nuevo_nombre.strip():
                self.tema["nombre"] = nuevo_nombre
                self.guardar_datos(self.datos)
                self.label_titulo.config(text=nuevo_nombre)
            ventana_editar.destroy()

        btn_guardar = tk.Button(ventana_editar, text="Guardar", command=guardar_cambios)
        btn_guardar.pack(pady=10)

    def eliminar_tema(self):
        confirmacion = tk.Toplevel(self.master)
        confirmacion.title("Confirmar Eliminación")

        label = tk.Label(confirmacion, text=f"¿Está seguro de eliminar el tema '{self.tema['nombre']}'?")
        label.pack(pady=10)

        def confirmar_eliminacion():
            self.datos["temas"].remove(self.tema)
            self.guardar_datos(self.datos)
            self.master.destroy()
            confirmacion.destroy()

        btn_confirmar = tk.Button(confirmacion, text="Sí, Eliminar", command=confirmar_eliminacion)
        btn_confirmar.pack(side="left", padx=10, pady=10)

        btn_cancelar = tk.Button(confirmacion, text="Cancelar", command=confirmacion.destroy)
        btn_cancelar.pack(side="right", padx=10, pady=10)
