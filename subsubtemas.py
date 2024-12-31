import tkinter as tk
from tkinter import ttk

def manejar_subsubtemas(ventana, subtema, subsubtemas):
    # Crear una nueva ventana para el subtema
    ventana_subtema = tk.Toplevel(ventana)
    ventana_subtema.title(f"Subsubtemas de {subtema}")
    ventana_subtema.geometry("600x400")

    # Marco para el área con scrollbar
    frame_subtema = tk.Frame(ventana_subtema)
    frame_subtema.pack(fill=tk.BOTH, expand=True)

    canvas_subtema = tk.Canvas(frame_subtema)
    scrollbar_subtema = ttk.Scrollbar(frame_subtema, orient=tk.VERTICAL, command=canvas_subtema.yview)
    scrollable_frame_subtema = tk.Frame(canvas_subtema)

    scrollable_frame_subtema.bind(
        "<Configure>",
        lambda e: canvas_subtema.configure(scrollregion=canvas_subtema.bbox("all"))
    )

    canvas_subtema.create_window((0, 0), window=scrollable_frame_subtema, anchor="nw")
    canvas_subtema.configure(yscrollcommand=scrollbar_subtema.set)

    canvas_subtema.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_subtema.pack(side=tk.RIGHT, fill=tk.Y)

    # Función para actualizar la lista de subsubtemas
    def actualizar_subsubtemas():
        for widget in scrollable_frame_subtema.winfo_children():
            widget.destroy()  # Eliminar botones existentes

        for i, subsubtema in enumerate(subsubtemas):
            boton = tk.Button(
                scrollable_frame_subtema,
                text=subsubtema,
                width=40,
                command=lambda s=subsubtema: print(f"Seleccionaste: {s}")
            )
            boton.grid(row=i, column=0, pady=5, padx=10)

        # Centrar el contenedor de los botones
        scrollable_frame_subtema.grid_columnconfigure(0, weight=1)

    # Botón para añadir subsubtemas
    def añadir_subsubtema():
        nuevo_subsubtema = f"Subsubtema {len(subsubtemas) + 1}"
        subsubtemas.append(nuevo_subsubtema)
        actualizar_subsubtemas()

    boton_añadir_subtema = tk.Button(ventana_subtema, text="Añadir Subsubtema", command=añadir_subsubtema)
    boton_añadir_subtema.pack(pady=10)

    # Actualizar la lista de subsubtemas
    actualizar_subsubtemas()