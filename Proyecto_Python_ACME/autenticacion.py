from almacenamiento import cargar_datos
from seguridad import verificar_contrasena


def iniciar_sesion():
    while True:
        print("\n========== LOGIN CLÍNICA ACME ==========")
        print("Deje el correo vacío para salir.")
        email = input("Usuario (e-mail): ").strip().lower()
        if not email:
            return None
        contrasena = input("Contraseña: ")

        datos = cargar_datos()
        for usuario in datos["usuarios"]:
            if usuario["email"].lower() == email and verificar_contrasena(
                contrasena, usuario["password_hash"]
            ):
                print(f"\nBienvenido(a), {usuario['nombres']} {usuario['apellidos']}.")
                return usuario

        print("Usuario o contraseña incorrectos. Intente nuevamente.")
