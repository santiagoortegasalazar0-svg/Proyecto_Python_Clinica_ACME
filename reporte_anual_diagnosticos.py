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


def reporte_anual_diagnostos():

    datos = cargar_datos()
    consultas = datos.get("consulta", [])
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
        fecha = _fecha_valida(consultas.get("fecha"))
        if fecha is None:
            invalidos +=1
            continue

        año = str(fecha.year) 
        grupos.setdefault(año, []).append((fecha, consultas))

    reporte = {"años": {}}


    for año in sorted(grupos):
        registros = grupos [año]
        total = len(registros)

        medicos = set()
        pacientes_unicos = set()
        sintomas_total = 0
        medicamentos_total = 0
        frecuencia_diagnosticos = Counter()


        for fecha, consultas in registros:
            medico_id = str(consulta.get("medico_identificacion, ")).strip()
            paciente_id = str(consulta.get("paciente_identificacion, ")).strip()

            if medico_id and (not ids_medicos or medico_id in ids_medicos):
                medicos.add(medico_id)
            elif medico_id:
                medicos.add(medico_id)

            if paciente_id and (not ids_pacientes or paciente_id in ids_pacientes):
                pacientes_unicos.add(paciente_id)
            elif paciente_id:
                pacientes_unicos.add(paciente_id)


            sintomas = consulta.get("sintomas", [])
            medicamentos = consulta.get("medicamentos", [])
            sintomas_total +=len(sintomas) if isinstance(sintomas, list) else 0
            medicamentos_total += len(medicamentos) if isinstance(medicamentos, list) else 0


            nombre_diagnostico = str(consulta.get("diagnostico", "sin diagnostico")).strip()
            frecuencia_diagnosticos[nombre_diagnostico or "sin diagnostico"] += 1
        
         