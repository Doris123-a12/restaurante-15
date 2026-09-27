import tkinter as tk


class LoginView:

    def __init__(self, root, servicio, mostrar_principal, logo_path):

        self.root = root
        self.servicio = servicio
        self.mostrar_principal = mostrar_principal

        self.frame = tk.Frame(root)
        self.frame.pack(expand=True)

        try:
            self.logo = tk.PhotoImage(file=logo_path)

            tk.Label(
                self.frame,
                image=self.logo
            ).pack(pady=10)

        except tk.TclError:

            tk.Label(
                self.frame,
                text="RESTAURANTE APP",
                font=("Arial", 20, "bold")
            ).pack(pady=10)

        tk.Label(
            self.frame,
            text="Inicio de sesión",
            font=("Arial", 14)
        ).pack(pady=5)

        tk.Label(self.frame, text="Usuario").pack()

        self.entrada_usuario = tk.Entry(
            self.frame,
            width=30
        )
        self.entrada_usuario.pack(pady=5)

        tk.Label(self.frame, text="Contraseña").pack()

        self.entrada_contrasena = tk.Entry(
            self.frame,
            width=30,
            show="*"
        )
        self.entrada_contrasena.pack(pady=5)

        self.mensaje = tk.Label(
            self.frame,
            text="",
            fg="red"
        )
        self.mensaje.pack(pady=5)

        tk.Button(
            self.frame,
            text="Ingresar",
            width=20,
            command=self.ingresar
        ).pack(pady=10)

    def ingresar(self):

        usuario = self.entrada_usuario.get().strip()
        contrasena = self.entrada_contrasena.get().strip()

        if not usuario or not contrasena:
            self.mensaje.config(
                text="Ingrese usuario y contraseña."
            )
            return

        if self.servicio.validar_acceso(usuario, contrasena):

            self.frame.destroy()
            self.mostrar_principal()

        else:

            self.mensaje.config(
                text="Usuario o contraseña incorrectos."
            )

    def destruir(self):
        self.frame.destroy()