import tkinter as tk
from tkinter import ttk, messagebox
from socios import obtener_socios, agregar_socio, eliminar_socio

def crear_interfaz(root):
    """Crea la interfaz gráfica para la gestión de socios."""
    frame = ttk.Frame(root)
    frame.pack(padx=10, pady=10, fill="both", expand=True)
    
    # Tabla para mostrar socios
    columnas = ("ID", "Nombre", "DNI", "Teléfono", "Membresía", "Estado")
    tree = ttk.Treeview(frame, columns=columnas, show="headings")
    for col in columnas:
        tree.heading(col, text=col)
    tree.pack(fill="both", expand=True)
    
    def actualizar_lista():
        for row in tree.get_children():
            tree.delete(row)
        socios = obtener_socios()
        for socio in socios:
            tree.insert("", "end", values=socio)
    
    actualizar_lista()
    
    # Botón para agregar socio
    def agregar():
        agregar_socio("Nuevo Socio", "12345678", "123456789", "Mensual", "Activo")
        actualizar_lista()
    
    btn_agregar = ttk.Button(frame, text="Agregar Socio", command=agregar)
    btn_agregar.pack(pady=5)
    
    # Botón para eliminar socio
    def eliminar():
        seleccionado = tree.selection()
        if seleccionado:
            id_socio = tree.item(seleccionado)['values'][0]
            eliminar_socio(id_socio)
            actualizar_lista()
        else:
            messagebox.showerror("Error", "Seleccione un socio para eliminar")
    
    btn_eliminar = ttk.Button(frame, text="Eliminar Socio", command=eliminar)
    btn_eliminar.pack(pady=5)
