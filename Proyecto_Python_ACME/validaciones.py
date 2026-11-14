import re


def pedir_texto(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("Este campo no puede quedar vacío.")


def pedir_identificacion(mensaje="Número de identificación: "):
    while True:
        valor = input(mensaje).strip()
        if valor.isdigit():
            return valor
        print("La identificación debe contener solo números.")


def pedir_telefono():
    while True:
        valor = input("Número de teléfono: ").strip()
        if re.fullmatch(r"[0-9+() -]{7,20}", valor):
            return valor
        print("Ingrese un teléfono válido.")


def pedir_email():
    while True:
        valor = input("E-mail: ").strip().lower()
        if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor):
            return valor
        print("Ingrese un correo válido.")


def pedir_contrasena():
    while True:
        valor = input("Contraseña (mínimo 8 caracteres): ")
        if len(valor) >= 8:
            confirmacion = input("Confirme la contraseña: ")
            if valor == confirmacion:
                return valor
            print("Las contraseñas no coinciden.")
        else:
            print("La contraseña debe tener al menos 8 caracteres.")
