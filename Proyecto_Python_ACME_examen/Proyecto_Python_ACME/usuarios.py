from almacenamiento import cargar_datos, guardar_datos
from seguridad import generar_hash
from validaciones import (
    pedir_identificacion, pedir_texto, pedir_telefono, pedir_email, pedir_contrasena
)


def registrar_usuario():
    datos = cargar_datos()
    print("\n--- REGISTRO DE USUARIO ---")
    identificacion = pedir_identificacion()
    if any(u["identificacion"] == identificacion for u in datos["usuarios"]):
        print("Ya existe un usuario con esa identificación.")
        return

    nombres = pedir_texto("Nombres: ")
    apellidos = pedir_texto("Apellidos: ")
    telefono = pedir_telefono()
    email = pedir_email()
    if any(u["email"].lower() == email for u in datos["usuarios"]):
        print("Ya existe un usuario con ese e-mail.")
        return
    direccion = pedir_texto("Dirección: ")

    while True:
        rol = input("Rol (1. Médico / 2. Administrativo): ").strip()
        if rol == "1":
            rol = "medico"
            break
        if rol == "2":
            rol = "administrativo"
            break
        print("Seleccione 1 o 2.")

    contrasena = pedir_contrasena()
    datos["usuarios"].append({
        "identificacion": identificacion,
        "nombres": nombres,
        "apellidos": apellidos,
        "telefono": telefono,
        "email": email,
        "direccion": direccion,
        "rol": rol,
        "password_hash": generar_hash(contrasena)
    })
    guardar_datos(datos)
    print("Usuario registrado correctamente.")


def menu_usuarios():
    registrar_usuario()
