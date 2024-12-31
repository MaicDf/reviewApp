import tkinter as tk
from tkinter import ttk
from subsubtemas import manejar_subsubtemas  # Asegúrate de que este archivo existe

def manejar_subtemas(ventana, tema, subtemas):
    # Crear una nueva ventana para el tema
    ventana_tema = tk.Toplevel(ventana)
    ventana_tema.title(f"Subtemas de {tema}")
    ventana_tema.geometry("600x400")

    frame_tema = tk.Frame(ventana_tema)
    frame_tema.pack(fill=tk.BOTH, expand=True)

    canvas_tema = tk.Canvas(frame_tema)
    scrollbar_tema = ttk.Scrollbar(frame_tema, orient=tk.VERTICAL, command=canvas_tema.yview)
    scrollable_frame_tema = tk.Frame(canvas_tema)

    scrollable_frame_tema.bind(
        "<Configure>",
        lambda e: canvas_tema.configure(scrollregion=canvas_tema.bbox("all"))
    )

    canvas_tema.create_window((0, 0), window=scrollable_frame_tema, anchor="nw")
    canvas_tema.configure(yscrollcommand=scrollbar_tema.set)

    canvas_tema.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_tema.pack(side=tk.RIGHT, fill=tk.Y)

    # Función para actualizar la lista de subtemas
    def actualizar_subtemas():
        for widget in scrollable_frame_tema.winfo_children():
            widget.destroy()  # Eliminar botones existentes

        for i, subtema in enumerate(subtemas):
            boton = tk.Button(
                scrollable_frame_tema,
                text=subtema,
                width=40,
                command=lambda s=subtema: manejar_subsubtemas(ventana, s, [])  # Llamada a manejar_subsubtemas
            )
            boton.grid(row=i, column=0, pady=5, padx=10)

        # Centrar el contenedor de los botones
        scrollable_frame_tema.grid_columnconfigure(0, weight=1)

    # Botón para añadir subtemas
    def añadir_subtema():
        nuevo_subtema = f"Subtema {len(subtemas) + 1}"
        subtemas.append(nuevo_subtema)
        actualizar_subtemas()

    # Botón para añadir un nuevo subtema
    boton_añadir_tema = tk.Button(ventana_tema, text="Añadir Subtema", command=añadir_subtema)
    boton_añadir_tema.pack(pady=10)

    # Actualizar la lista de subtemas
    actualizar_subtemas()
