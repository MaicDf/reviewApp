import tkinter as tk
from tkinter import simpledialog, messagebox

# Suponiendo que 'PantallaSubsubtemas' ya está definida correctamente en otro archivo
# from subsubtemas import PantallaSubsubtemas

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

        # Mostrar el tema con opciones de editar y eliminar
        self.mostrar_tema()

        # Botón para añadir un subtema
        self.btn_anadir_subtema = tk.Button(self, text="Añadir Subtema", command=self.anadir_subtema)
        self.btn_anadir_subtema.pack()

        self.frame_contenido.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))

    def mostrar_tema(self):
        """Mostrar el nombre del tema y botones para editar y eliminar."""
        # Mostrar nombre del tema
        nombre_tema = tk.Label(self.frame_contenido, text=self.tema["nombre"], font=("Arial", 16))
        nombre_tema.pack(pady=10)

        # Botón para editar el nombre del tema
        btn_editar = tk.Button(self.frame_contenido, text="Editar Nombre", command=self.editar_nombre_tema)
        btn_editar.pack(pady=5)

        # Botón para eliminar el tema
        btn_eliminar = tk.Button(self.frame_contenido, text="Eliminar Tema", command=self.eliminar_tema)
        btn_eliminar.pack(pady=5)

        # Mostrar subtemas
        self.mostrar_subtemas()

    def mostrar_subtemas(self):
        """Mostrar los subtemas existentes"""
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

        self.mostrar_tema()

        # Crear botones de subtemas
        for subtema in self.tema["subtemas"]:
            btn_subtema = tk.Button(self.frame_contenido, text=subtema["nombre"], 
                                    bg=self.calcular_color(subtema["subsubtemas"]),
                                    command=lambda subtema=subtema: self.abrir_subsubtemas(subtema))
            btn_subtema.pack(fill="x", pady=5)

    def anadir_subtema(self):
        """Añadir un subtema con nombre"""
        # Pedir el nombre del nuevo subtema
        nombre_subtema = simpledialog.askstring("Nuevo Subtema", "Ingrese el nombre del subtema:")
        
        if nombre_subtema and nombre_subtema.strip():
            nuevo_subtema = {"nombre": nombre_subtema, "estado":"0","subsubtemas": []}
            self.tema["subtemas"].append(nuevo_subtema)
            self.guardar_datos(self.datos)
            self.mostrar_subtemas()
        else:
            messagebox.showwarning("Advertencia", "Debe ingresar un nombre para el subtema.")

    def abrir_subsubtemas(self, subtema):
        """Abrir la pantalla de subsubtemas"""
        ventana_subsubtemas = tk.Toplevel(self.master)
        app_subsubtemas = PantallaSubsubtemas(ventana_subsubtemas, subtema, self.datos, self.guardar_datos)
        app_subsubtemas.pack()

    def editar_nombre_tema(self):
        """Editar el nombre del tema"""
        nuevo_nombre = simpledialog.askstring("Editar Nombre", "Ingrese el nuevo nombre del tema:", initialvalue=self.tema["nombre"])
        
        if nuevo_nombre and nuevo_nombre.strip():
            self.tema["nombre"] = nuevo_nombre
            self.guardar_datos(self.datos)
            self.mostrar_subtemas()
        else:
            messagebox.showwarning("Advertencia", "Debe ingresar un nombre válido.")

    def eliminar_tema(self):
        """Eliminar el tema"""
        respuesta = messagebox.askyesno("Confirmación", "¿Está seguro que desea eliminar este tema?")
        
        if respuesta:
            self.datos["temas"].remove(self.tema)
            self.guardar_datos(self.datos)
            self.master.destroy()  # Cerrar la ventana actual y volver a la pantalla principal
        else:
            messagebox.showinfo("Cancelado", "La eliminación ha sido cancelada.")

    def calcular_color(self, subsubtemas):
        """Calcular el color basado en los subsubtemas"""
        total = len(subsubtemas)
        verde = rojo = 0
        for subsubtema in subsubtemas:
            if subsubtema["estado"] == "onTime":
                verde += 1
            elif subsubtema["estado"] == "overDue":
                rojo += 1

        proporción_verde = verde / total if total > 0 else 0
        proporción_rojo = rojo / total if total > 0 else 0

        # Escala de colores de verde claro a rojo claro
        color = self.lerp_color((144, 238, 144), (255, 182, 193), proporción_rojo)
        return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"

    def lerp_color(self, color1, color2, t):
        """Interpolación lineal entre dos colores"""
        return (
            int(color1[0] + (color2[0] - color1[0]) * t),
            int(color1[1] + (color2[1] - color1[1]) * t),
            int(color1[2] + (color2[2] - color1[2]) * t),
        )
