import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter.scrolledtext import ScrolledText
from datetime import timedelta, date
from utils import RichTextEditor

class PantallaDetalles(tk.Frame):
    def __init__(self, master, tema, subtema, subsubtema, datos, guardar_datos):
        super().__init__(master)
        self.master = master
        self.subsubtema = subsubtema
        self.datos = datos
        self.guardar_datos = guardar_datos
        self.tema = tema
        self.subtema = subtema

        self.master.geometry("700x800")  # Increased height for more space
        self.crear_widgets()

    def crear_widgets(self):
        self.master.title("Details")
        # Title
        title_label = tk.Label(self, text=self.subsubtema["nombre"], font=("Arial", 20), anchor="center")
        title_label.pack(pady=10)

        # Edit Name Button
        edit_name_button = tk.Button(self, text="🖉 Edit Name", command=lambda: self.editar_subsubtema(title_label))
        edit_name_button.pack(pady=5)

        # Atomic Task Label and Edit Icon
        atomic_task_frame = tk.Frame(self)
        atomic_task_frame.pack(anchor="w", fill="x", padx=10, pady=5)

        edit_atomic_task_button = tk.Button(atomic_task_frame, text="🖉", command=self.editar_atomic_task)
        edit_atomic_task_button.pack(side="left", padx=5)

        self.atomic_task_label = tk.Label(atomic_task_frame, text="Atomic Task: " + self.subsubtema.get("atomic_task", ""))
        self.atomic_task_label.pack(side="left")

        # Hint Label and Edit Icon (New Hint Field)
        hint_frame = tk.Frame(self)
        hint_frame.pack(anchor="w", fill="x", padx=10, pady=5)

        edit_hint_button = tk.Button(hint_frame, text="🖉", command=self.editar_hint)
        edit_hint_button.pack(side="left", padx=5)

        self.hint_label = tk.Label(hint_frame, text="Hint: " + self.subsubtema.get("hint", ""))
        self.hint_label.pack(side="left")

        # Concept/Active Recall Text Area and Edit Icon
        concept_frame = tk.Frame(self)
        concept_frame.pack(anchor="w", fill="x", padx=10, pady=5)

        edit_concept_button = tk.Button(concept_frame, text="🖉", command=self.editar_concept)
        edit_concept_button.pack(side="left", padx=5)

        concept_label = tk.Label(concept_frame, text="Concept(Active Recall):")
        concept_label.pack(side="left")
         
        self.concept_text = RichTextEditor(self, wrap=tk.WORD, height=15, width=80, bg="white", undo=True)  # Increased height and width
        self.concept_text.pack(fill="both", expand=True, padx=10, pady=5)

        # Insert concept text
        concept_content = self.subsubtema["concept"]

        self.concept_text.delete("1.0", tk.END)
        self.concept_text.insert("1.0", concept_content)

        # Show Button
        self.show_button = tk.Button(self, text="Show", command=self.mostrar_concepto)
        self.show_button.pack(pady=5)

        # Done Buttons
        self.done_button = tk.Button(self, text="Done (Default)", command=self.configurar_repaso_default)
        self.done_button.pack(pady=5)

        self.done_custom_button = tk.Button(self, text="Done (Custom)", command=self.configurar_repaso_custom)
        self.done_custom_button.pack(pady=5)

        # Save Button
        save_button = tk.Button(self, text="Save", command=self.save_fields, bg="green", fg="white")
        save_button.pack(pady=10)

        # Delete Button
        delete_button = tk.Button(self, text="Delete", command=self.eliminar_subsubtema, bg="red", fg="white")
        delete_button.pack(pady=10)

    def editar_subsubtema(self, tittle_label):
        """Function to edit the name of the subsubtema"""
        ventana_editar = tk.Toplevel(self.master)
        ventana_editar.title("Editar Subsubtema")

        label = tk.Label(ventana_editar, text="Nuevo Nombre del Subsubtema:")
        label.pack(pady=10)

        entry_nombre = tk.Entry(ventana_editar)
        entry_nombre.insert(0, self.subsubtema["nombre"])
        entry_nombre.pack(pady=10)

        def guardar_cambios():
            nuevo_nombre = entry_nombre.get()
            if nuevo_nombre.strip():
                self.subsubtema["nombre"] = nuevo_nombre
                self.guardar_datos(self.datos)
                tittle_label.config(text=nuevo_nombre)
            ventana_editar.destroy()

        btn_guardar = tk.Button(ventana_editar, text="Guardar", command=guardar_cambios)
        btn_guardar.pack(pady=10)
        
    def editar_atomic_task(self):
        nuevo_valor = simpledialog.askstring("Edit Atomic Task", "Enter new atomic task:")
        if nuevo_valor:
            self.subsubtema["atomic_task"] = nuevo_valor
            self.atomic_task_label.config(text="Atomic Task: " + nuevo_valor)

    def editar_hint(self):
        nuevo_valor = simpledialog.askstring("Edit Hint", "Enter new hint:")
        if nuevo_valor:
            self.subsubtema["hint"] = nuevo_valor
            self.hint_label.config(text="Hint: " + nuevo_valor)

    def editar_concept(self):
        self.concept_text.config(state="normal", bg="white")
        self.concept_text.focus_set()

    def mostrar_concepto(self):
        self.concept_text.config(state="normal", bg="white")

    def configurar_repaso_default(self):
        self.subsubtema["deadline"] = (date.today() + timedelta(days=30)).strftime('%Y-%m-%d')
        self.guardar_datos(self.datos)
        self.master.destroy()

    def configurar_repaso_custom(self):
        dias = simpledialog.askinteger("Custom Days", "Enter the number of days:")
        if dias is not None:
            self.subsubtema["deadline"] = (date.today() + timedelta(days=dias)).strftime('%Y-%m-%d')
            self.guardar_datos(self.datos)
        self.master.destroy()

    def save_fields(self):
        # Save atomic task and concept
        self.subsubtema["concept"] = self.concept_text.get("1.0", "end-1c").strip()
        self.guardar_datos(self.datos)
        messagebox.showinfo("Save Successful", "The changes have been saved successfully!")
        self.master.destroy()

    def eliminar_subsubtema(self):
        confirm = messagebox.askyesno("Delete Subsubtema", "Are you sure you want to delete this subsubtema?")
        if confirm:
            self.datos["temas"][self.tema['id']]["subtemas"][self.subtema['id']]['subsubtemas'].remove(self.subsubtema)
            self.guardar_datos(self.datos)
            self.master.destroy()
