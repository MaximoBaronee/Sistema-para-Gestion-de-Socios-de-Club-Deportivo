import tkinter as tk
from tkinter import ttk, messagebox
from database import ejecutar_consulta
from socios import agregar_socio, eliminar_socio, obtener_socios

def crear_interfaz_socios(ventana_socios):
    ventana_socios.title("Gestión de Socios")
    ventana_socios.geometry("800x600")
    
    # Frame principal (solo usa pack)
    frame_principal = tk.Frame(ventana_socios)
    frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Frame para el formulario (centrado con pack)
    frame_form = tk.Frame(frame_principal)
    frame_form.pack(pady=(0, 15), anchor='center')
    
    # Frame para campos (centrado)
    frame_campos = tk.Frame(frame_form)
    frame_campos.pack()
    
    # Nombre
    frame_nombre = tk.Frame(frame_campos)
    frame_nombre.pack(pady=5)
    tk.Label(frame_nombre, text="Nombre:").pack(side=tk.LEFT, padx=5)
    entry_nombre = tk.Entry(frame_nombre, width=30)
    entry_nombre.pack(side=tk.LEFT)
    
    # DNI
    frame_dni = tk.Frame(frame_campos)
    frame_dni.pack(pady=5)
    tk.Label(frame_dni, text="DNI:").pack(side=tk.LEFT, padx=5)
    entry_dni = tk.Entry(frame_dni, width=20)
    entry_dni.pack(side=tk.LEFT)
    
    # Teléfono
    frame_telefono = tk.Frame(frame_campos)
    frame_telefono.pack(pady=5)
    tk.Label(frame_telefono, text="Teléfono:").pack(side=tk.LEFT, padx=5)
    entry_telefono = tk.Entry(frame_telefono, width=20)
    entry_telefono.pack(side=tk.LEFT)
    
    # Frame para la tabla
    frame_tabla = tk.Frame(frame_principal)
    frame_tabla.pack(fill=tk.BOTH, expand=True)
    
    # Configurar Treeview (solo pack)
    tree = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "DNI", "Teléfono"), show="headings")
    tree.heading("ID", text="ID", anchor="center")
    tree.heading("Nombre", text="Nombre", anchor="w")
    tree.heading("DNI", text="DNI", anchor="center")
    tree.heading("Teléfono", text="Teléfono", anchor="center")
    
    tree.column("ID", width=50, anchor="center")
    tree.column("Nombre", width=200)
    tree.column("DNI", width=100, anchor="center")
    tree.column("Teléfono", width=100, anchor="center")
    
    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Frame para botones principales (centrado)
    frame_botones_accion = tk.Frame(frame_principal)
    frame_botones_accion.pack(pady=(10, 5), anchor='center')
    
    # Botones de acción (solo pack)
    btn_agregar = tk.Button(
        frame_botones_accion,
        text="Agregar Socio",
        command=lambda: agregar_socio_interfaz(entry_nombre, entry_dni, entry_telefono, tree),
        bg="#28a745",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=15,
        pady=5
    )
    btn_agregar.pack(side=tk.LEFT, padx=10)
    
    btn_eliminar = tk.Button(
        frame_botones_accion,
        text="Eliminar Socio",
        command=lambda: eliminar_socio_interfaz(tree),
        bg="#dc3545",
        fg="white",
        font=("Arial", 10),
        padx=15,
        pady=5
    )
    btn_eliminar.pack(side=tk.LEFT, padx=10)
    
    # Frame para botón volver (centrado abajo)
    frame_boton_volver = tk.Frame(frame_principal)
    frame_boton_volver.pack(pady=(5, 10), anchor='center')
    
    btn_volver = tk.Button(
        frame_boton_volver,
        text="Volver al Menú",
        command=ventana_socios.destroy,
        bg="#6c757d",
        fg="white",
        font=("Arial", 10),
        padx=15,
        pady=5,
        width=15
    )
    btn_volver.pack()
    
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