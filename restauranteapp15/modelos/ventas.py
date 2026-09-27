class Venta:
    def __init__(self, identificacion_usuario, codigo_producto, fecha):
        self.identificacion_usuario = identificacion_usuario
        self.codigo_producto = codigo_producto
        self.fecha = fecha

    def to_dict(self):
        return {
            "identificacion_usuario": self.identificacion_usuario,
            "codigo_producto": self.codigo_producto,
            "fecha": self.fecha
        }