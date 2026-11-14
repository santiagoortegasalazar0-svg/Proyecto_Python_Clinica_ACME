import json
import re
from datetime import datetime
from almacenamiento import cargar_datos, guardar_datos, CARPETA_PRESCRIPCIONES
from pacientes import buscar_paciente
from validaciones import pedir_identificacion, pedir_texto


def registrar_diagnostico(medico):
    datos = cargar_datos()
    print("\n--- DIAGNÓSTICO DE PACIENTE ---")
    identificacion = pedir_identificacion("Identificación del paciente: ")
    paciente = buscar_paciente(identificacion, datos)
    if paciente is None:
        print("El paciente no está registrado. Regístrelo antes de continuar.")
        return

    sintomas = []
    print("Registre los síntomas. Escriba 'fin' para terminar.")
    while True:
        sintoma = input("Síntoma: ").strip()
        if sintoma.lower() == "fin":
            break
        if sintoma:
            sintomas.append(sintoma)
    if not sintomas:
        print("Debe registrar al menos un síntoma.")
        return

    diagnostico = pedir_texto("Diagnóstico o patología: ")
    medicamentos = []
    print("\nRegistre los medicamentos. Escriba 'fin' en el nombre para terminar.")
    while True:
        medicamento = input("Medicamento: ").strip()
        if medicamento.lower() == "fin":
            break
        if not medicamento:
            print("El nombre del medicamento es obligatorio.")
            continue
        cantidad = pedir_texto("Cantidad (por ejemplo, 20 tabletas): ")
        dosis = pedir_texto("Dosis diaria (por ejemplo, 1 tableta cada 8 horas): ")
        while True:
            try:
                tiempo = int(input("Tiempo de aplicación en días: "))
                if tiempo > 0:
                    break
                print("Ingrese un número mayor que cero.")
            except ValueError:
                print("Ingrese un número entero.")
        medicamentos.append({
            "medicamento": medicamento,
            "cantidad": cantidad,
            "dosis": dosis,
            "tiempo_aplicacion_dias": tiempo
        })

    fecha = datetime.now().astimezone().isoformat(timespec="seconds")
    consulta_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
    consulta = {
        "id": consulta_id,
        "fecha": fecha,
        "paciente_identificacion": paciente["identificacion"],
        "paciente": f"{paciente['nombres']} {paciente['apellidos']}",
        "medico_identificacion": medico["identificacion"],
        "medico": f"{medico['nombres']} {medico['apellidos']}",
        "sintomas": sintomas,
        "diagnostico": diagnostico,
        "medicamentos": medicamentos
    }

    datos["consultas"].append(consulta)
    guardar_datos(datos)

    prescripcion = {
        "fecha": fecha,
        "paciente": {
            "identificacion": paciente["identificacion"],
            "nombres": paciente["nombres"],
            "apellidos": paciente["apellidos"]
        },
        "medico": {
            "identificacion": medico["identificacion"],
            "nombres": medico["nombres"],
            "apellidos": medico["apellidos"]
        },
        "sintomas": sintomas,
        "diagnostico": diagnostico,
        "medicamentos": medicamentos
    }
    nombre_archivo = f"prescripcion_{consulta_id}_{paciente['identificacion']}.json"
    ruta = CARPETA_PRESCRIPCIONES / nombre_archivo
    with ruta.open("w", encoding="utf-8") as archivo:
        json.dump(prescripcion, archivo, ensure_ascii=False, indent=4)

    print(f"\nDiagnóstico guardado correctamente.")
    print(f"Prescripción JSON generada en: prescripciones/{nombre_archivo}")
