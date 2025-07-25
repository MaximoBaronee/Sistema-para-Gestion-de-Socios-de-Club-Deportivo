import tkinter as tk
from tkinter import ttk, messagebox
from database import ejecutar_consulta
from socios import agregar_socio, eliminar_socio, obtener_socios

def crear_interfaz_socios(ventana_socios):
    ventana_socios.title("Gestión de Socios")
    ventana_socios.geometry("800x600")
    
    # Frame principal
    frame_principal = tk.Frame(ventana_socios)
    frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Frame para el formulario
    frame_form = tk.Frame(frame_principal)
    frame_form.pack(fill=tk.X, pady=(0, 10))
    
    # Campos del formulario
    tk.Label(frame_form, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_nombre = tk.Entry(frame_form, width=30)
    entry_nombre.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(frame_form, text="DNI:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_dni = tk.Entry(frame_form, width=20)
    entry_dni.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    
    tk.Label(frame_form, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_telefono = tk.Entry(frame_form, width=20)
    entry_telefono.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    
    # Frame para la tabla
    frame_tabla = tk.Frame(frame_principal)
    frame_tabla.pack(fill=tk.BOTH, expand=True)
    
    # Configurar Treeview
    tree = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "DNI", "Teléfono"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("DNI", text="DNI")
    tree.heading("Teléfono", text="Teléfono")
    
    tree.column("ID", width=50, anchor="center")
    tree.column("Nombre", width=200)
    tree.column("DNI", width=100, anchor="center")
    tree.column("Teléfono", width=100, anchor="center")
    
    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Frame para botones
    frame_botones = tk.Frame(frame_principal)
    frame_botones.pack(fill=tk.X, pady=(10, 0))
    
    # Botones
    btn_agregar = tk.Button(
        frame_botones,
        text="Agregar Socio",
        command=lambda: agregar_socio_interfaz(entry_nombre, entry_dni, entry_telefono, tree),
        bg="#28a745",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=10,
        pady=5
    )
    btn_agregar.pack(side=tk.LEFT, padx=5)
    
    btn_eliminar = tk.Button(
        frame_botones,
        text="Eliminar Socio",
        command=lambda: eliminar_socio_interfaz(tree),
        bg="#dc3545",
        fg="white",
        font=("Arial", 10),
        padx=10,
        pady=5
    )
    btn_eliminar.pack(side=tk.LEFT, padx=5)
    
    btn_volver = tk.Button(
        frame_botones,
        text="Volver al Menú",
        command=ventana_socios.destroy,
        bg="#6c757d",
        fg="white",
        font=("Arial", 10),
        padx=10,
        pady=5
    )
    btn_volver.pack(side=tk.RIGHT, padx=5)
    
    # Cargar datos iniciales
    listar_socios_interfaz(tree)
    
    return tree

def agregar_socio_interfaz(entry_nombre, entry_dni, entry_telefono, tree):
    nombre = entry_nombre.get().strip()
    dni = entry_dni.get().strip()
    telefono = entry_telefono.get().strip()
    
    if not nombre or not dni:
        messagebox.showerror("Error", "Nombre y DNI son obligatorios")
        return
    
    try:
        # Agregar con membresía mensual y estado activo por defecto
        agregar_socio(nombre, dni, telefono, "Mensual", "Activo")
        messagebox.showinfo("Éxito", "Socio agregado correctamente")
        listar_socios_interfaz(tree)
        
        # Limpiar campos
        entry_nombre.delete(0, tk.END)
        entry_dni.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar el socio: {str(e)}")

def eliminar_socio_interfaz(tree):
    seleccionado = tree.selection()
    if not seleccionado:
        messagebox.showwarning("Advertencia", "Seleccione un socio para eliminar")
        return
    
    id_socio = tree.item(seleccionado[0])['values'][0]
    nombre = tree.item(seleccionado[0])['values'][1]
    
    if messagebox.askyesno("Confirmar", f"¿Eliminar al socio {nombre}?"):
        try:
            eliminar_socio(id_socio)
            messagebox.showinfo("Éxito", "Socio eliminado correctamente")
            listar_socios_interfaz(tree)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el socio: {str(e)}")

def listar_socios_interfaz(tree):
    try:
        socios = obtener_socios()
        tree.delete(*tree.get_children())
        for socio in socios:
            tree.insert("", "end", values=socio)
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar socios: {str(e)}")