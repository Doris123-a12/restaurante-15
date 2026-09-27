import json


class ArchivoServicio:

    def __init__(self, ruta_productos, ruta_usuarios, ruta_ventas):
        self.ruta_productos = ruta_productos
        self.ruta_usuarios = ruta_usuarios
        self.ruta_ventas = ruta_ventas

    def cargar_productos(self):
        return self._cargar(self.ruta_productos)

    def cargar_usuarios(self):
        return self._cargar(self.ruta_usuarios)

    def cargar_ventas(self):
        return self._cargar(self.ruta_ventas)

    def guardar_productos(self, productos):
        return self._guardar(self.ruta_productos, productos)

    def guardar_ventas(self, ventas):
        return self._guardar(self.ruta_ventas, ventas)

    def _cargar(self, ruta):
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

            if not isinstance(datos, list):
                raise ValueError("El archivo debe contener una lista.")

            return datos

        except (FileNotFoundError, json.JSONDecodeError, PermissionError, ValueError) as error:
            print(f"No se pudo leer {ruta}: {error}")
            return []

    def _guardar(self, ruta, datos):
        try:
            with open(ruta, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)

            return True

        except (PermissionError, OSError) as error:
            print("No se pudo guardar:", error)
            return False