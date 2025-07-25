import tkinter as tk
from gestion_pagos import crear_interfaz_pagos, configurar_botones, cargar_socios
from gestion_socios import crear_interfaz_socios

def abrir_menu_principal():
    menu = tk.Tk()
    menu.title("Sistema de Gestión de Membresías")
    menu.geometry("400x300")
    
    tk.Label(menu, text="Menú Principal", font=("Arial", 14)).pack(pady=10)
    
    btn_socios = tk.Button(menu, text="Gestión de Socios", command=gestionar_socios)
    btn_pagos = tk.Button(menu, text="Gestión de Pagos", command=gestionar_pagos)
    
    btn_socios.pack(pady=5)
    btn_pagos.pack(pady=5)
    
    menu.mainloop()

def gestionar_socios():
    ventana_socios = tk.Toplevel()
    from gestion_socios import crear_interfaz_socios
    crear_interfaz_socios(ventana_socios)

def gestionar_pagos():
    ventana_pagos = tk.Toplevel()
    ventana_pagos.title("Gestión de Pagos")
    ventana_pagos.geometry("800x600")
    
    tree, frame_botones = crear_interfaz_pagos(ventana_pagos)
    configurar_botones(frame_botones, tree)
    cargar_socios(tree)

def mostrar_menu(root):
    abrir_menu_principal()