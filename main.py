# main.py
import tkinter as tk
from login import mostrar_login
from menu_principal import mostrar_menu

def iniciar_app():
    root = tk.Tk()
    root.title("Gestión de Membresías - Club Deportivo")
    root.geometry("800x600")

    # Manejar el evento de cierre de la ventana
    def on_closing():
        try:
            root.destroy()
        except tk.TclError:
            pass  # Ignora el error si la ventana ya ha sido destruida

    root.protocol("WM_DELETE_WINDOW", on_closing)  # Interceptar el evento de cierre

    if mostrar_login(root):
        mostrar_menu(root)  # Muestra el menú principal después del login
    else:
        try:
            root.destroy()  # Cierra la ventana si el login falla
        except tk.TclError:
            pass  # Ignora el error si la ventana ya fue destruida

    root.mainloop()

if __name__ == "__main__":
    iniciar_app()
