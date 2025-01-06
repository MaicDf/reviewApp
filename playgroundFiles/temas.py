import tkinter as tk
from subtemas import PantallaSubtemas
from utils import update_estados

class PantallaTemas(tk.Frame):
    def __init__(self, master, datos, guardar_datos):
        super().__init__(master)
        self.master = master
        self.datos = datos
        self.guardar_datos = guardar_datos
        # Bind <FocusIn> to self.actualizarVista using a lambda to call it when the event occurs
        self.master.bind("<FocusIn>", lambda event: self.actualizarVista())        
        self.crear_widgets()
        

    def crear_widgets(self):
        #this is supposed to update the view each time is focused on
        update_estados(self.datos,self.guardar_datos)
        # Set window title
        self.master.title("Temas - (" + str(len(self.datos["temas"])) + ")")

        self.temas_frame = tk.Frame(self)
        self.temas_frame.pack(fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.temas_frame, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.canvas = tk.Canvas(self.temas_frame, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar.config(command=self.canvas.yview)

        self.frame_contenido = tk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.frame_contenido, anchor="nw")

        
        self.mostrar_temas()

        self.btn_anadir_tema = tk.Button(self, text="Añadir Tema", command=self.anadir_tema)
        self.btn_anadir_tema.pack()
        
        self.btn_anadir_tema = tk.Button(self, text="Actualizar", command=self.mostrar_temas)
        self.btn_anadir_tema.pack()


        self.frame_contenido.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(
            self.canvas_window, width=e.width
        ))

    def mostrar_temas(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

        total_temas = len(self.datos["temas"])
        if total_temas == 0:
            return

        # Sort the 'temas' list alphanumerically by the "nombre" field
        self.datos["temas"].sort(key=lambda tema: tema["nombre"].lower())

        filas = (total_temas // 4) + (1 if total_temas % 4 != 0 else 0)

        for index, tema in enumerate(self.datos["temas"]):
            fila = index // 4
            columna = index % 4

            btn_tema = tk.Button(self.frame_contenido, text=tema["nombre"], 
                                bg=self.calcular_color(tema["subtemas"]), 
                                command=lambda tema=tema: self.abrir_subtemas(tema))
            btn_tema.grid(row=fila, column=columna, sticky="nsew", padx=5, pady=5)

        for i in range(filas):
            self.frame_contenido.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.frame_contenido.grid_columnconfigure(j, weight=1, minsize=100)

        self.frame_contenido.update_idletasks()
        canvas_width = self.frame_contenido.winfo_reqwidth()
        self.canvas.config(scrollregion=self.canvas.bbox("all"), width=canvas_width)
        self.guardar_datos(self.datos)

    def anadir_tema(self):
        ventana_entrada = tk.Toplevel(self.master)
        ventana_entrada.title("Ingrese el nombre del nuevo tema")

        label = tk.Label(ventana_entrada, text="Nombre del Tema:")
        label.pack(pady=10)

        entry_nombre = tk.Entry(ventana_entrada)
        entry_nombre.pack(pady=10)

        def guardar_tema():
            nombre_tema = entry_nombre.get()
            if nombre_tema.strip():
                nuevo_tema = {"id":len(self.datos["temas"]),"nombre": nombre_tema, "subtemas": []}
                self.datos["temas"].append(nuevo_tema)
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
        total = len(subtemas)
        sumEstados = sum(float(subtema["estado"]) for subtema in subtemas)
        proporcion_verde = sumEstados / total if total > 0 else 0
        proporcion_rojo = 1 - proporcion_verde if total > 0 else 0

        color = self.lerp_color((144, 238, 144), (255, 182, 193), proporcion_rojo)
        return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"

    def lerp_color(self, color1, color2, t):
        return (
            int(color1[0] + (color2[0] - color1[0]) * t),
            int(color1[1] + (color2[1] - color1[1]) * t),
            int(color1[2] + (color2[2] - color1[2]) * t),
        )


    def actualizarVista(self):
        update_estados(self.datos,self.guardar_datos)
        if self.frame_contenido:
            self.mostrar_temas()
        else:
            print("frame_contenido no está inicializado todavía.")
            
