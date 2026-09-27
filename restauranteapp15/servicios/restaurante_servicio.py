from datetime import datetime

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.ventas import Venta


class RestauranteServicio:

    def __init__(
        self,
        datos_productos,
        datos_usuarios,
        datos_ventas,
        archivo_servicio
    ):
        self.archivo_servicio = archivo_servicio

        self.productos = []
        self.usuarios = []
        self.ventas = []

        self.crear_productos(datos_productos)
        self.crear_usuarios(datos_usuarios)
        self.crear_ventas(datos_ventas)

    def crear_productos(self, datos):

        for dato in datos:
            try:
                producto = Producto(
                    dato["codigo"],
                    dato["nombre"],
                    dato["categoria"],
                    float(dato["precio"]),
                    int(dato.get("stock", 0))
                )

                self.productos.append(producto)

            except (KeyError, ValueError) as error:
                print("No se pudo cargar el producto:", error)

    def crear_usuarios(self, datos):

        for dato in datos:
            try:
                usuario = Usuario(
                    dato["identificacion"],
                    dato["nombre"],
                    dato["correo"],
                    dato.get("contrasena", "1234")
                )

                self.usuarios.append(usuario)

            except (KeyError, ValueError) as error:
                print("No se pudo cargar el usuario:", error)

    def crear_ventas(self, datos):

        for dato in datos:
            try:
                venta = Venta(
                    dato["identificacion_usuario"],
                    dato["codigo_producto"],
                    dato["fecha"]
                )

                self.ventas.append(venta)

            except KeyError as error:
                print("No se pudo cargar la venta:", error)

    def validar_acceso(self, identificacion, contrasena):

        return any(
            usuario.identificacion == identificacion
            and usuario.contrasena == contrasena
            for usuario in self.usuarios
        )

    def obtener_productos(self):
        return self.productos

    def obtener_usuarios(self):
        return self.usuarios

    def obtener_ventas(self):
        return self.ventas

    def registrar_venta(self, identificacion_usuario, codigo_producto):

        usuario = next(
            (
                usuario
                for usuario in self.usuarios
                if usuario.identificacion == identificacion_usuario
            ),
            None
        )

        producto = next(
            (
                producto
                for producto in self.productos
                if producto.codigo == codigo_producto
            ),
            None
        )

        if usuario is None:
            return False, "El usuario seleccionado no existe."

        if producto is None:
            return False, "El producto seleccionado no existe."

        if producto.stock <= 0:
            return False, "El producto no tiene stock disponible."

        venta = Venta(
            identificacion_usuario,
            codigo_producto,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        self.ventas.append(venta)

        producto.stock -= 1

        ventas_ok = self.archivo_servicio.guardar_ventas(
            [venta.to_dict() for venta in self.ventas]
        )

        productos_ok = self.archivo_servicio.guardar_productos(
            [producto.to_dict() for producto in self.productos]
        )

        if not ventas_ok or not productos_ok:

            self.ventas.pop()
            producto.stock += 1

            return False, "No se pudo guardar la operación."

        return True, "Venta registrada correctamente."