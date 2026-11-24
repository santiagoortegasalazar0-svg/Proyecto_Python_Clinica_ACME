from almacenamiento import cargar_datos, guardar_datos
from validaciones import pedir_identificacion, pedir_texto, pedir_telefono, pedir_email


def registrar_paciente():
    datos = cargar_datos()
    print("\n--- REGISTRO DE PACIENTE ---")
    identificacion = pedir_identificacion()
    if any(p["identificacion"] == identificacion for p in datos["pacientes"]):
        print("Ya existe un paciente con esa identificación.")
        return

    nombres = pedir_texto("Nombres: ")
    apellidos = pedir_texto("Apellidos: ")
    telefono = pedir_telefono()
    email = pedir_email()
    direccion = pedir_texto("Dirección: ")

    while True:
        genero = input("Género (masculino/femenino/otro): ").strip().lower()
        if genero in ("masculino", "femenino", "otro"):
            break
        print("Opción no válida.")
    while True:
        estado_civil = input(
            "Estado civil (soltero/a, casado/a, unión libre, divorciado/a, viudo/a): "
        ).strip().lower()
        if estado_civil in (
            "soltero", "soltera", "casado", "casada", "unión libre",
            "union libre", "divorciado", "divorciada", "viudo", "viuda"
        ):
            break
        print("Estado civil no válido.")

    datos["pacientes"].append({
        "identificacion": identificacion,
        "nombres": nombres,
        "apellidos": apellidos,
        "telefono": telefono,
        "email": email,
        "direccion": direccion,
        "genero": genero,
        "estado_civil": estado_civil
    })
    guardar_datos(datos)
    print("Paciente registrado correctamente.")


def buscar_paciente(identificacion, datos=None):
    if datos is None:
        datos = cargar_datos()
    for paciente in datos["pacientes"]:
        if paciente["identificacion"] == identificacion:
            return paciente
    return None


def menu_pacientes():
    registrar_paciente()
