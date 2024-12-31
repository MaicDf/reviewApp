import tkinter as tk
from temas import PantallaTemas
import json

# Cargar datos desde el archivo JSON
def cargar_datos():
    try:
        with open("data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"temas": []}

# Guardar datos en el archivo JSON
def guardar_datos(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

def main():
    datos = cargar_datos()

    root = tk.Tk()
    root.title("Gestor de Temas")
    app = PantallaTemas(root, datos, guardar_datos)
    app.pack()

    root.mainloop()

if __name__ == "__main__":
    main()