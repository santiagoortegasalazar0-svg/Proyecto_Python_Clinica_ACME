from autenticacion import iniciar_sesion
from usuarios import menu_usuarios
from pacientes import menu_pacientes
from diagnosticos import registrar_diagnostico
from historia_clinica import consultar_historia
from almacenamiento import inicializar_archivos, cargar_datos, guardar_datos


def menu_principal(usuario):
    while True:
        print("\n========== CLÍNICA ACME ==========")
        print(f"Usuario: {usuario['nombres']} {usuario['apellidos']} | Rol: {usuario['rol']}")
        print("1. Registrar usuario")
        print("2. Registrar paciente")
        print("3. Diagnosticar paciente")
        print("4. Consultar historia clínica")
        print("5. Cerrar sesión")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            if usuario["rol"] != "administrativo":
                print("Acceso denegado. Solo el personal administrativo puede registrar usuarios.")
            else:
                menu_usuarios()
        elif opcion == "2":
            menu_pacientes()
        elif opcion == "3":
            if usuario["rol"] != "medico":
                print("Acceso denegado. Solo los médicos pueden realizar diagnósticos.")
            else:
                registrar_diagnostico(usuario)
        elif opcion == "4":
            print("\nAbriendo historia clínica...")
            consultar_historia()
            input("\nPresione ENTER para regresar al menú...")
        elif opcion == "5":
            print("Sesión cerrada.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")


def main():
    inicializar_archivos()
    while True:
        usuario = iniciar_sesion()
        if usuario is None:
            print("Hasta pronto.")
            break
        menu_principal(usuario)
        respuesta = input("\n¿Desea salir del sistema? (s/n): ").strip().lower()
        if respuesta == "s":
            print("Hasta pronto.")
            break


if __name__ == "__main__":
    main()
