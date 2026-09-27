import tkinter as tk
from pathlib import Path

from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


BASE_DIR = Path(__file__).resolve().parent

DATOS_DIR = BASE_DIR / "datos"
ASSETS_DIR = BASE_DIR / "assets"


def iniciar_aplicacion():

    root = tk.Tk()

    root.title("Restaurante App - Semana 15")
    root.geometry("950x700")
    root.resizable(False, False)

    archivo_servicio = ArchivoServicio(
        str(DATOS_DIR / "productos.json"),
        str(DATOS_DIR / "usuarios.json"),
        str(DATOS_DIR / "ventas.json")
    )

    servicio = RestauranteServicio(
        archivo_servicio.cargar_productos(),
        archivo_servicio.cargar_usuarios(),
        archivo_servicio.cargar_ventas(),
        archivo_servicio
    )

    vista_actual = {
        "vista": None
    }

    logo_path = str(
        ASSETS_DIR / "logo.png"
    )

    def mostrar_login():

        if vista_actual["vista"] is not None:
            vista_actual["vista"].destruir()

        vista_actual["vista"] = LoginView(
            root,
            servicio,
            mostrar_principal,
            logo_path
        )

    def mostrar_principal():

        if vista_actual["vista"] is not None:
            vista_actual["vista"].destruir()

        vista_actual["vista"] = MainView(
            root,
            servicio,
            mostrar_login,
            logo_path
        )

    mostrar_login()

    root.mainloop()


if __name__ == "__main__":
    iniciar_aplicacion()