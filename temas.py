# temas.py
import tkinter as tk
from tkinter import ttk
from subtemas import manejar_subtemas

temas = {
    "Python": ["Variables", "Funciones", "POO"],
    "JavaScript": ["Eventos", "POO", "Bloques básicos"],
    "React": ["Componentes", "Hooks"],
    "SQL": ["SELECT", "JOIN", "Funciones"],
    "AWS": ["EC2", "S3", "Lambda"]
}

def manejar_temas(ventana):
    # Marco para el área con scrollbar
    frame_principal = tk.Frame(ventana)
    frame_principal.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(frame_principal)
    scrollbar = ttk.Scrollbar(frame_principal, orient=tk.VERTICAL, command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Función para actualizar los recuadros de temas
    def actualizar_recuadros():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()  # Eliminar recuadros existentes

        for i, tema in enumerate(temas.keys()):
            boton = tk.Button(
                scrollable_frame,
                text=tema,
                width=20,
                height=5,
                command=lambda t=tema: manejar_subtemas(ventana, t, temas[t])
            )
            boton.grid(row=i // 3, column=i % 3, padx=10, pady=10)

    # Botón para añadir temas
    def añadir_tema():
        nuevo_tema = f"Tema {len(temas) + 1}"
        temas[nuevo_tema] = []  # Crear el nuevo tema con una lista vacía de subtemas
        actualizar_recuadros()

    boton_añadir = tk.Button(ventana, text="Añadir Tema", command=añadir_tema)
    boton_añadir.pack(pady=10)

    # Actualizar los recuadros iniciales
    actualizar_recuadros()
