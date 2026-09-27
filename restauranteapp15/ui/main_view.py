import tkinter as tk
from tkinter import ttk, messagebox


class MainView:

    def __init__(self, root, servicio, cerrar_sesion, logo_path):

        self.root = root
        self.servicio = servicio
        self.cerrar_sesion = cerrar_sesion

        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        self.crear_interfaz(logo_path)

    def crear_interfaz(self, logo_path):

        encabezado = tk.Frame(self.frame)
        encabezado.pack(fill="x", padx=20, pady=10)

        try:

            self.logo = tk.PhotoImage(file=logo_path)

            tk.Label(
                encabezado,
                image=self.logo
            ).pack(side="left")

        except tk.TclError:

            tk.Label(
                encabezado,
                text="RESTAURANTE APP",
                font=("Arial", 18, "bold")
            ).pack(side="left")

        tk.Button(
            encabezado,
            text="Cerrar sesión",
            command=self.cerrar_sesion
        ).pack(side="right")

        tk.Label(
            self.frame,
            text="Panel principal",
            font=("Arial", 16, "bold")
        ).pack(pady=5)

        botones = tk.Frame(self.frame)
        botones.pack(pady=8)

        tk.Button(
            botones,
            text="Productos",
            width=16,
            command=self.mostrar_productos
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            botones,
            text="Usuarios",
            width=16,
            command=self.mostrar_usuarios
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            botones,
            text="Ventas",
            width=16,
            command=self.mostrar_ventas
        ).grid(row=0, column=2, padx=5)

        self.area = tk.Text(
            self.frame,
            width=95,
            height=7
        )
        self.area.pack(padx=20, pady=8)

        marco = tk.LabelFrame(
            self.frame,
            text="Registrar venta",
            padx=10,
            pady=10
        )

        marco.pack(
            fill="x",
            padx=20,
            pady=5
        )

        tk.Label(
            marco,
            text="Usuario:"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.combo_usuario = ttk.Combobox(
            marco,
            state="readonly",
            width=35
        )

        self.combo_usuario.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        tk.Label(
            marco,
            text="Producto:"
        ).grid(row=1, column=0, padx=5, pady=5)

        self.combo_producto = ttk.Combobox(
            marco,
            state="readonly",
            width=35
        )

        self.combo_producto.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        # Evento: command llama al callback registrar_venta
        tk.Button(
            marco,
            text="Registrar venta",
            width=20,
            command=self.registrar_venta
        ).grid(
            row=0,
            column=2,
            rowspan=2,
            padx=15
        )

        self.cargar_combos()

        self.tabla = ttk.Treeview(
            self.frame,
            columns=("usuario", "producto", "fecha"),
            show="headings",
            height=7
        )

        self.tabla.heading(
            "usuario",
            text="Usuario"
        )

        self.tabla.heading(
            "producto",
            text="Producto"
        )

        self.tabla.heading(
            "fecha",
            text="Fecha"
        )

        self.tabla.column(
            "usuario",
            width=220
        )

        self.tabla.column(
            "producto",
            width=220
        )

        self.tabla.column(
            "fecha",
            width=220
        )

        self.tabla.pack(
            fill="x",
            padx=20,
            pady=8
        )

        self.actualizar_tabla_ventas()

    def cargar_combos(self):

        self.combo_usuario["values"] = [
            f"{usuario.identificacion} - {usuario.nombre}"
            for usuario in self.servicio.obtener_usuarios()
        ]

        self.combo_producto["values"] = [
            f"{producto.codigo} - {producto.nombre}"
            for producto in self.servicio.obtener_productos()
            if producto.stock > 0
        ]

    def registrar_venta(self):

        usuario_seleccionado = self.combo_usuario.get()
        producto_seleccionado = self.combo_producto.get()

        if not usuario_seleccionado or not producto_seleccionado:

            messagebox.showwarning(
                "Datos incompletos",
                "Seleccione un usuario y un producto."
            )

            return

        identificacion = usuario_seleccionado.split(" - ")[0]
        codigo = producto_seleccionado.split(" - ")[0]

        correcto, mensaje = self.servicio.registrar_venta(
            identificacion,
            codigo
        )

        if correcto:

            messagebox.showinfo(
                "Venta",
                mensaje
            )

            self.actualizar_tabla_ventas()
            self.cargar_combos()
            self.mostrar_productos()

        else:

            messagebox.showerror(
                "Venta",
                mensaje
            )

    def actualizar_tabla_ventas(self):

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        usuarios = {
            usuario.identificacion: usuario.nombre
            for usuario in self.servicio.obtener_usuarios()
        }

        productos = {
            producto.codigo: producto.nombre
            for producto in self.servicio.obtener_productos()
        }

        for venta in self.servicio.obtener_ventas():

            self.tabla.insert(
                "",
                tk.END,
                values=(
                    usuarios.get(
                        venta.identificacion_usuario,
                        venta.identificacion_usuario
                    ),
                    productos.get(
                        venta.codigo_producto,
                        venta.codigo_producto
                    ),
                    venta.fecha
                )
            )

    def mostrar_productos(self):

        self.area.delete(
            "1.0",
            tk.END
        )

        self.area.insert(
            tk.END,
            "--- PRODUCTOS REGISTRADOS ---\n\n"
        )

        for producto in self.servicio.obtener_productos():

            self.area.insert(
                tk.END,
                producto.mostrar_informacion() + "\n"
            )

    def mostrar_usuarios(self):

        self.area.delete(
            "1.0",
            tk.END
        )

        self.area.insert(
            tk.END,
            "--- USUARIOS REGISTRADOS ---\n\n"
        )

        for usuario in self.servicio.obtener_usuarios():

            self.area.insert(
                tk.END,
                usuario.mostrar_informacion() + "\n"
            )

    def mostrar_ventas(self):

        self.area.delete(
            "1.0",
            tk.END
        )

        self.area.insert(
            tk.END,
            "--- VENTAS REGISTRADAS ---\n\n"
        )

        for venta in self.servicio.obtener_ventas():

            self.area.insert(
                tk.END,
                f"Usuario: {venta.identificacion_usuario} | "
                f"Producto: {venta.codigo_producto} | "
                f"Fecha: {venta.fecha}\n"
            )

    def destruir(self):
        self.frame.destroy()