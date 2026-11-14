
from almacenamiento import cargar_datos
from pacientes import buscar_paciente
from validaciones import pedir_identificacion


def consultar_historia():

    print("\n========== HISTORIA CLINICA ==========")

    datos = cargar_datos()

    print("Archivo JSON cargado correctamente.")

    identificacion = pedir_identificacion(
        "Ingrese el documento del paciente: "
    )

    print("Documento ingresado:", identificacion)

    paciente = buscar_paciente(identificacion, datos)

    if paciente is None:
        print("ERROR: No se encontro el paciente.")
        return

    print("\n========== DATOS DEL PACIENTE ==========")

    print("Identificacion:", paciente["identificacion"])
    print("Nombres:", paciente["nombres"])
    print("Apellidos:", paciente["apellidos"])
    print("Telefono:", paciente["telefono"])
    print("Correo:", paciente["email"])
    print("Direccion:", paciente["direccion"])
    print("Genero:", paciente["genero"])
    print("Estado civil:", paciente["estado_civil"])

    print("\n========== HISTORIAL DE CONSULTAS ==========")

    consultas = []

    for consulta in datos.get("consultas", []):

        documento = str(
            consulta.get("paciente_identificacion", "")
        ).strip()

        if documento == identificacion.strip():
            consultas.append(consulta)

    print("Consultas encontradas:", len(consultas))

    if not consultas:
        print("Este paciente no tiene consultas registradas.")
        return

    for numero, consulta in enumerate(consultas, start=1):

        print("\n--------------------------------")
        print("CONSULTA NUMERO:", numero)
        print("--------------------------------")

        print("Fecha:", consulta.get("fecha", "No registrada"))
        print("Medico:", consulta.get("medico", "No registrado"))

        print("\nSintomas:")

        for sintoma in consulta.get("sintomas", []):
            print("-", sintoma)

        print("\nDiagnostico:")
        print(consulta.get("diagnostico", "No registrado"))

        print("\nMedicamentos prescritos:")

        medicamentos = consulta.get("medicamentos", [])

        if not medicamentos:
            print("No se registraron medicamentos.")

        for medicamento in medicamentos:

            print("\nMedicamento:", medicamento.get("medicamento"))
            print("Cantidad:", medicamento.get("cantidad"))
            print("Dosis:", medicamento.get("dosis"))
            print(
                "Tiempo de aplicacion:",
                medicamento.get("tiempo_aplicacion_dias"),
                "dias"
            )

    print("\n========== FIN DE HISTORIA CLINICA ==========")

