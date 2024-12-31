import tkinter as tk
from temas import PantallaTemas
import json

#print(datos['temas'][0]['subtemas']): this way we can access to the data
def cargar_datos():
    try:
        with open("playgroundFiles/dataTest.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"temas": []}

# Guardar datos en el archivo JSON
def guardar_datos(data):
    with open("playgroundFiles/dataTest.json", "w") as file:
        json.dump(data, file, indent=4)

def main():
    datos = cargar_datos()
    root = tk.Tk() #creates the widonw
    root.title("Gestor de Temas")        
    app = PantallaTemas(root, datos, guardar_datos)
    app.pack() #adds the widget to the window
    root.mainloop() #Wait for user actions to update interface

if __name__ == "__main__":
    main()