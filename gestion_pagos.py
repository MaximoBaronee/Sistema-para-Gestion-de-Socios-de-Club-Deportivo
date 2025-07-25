import tkinter as tk
from tkinter import ttk, messagebox
from socios import obtener_socios_con_pagos, actualizar_estado_pago

def crear_interfaz_pagos(ventana_pagos):
    # Frame principal
    frame_principal = tk.Frame(ventana_pagos)
    frame_principal.pack(fill=tk.BOTH, expand=True)
    
    # Frame para la tabla (arriba)
    frame_tabla = tk.Frame(frame_principal)
    frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))
    
    # Configuración del Treeview
    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 11), rowheight=30)
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
    
    tree = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "DNI", "Estado"), show="headings")
    tree.heading("ID", text="ID", anchor="center")
    tree.heading("Nombre", text="Nombre", anchor="w")
    tree.heading("DNI", text="DNI", anchor="center")
    tree.heading("Estado", text="Estado Pago", anchor="center")
    
    tree.column("ID", width=60, anchor="center")
    tree.column("Nombre", width=250, anchor="w")
    tree.column("DNI", width=120, anchor="center")
    tree.column("Estado", width=120, anchor="center")
    
    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.tag_configure('pagado', background='#d4edda', foreground='#155724')
    tree.tag_configure('pendiente', background='#f8d7da', foreground='#721c24')
    
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Frame para los botones (abajo)
    frame_botones = tk.Frame(frame_principal)
    frame_botones.pack(fill=tk.X, padx=10, pady=10)
    
    return tree, frame_botones

def configurar_botones(frame_botones, tree):
    # Configurar el frame para organizar botones verticalmente
    frame_botones.grid_columnconfigure(0, weight=1)  # Centrar los botones
    
    # Botón Cambiar Estado (arriba)
    btn_cambiar = tk.Button(
        frame_botones,
        text="Cambiar Estado",
        command=lambda: cambiar_estado_pago(tree),
        bg="#4e73df",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=15,
        pady=5,
        relief=tk.GROOVE,
        borderwidth=2,
        width=15
    )
    btn_cambiar.grid(row=0, column=0, pady=(0, 10))  # Margen inferior de 10px
    
    # Botón Volver (abajo)
    btn_volver = tk.Button(
        frame_botones,
        text="Volver al Menú",
        command=frame_botones.master.master.destroy,
        bg="#6c757d",
        fg="white",
        font=("Arial", 10),
        padx=15,
        pady=5,
        relief=tk.GROOVE,
        borderwidth=2,
        width=15
    )
    btn_volver.grid(row=1, column=0)  # Debajo del primer botón

def cargar_socios(tree):
    try:
        socios = obtener_socios_con_pagos()
        tree.delete(*tree.get_children())
        for socio in socios:
            id_socio, nombre, dni, estado = socio
            tags = ('pagado',) if estado == "Pagado" else ('pendiente',)
            tree.insert("", "end", values=(id_socio, nombre, dni, estado), tags=tags)
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar socios: {str(e)}")

def cambiar_estado_pago(tree):
    seleccionado = tree.selection()
    if not seleccionado:
        messagebox.showwarning("Advertencia", "Seleccione un socio primero")
        return
        
    item = seleccionado[0]
    valores = tree.item(item, 'values')
    id_socio = valores[0]
    nombre = valores[1]
    estado_actual = valores[3]
    
    nuevo_estado = "Pendiente" if estado_actual == "Pagado" else "Pagado"
    
    if not messagebox.askyesno(
        "Confirmar cambio", 
        f"¿Cambiar estado de pago de {nombre} a '{nuevo_estado}'?"
    ):
        return
        
    try:
        if actualizar_estado_pago(id_socio, nuevo_estado):
            # Actualizar visualización
            nuevos_valores = list(valores)
            nuevos_valores[3] = nuevo_estado
            tree.item(item, values=nuevos_valores)
            
            # Actualizar color
            tags = ('pagado',) if nuevo_estado == "Pagado" else ('pendiente',)
            tree.item(item, tags=tags)
            
            messagebox.showinfo("Éxito", f"Estado de {nombre} actualizado a '{nuevo_estado}'")
        else:
            messagebox.showerror("Error", "No se pudo guardar el cambio en la BD")
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar: {str(e)}")