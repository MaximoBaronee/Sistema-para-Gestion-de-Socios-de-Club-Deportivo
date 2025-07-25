import tkinter as tk
from tkinter import messagebox
import mysql.connector
from menu_principal import abrir_menu_principal

# Conectar con la base de datos
try:
    conexion = mysql.connector.connect(
        host="", # Coloque la dirección del host aquí,por ejemplo "localhost"
        user="", # Coloque el nombre de usuario aquí,por ejemplo "root"
        password="",  # Coloque la contraseña aquí
        database="" # Coloque el nombre de tu base de datos aquí
    )
    cursor = conexion.cursor()
except mysql.connector.Error as e:
    messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
    exit()

# Usuario predeterminado
ADMIN_USUARIO = "" #Coloque el nombre de usuario aquí
ADMIN_CLAVE = "" #Coloque la contraseña aquí

# Variable global para la ventana principal
root = None

# Función para verificar login
def verificar_login():
    global root  # Hacer root global para poder acceder en esta función
    usuario = entry_usuario.get()
    clave = entry_clave.get()
    
    # Verificar si es el usuario admin
    if usuario == ADMIN_USUARIO and clave == ADMIN_CLAVE:
        messagebox.showinfo("Éxito", "Inicio de sesión como administrador exitoso")
        root.destroy()
        abrir_menu_principal()
        return
    
    consulta = "SELECT clave FROM usuarios WHERE usuario = %s"
    cursor.execute(consulta, (usuario,))
    resultado = cursor.fetchone()
    
    if resultado and resultado[0] == clave:
        messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
        root.destroy()
        abrir_menu_principal()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# Interfaz de Login
def mostrar_login(main_root):
    global entry_usuario, entry_clave, root  # Hacer las entradas y root globales
    root = main_root  # Asignar la ventana principal a la variable global
    root.title("Login - Club Deportivo")
    root.geometry("300x200")

    tk.Label(root, text="Usuario:").pack()
    entry_usuario = tk.Entry(root)
    entry_usuario.pack()

    tk.Label(root, text="Contraseña:").pack()
    entry_clave = tk.Entry(root, show="*")
    entry_clave.pack()

    tk.Button(root, text="Iniciar Sesión", command=verificar_login).pack(pady=10)

    root.mainloop()