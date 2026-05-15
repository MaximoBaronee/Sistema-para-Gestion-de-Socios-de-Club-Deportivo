import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk, messagebox
from backend.socios import obtener_socios_con_pagos, actualizar_estado_pago, buscar_socio_por_nombre, buscar_socio_por_dni, filtrar_socios_por_estado

def crear_interfaz_pagos(ventana_pagos):
    # Frame principal
    frame_principal = tk.Frame(ventana_pagos)
    frame_principal.pack(fill=tk.BOTH, expand=True)

    # Frame para búsquedas y filtros (arriba del todo)
    frame_busqueda = tk.Frame(frame_principal)
    frame_busqueda.pack(fill=tk.X, padx=10, pady=10)

    # Etiqueta y entrada para búsqueda por nombre
    lbl_nombre = tk.Label(frame_busqueda, text="Nombre:", font=("Arial", 10))
    lbl_nombre.grid(row=0, column=0, padx=(0, 5), sticky="e")

    entry_nombre = tk.Entry(frame_busqueda, font=("Arial", 10), width=30)
    entry_nombre.grid(row=0, column=1, padx=5)

    # Lupita para buscar por nombre
    btn_buscar_nombre = tk.Button(
        frame_busqueda,
        text="🔍",
        font=("Arial", 12),
        width=3,
        command=lambda: buscar_por_nombre(tree, entry_nombre.get())
    )
    btn_buscar_nombre.grid(row=0, column=2, padx=5)

    # Separador
    separador1 = tk.Label(frame_busqueda, text="|", font=("Arial", 10))
    separador1.grid(row=0, column=3, padx=10)

    # Etiqueta y entrada para búsqueda por DNI
    lbl_dni = tk.Label(frame_busqueda, text="DNI:", font=("Arial", 10))
    lbl_dni.grid(row=0, column=4, padx=(0, 5), sticky="e")

    entry_dni = tk.Entry(frame_busqueda, font=("Arial", 10), width=15)
    entry_dni.grid(row=0, column=5, padx=5)

    # Lupita para buscar por DNI
    btn_buscar_dni = tk.Button(
        frame_busqueda,
        text="🔍",
        font=("Arial", 12),
        width=3,
        command=lambda: buscar_por_dni(tree, entry_dni.get())
    )
    btn_buscar_dni.grid(row=0, column=6, padx=5)

    # Separador
    separador2 = tk.Label(frame_busqueda, text="|", font=("Arial", 10))
    separador2.grid(row=0, column=7, padx=10)

    # Etiqueta para filtros
    lbl_filtro = tk.Label(frame_busqueda, text="Filtrar por estado:", font=("Arial", 10))
    lbl_filtro.grid(row=0, column=8, padx=(0, 5), sticky="e")

    # Botón Pendiente
    btn_pendiente = tk.Button(
        frame_busqueda,
        text="Pendiente",
        command=lambda: filtrar_por_estado(tree, "Pendiente"),
        bg="#f8d7da",
        fg="#721c24",
        font=("Arial", 9, "bold"),
        padx=10,
        pady=2,
        relief=tk.GROOVE,
        borderwidth=2
    )
    btn_pendiente.grid(row=0, column=9, padx=5)

    # Botón Pagado
    btn_pagado = tk.Button(
        frame_busqueda,
        text="Pagado",
        command=lambda: filtrar_por_estado(tree, "Pagado"),
        bg="#d4edda",
        fg="#155724",
        font=("Arial", 9, "bold"),
        padx=10,
        pady=2,
        relief=tk.GROOVE,
        borderwidth=2
    )
    btn_pagado.grid(row=0, column=10, padx=5)

    # Botón Todos
    btn_todos = tk.Button(
        frame_busqueda,
        text="Todos",
        command=lambda: cargar_socios(tree),
        bg="#6c757d",
        fg="white",
        font=("Arial", 9),
        padx=10,
        pady=2,
        relief=tk.GROOVE,
        borderwidth=2
    )
    btn_todos.grid(row=0, column=11, padx=5)

    # Frame para la tabla
    frame_tabla = tk.Frame(frame_principal)
    frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

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

    return tree, frame_botones, entry_nombre, entry_dni

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

def buscar_por_nombre(tree, nombre):
    """Busca socios por nombre y muestra solo los resultados coincidentes"""
    try:
        if not nombre.strip():
            messagebox.showwarning("Advertencia", "Ingrese un nombre para buscar")
            return

        socios = buscar_socio_por_nombre(nombre)
        tree.delete(*tree.get_children())

        if not socios:
            messagebox.showinfo("Resultado", "No se encontraron socios con ese nombre")
            return

        for socio in socios:
            id_socio, nombre_socio, dni, estado = socio
            tags = ('pagado',) if estado == "Pagado" else ('pendiente',)
            tree.insert("", "end", values=(id_socio, nombre_socio, dni, estado), tags=tags)

        messagebox.showinfo("Resultado", f"Se encontraron {len(socios)} socio(s)")
    except Exception as e:
        messagebox.showerror("Error", f"Error al buscar por nombre: {str(e)}")

def buscar_por_dni(tree, dni):
    """Busca socios por DNI y muestra solo los resultados coincidentes"""
    try:
        if not dni.strip():
            messagebox.showwarning("Advertencia", "Ingrese un DNI para buscar")
            return

        socios = buscar_socio_por_dni(dni)
        tree.delete(*tree.get_children())

        if not socios:
            messagebox.showinfo("Resultado", "No se encontraron socios con ese DNI")
            return

        for socio in socios:
            id_socio, nombre, dni_socio, estado = socio
            tags = ('pagado',) if estado == "Pagado" else ('pendiente',)
            tree.insert("", "end", values=(id_socio, nombre, dni_socio, estado), tags=tags)

        messagebox.showinfo("Resultado", f"Se encontraron {len(socios)} socio(s)")
    except Exception as e:
        messagebox.showerror("Error", f"Error al buscar por DNI: {str(e)}")

def filtrar_por_estado(tree, estado):
    """Filtra socios por estado de pago (Pendiente o Pagado)"""
    try:
        socios = filtrar_socios_por_estado(estado)
        tree.delete(*tree.get_children())

        if not socios:
            messagebox.showinfo("Resultado", f"No hay socios con estado '{estado}'")
            return

        for socio in socios:
            id_socio, nombre, dni, estado_socio = socio
            tags = ('pagado',) if estado_socio == "Pagado" else ('pendiente',)
            tree.insert("", "end", values=(id_socio, nombre, dni, estado_socio), tags=tags)

        messagebox.showinfo("Resultado", f"Se encontraron {len(socios)} socio(s) con estado '{estado}'")
    except Exception as e:
        messagebox.showerror("Error", f"Error al filtrar por estado: {str(e)}")

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
            # Actualizar solo el item seleccionado en lugar de recargar todo
            tree.set(item, "Estado", nuevo_estado)

            # Actualizar los tags (colores) del item
            tags = ('pagado',) if nuevo_estado == "Pagado" else ('pendiente',)
            tree.item(item, tags=tags)

            messagebox.showinfo("Éxito", f"Estado de {nombre} actualizado a '{nuevo_estado}'")
        else:
            messagebox.showerror("Error", "No se pudo guardar el cambio en la BD")
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar: {str(e)}")