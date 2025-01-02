import tkinter as tk
#from subsubsubtemas import PantallaSubsubsubtemas

class PantallaSubsubtemas(tk.Frame):
    def __init__(self, master, tema, subtema, datos, guardar_datos):
        super().__init__(master)
        self.master = master
        self.subtema = subtema
        self.datos = datos
        self.guardar_datos = guardar_datos
        self.crear_widgets()
        self.subsubtemas_frame = tk.Frame(self, width=450)
        self.subsubtemas_frame.pack(fill="both", expand=True)
        self.tema=tema
        
    def crear_widgets(self):
        self.label_titulo = tk.Label(self, text=self.subtema["nombre"], font=("Arial", 16, "bold"))
        self.label_titulo.pack(pady=10)

        self.subsubtemas_frame = tk.Frame(self)
        self.subsubtemas_frame.pack(fill="both", expand=True)

        # Scrollbars for horizontal and vertical scrolling
        self.scrollbar_y = tk.Scrollbar(self.subsubtemas_frame, orient="vertical")
        self.scrollbar_y.pack(side="right", fill="y")

        self.scrollbar_x = tk.Scrollbar(self.subsubtemas_frame, orient="horizontal")
        self.scrollbar_x.pack(side="bottom", fill="x")

        # Canvas for dynamic content
        self.canvas = tk.Canvas(
            self.subsubtemas_frame, 
            yscrollcommand=self.scrollbar_y.set, 
            xscrollcommand=self.scrollbar_x.set
        )
        self.canvas.pack(side="left", fill="both", expand=True)

        # Configure scrollbars
        self.scrollbar_y.config(command=self.canvas.yview)
        self.scrollbar_x.config(command=self.canvas.xview)

        self.frame_contenido = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_contenido, anchor="nw")

        # Display subsubtopics
        self.mostrar_subsubtemas()

        # Buttons for actions
        self.btn_anadir_subsubtema = tk.Button(self, text="Añadir Subsubtema", command=self.anadir_subsubtema)
        self.btn_anadir_subsubtema.pack(pady=5)

        self.btn_editar_subtema = tk.Button(self, text="Editar Subtema", command=self.editar_subtema)
        self.btn_editar_subtema.pack(pady=5)

        self.btn_eliminar_subtema = tk.Button(self, text="Eliminar Subtema", command=self.eliminar_subtema)
        self.btn_eliminar_subtema.pack(pady=5)

        self.frame_contenido.bind("<Configure>", self.actualizar_scrollregion)

    def mostrar_subsubtemas(self):
        # Clear previous widgets
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

        # Define grid layout
        if(len(self.subtema["subsubtemas"]))==0:
            return
        filas, columnas = 3, 4
        for index, subsubtema in enumerate(self.subtema["subsubtemas"]):
            fila = index // columnas
            columna = index % columnas

            # Create a button for each subsubtopic
            btn_subsubtema = tk.Button(
                self.frame_contenido,
                text=subsubtema["nombre"],
                bg=self.calcular_color(subsubtema),
                command=lambda subsubtema=subsubtema: self.abrir_subsubsubtemas(subsubtema))
            
            btn_subsubtema.grid(row=fila, column=columna, sticky="nsew", padx=5, pady=5)

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


    def calcular_color(self, subsubtema):
        # Attempt to convert the "estado" value to a float. If it fails, default to 0.0.
        try:
            estado = float(subsubtema.get("estado", 0.0))
        except ValueError:
            # Handle invalid state values by defaulting to 0.0 (you can modify this as needed)
            estado = 0.0

        proporción_verde = estado
        proporción_rojo = 1 - estado

        # Interpolate between green and red using lerp_color
        color = self.lerp_color((144, 238, 144), (255, 182, 193), proporción_rojo)
        return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"

    def lerp_color(self, color1, color2, t):
        """
        Linearly interpolate between two colors.
        color1, color2: tuples representing RGB values (0-255)
        t: a float between 0 and 1 representing the interpolation factor
        """
        return (
            int(color1[0] + (color2[0] - color1[0]) * t),
            int(color1[1] + (color2[1] - color1[1]) * t),
            int(color1[2] + (color2[2] - color1[2]) * t),
        )

    def anadir_subsubtema(self):
        ventana_entrada = tk.Toplevel(self.master)
        ventana_entrada.title("Ingrese el nombre del nuevo subsubtema")

        label = tk.Label(ventana_entrada, text="Nombre del Subsubtema:")
        label.pack(pady=10)

        entry_nombre = tk.Entry(ventana_entrada)
        entry_nombre.pack(pady=10)

        def guardar_subsubtema():
            nombre_subsubtema = entry_nombre.get()
            if nombre_subsubtema.strip():
                nuevo_subsubtema = {"nombre": nombre_subsubtema, "estado": 0.0}
                self.subtema["subsubtemas"].append(nuevo_subsubtema)
                self.guardar_datos(self.datos)
                self.mostrar_subsubtemas()
            ventana_entrada.destroy()

        btn_guardar = tk.Button(ventana_entrada, text="Guardar", command=guardar_subsubtema)
        btn_guardar.pack(pady=10)

    def abrir_subsubsubtemas(self, subsubtema):
        """Abrir la pantalla de subsubsubtemas"""
        ventana_subsubsubtemas = tk.Toplevel(self.master)
        app_subsubsubtemas = PantallaSubsubsubtemas(ventana_subsubsubtemas, subsubtema, self.datos, self.guardar_datos)
        app_subsubsubtemas.pack()

    def editar_subtema(self):
        ventana_editar = tk.Toplevel(self.master)
        ventana_editar.title("Editar Subtema")

        label = tk.Label(ventana_editar, text="Nuevo Nombre del Subtema:")
        label.pack(pady=10)

        entry_nombre = tk.Entry(ventana_editar)
        entry_nombre.insert(0, self.subtema["nombre"])
        entry_nombre.pack(pady=10)

        def guardar_cambios():
            nuevo_nombre = entry_nombre.get()
            if nuevo_nombre.strip():
                self.subtema["nombre"] = nuevo_nombre
                self.guardar_datos(self.datos)
                self.label_titulo.config(text=nuevo_nombre)
            ventana_editar.destroy()

        btn_guardar = tk.Button(ventana_editar, text="Guardar", command=guardar_cambios)
        btn_guardar.pack(pady=10)

    def eliminar_subtema(self):
        confirmacion = tk.Toplevel(self.master)
        confirmacion.title("Confirmar Eliminación")

        label = tk.Label(confirmacion, text=f"¿Está seguro de eliminar el subtema '{self.subtema['nombre']}'?")
        label.pack(pady=10)

        def confirmar_eliminacion():
            print(self.datos["temas"][self.tema['id']])
            self.datos["temas"][self.tema['id']]["subtemas"].remove(self.subtema)
            self.guardar_datos(self.datos)
            self.master.destroy()
            confirmacion.destroy()

        btn_confirmar = tk.Button(confirmacion, text="Sí, Eliminar", command=confirmar_eliminacion)
        btn_confirmar.pack(side="left", padx=10, pady=10)

        btn_cancelar = tk.Button(confirmacion, text="Cancelar", command=confirmacion.destroy)
        btn_cancelar.pack(side="right", padx=10, pady=10)
