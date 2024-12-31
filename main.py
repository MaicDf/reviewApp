# main.py
import tkinter as tk
from temas import manejar_temas

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Biblioteca de Repaso")
ventana.geometry("530x400")  # Ancho x Alto

# Ejecutar la lógica de temas en la ventana principal
manejar_temas(ventana)

# Iniciar el bucle principal
ventana.mainloop()