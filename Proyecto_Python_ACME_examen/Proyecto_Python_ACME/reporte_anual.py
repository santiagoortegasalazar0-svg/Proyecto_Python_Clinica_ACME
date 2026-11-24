import json
from collections import Counter
from datetime import datetime
from pathlib import Path

from almacenamiento import cargar_datos


ARCHIVO_REPORTE = Path(__file__).resolve().parent / "reporte_anual_diagnosticos.json"


def _fecha_valida(fecha):
    if not isinstance(fecha, str) or not fecha.strip():
        return None
    try:
        return datetime.fromisoformat(fecha.strip())
    except (ValueError, TypeError):
        return None


def reporte_anual_diagnosticos():
    """
    Consolida las consultas (diagnósticos) almacenadas en acme.json por año.
    Ignora consultas con fechas inválidas y las informa al usuario.
    """
    datos = cargar_datos()
    consultas = datos.get("consultas", [])
    usuarios = datos.get("usuarios", [])
    pacientes = datos.get("pacientes", [])

    ids_medicos = {
        str(u.get("identificacion", "")).strip()
        for u in usuarios if u.get("rol") == "medico"
    }
    ids_pacientes = {
        str(p.get("identificacion", "")).strip()
        for p in pacientes
    }

    grupos = {}
    invalidos = 0

    for consulta in consultas:
        fecha = _fecha_valida(consulta.get("fecha"))
        if fecha is None:
            invalidos += 1
            continue

        anio = str(fecha.year)  # agrupación estricta YYYY
        grupos.setdefault(anio, []).append((fecha, consulta))

    reporte = {"años": {}}

    for anio in sorted(grupos):
        registros = grupos[anio]
        total = len(registros)

        medicos = set()
        pacientes_unicos = set()
        sintomas_total = 0
        medicamentos_total = 0
        frecuencia_diagnosticos = Counter()

        for fecha, consulta in registros:
            medico_id = str(consulta.get("medico_identificacion", "")).strip()
            paciente_id = str(consulta.get("paciente_identificacion", "")).strip()

            if medico_id and (not ids_medicos or medico_id in ids_medicos):
                medicos.add(medico_id)
            elif medico_id:
                # Conserva identificaciones de médico de registros antiguos
                # aunque el usuario no esté actualmente en usuarios.json.
                medicos.add(medico_id)

            if paciente_id and (not ids_pacientes or paciente_id in ids_pacientes):
                pacientes_unicos.add(paciente_id)
            elif paciente_id:
                pacientes_unicos.add(paciente_id)

            sintomas = consulta.get("sintomas", [])
            medicamentos = consulta.get("medicamentos", [])
            sintomas_total += len(sintomas) if isinstance(sintomas, list) else 0
            medicamentos_total += len(medicamentos) if isinstance(medicamentos, list) else 0

            nombre_diagnostico = str(consulta.get("diagnostico", "Sin diagnóstico")).strip()
            frecuencia_diagnosticos[nombre_diagnostico or "Sin diagnóstico"] += 1

        registros_ordenados = sorted(registros, key=lambda elemento: elemento[0])
        primero = registros_ordenados[0][1]
        ultimo = registros_ordenados[-1][1]
        diagnostico_comun = frecuencia_diagnosticos.most_common(1)[0][0]

        reporte["años"][anio] = {
            "total_diagnosticos": total,
            "medicos_participantes": len(medicos),
            "pacientes_atendidos": len(pacientes_unicos),
            "promedio_sintomas": round(sintomas_total / total, 2),
            "promedio_medicamentos": round(medicamentos_total / total, 2),
            "diagnostico_mas_comun": diagnostico_comun,
            "primer_diagnostico": primero.get("diagnostico", "Sin diagnóstico"),
            "ultimo_diagnostico": ultimo.get("diagnostico", "Sin diagnóstico")
        }

    with ARCHIVO_REPORTE.open("w", encoding="utf-8") as archivo:
        json.dump(reporte, archivo, ensure_ascii=False, indent=4)

    print("\n--- REPORTE ANUAL DE DIAGNÓSTICOS ---")
    if reporte["años"]:
        for anio, metricas in reporte["años"].items():
            print(f"\nAño: {anio}")
            for clave, valor in metricas.items():
                print(f"{clave.replace('_', ' ').capitalize()}: {valor}")
    else:
        print("No hay diagnósticos con fechas válidas para generar el reporte.")

    print(f"\nArchivo generado: {ARCHIVO_REPORTE.name}")
    if invalidos:
        print(f"Diagnósticos ignorados por fecha inválida: {invalidos}")
    print("Reporte anual generado correctamente.")
