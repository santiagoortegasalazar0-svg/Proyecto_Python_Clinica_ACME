import json
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
ARCHIVO_DATOS = CARPETA / "datos" / "acme.json"
CARPETA_PRESCRIPCIONES = CARPETA / "prescripciones"


def guardar_datos(datos):
    ARCHIVO_DATOS.parent.mkdir(parents=True, exist_ok=True)
    temporal = ARCHIVO_DATOS.with_suffix(".tmp")
    with temporal.open("w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)
    temporal.replace(ARCHIVO_DATOS)


def cargar_datos():
    if not ARCHIVO_DATOS.exists():
        inicializar_archivos()
    with ARCHIVO_DATOS.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


def inicializar_archivos():
    CARPETA_PRESCRIPCIONES.mkdir(parents=True, exist_ok=True)
    if ARCHIVO_DATOS.exists():
        return

    from seguridad import generar_hash
    datos = {
        "usuarios": [{
            "identificacion": "0000",
            "nombres": "Admin",
            "apellidos": "Administrador",
            "telefono": "555 000111",
            "email": "admin@acmeclinic.com",
            "direccion": "Cl 185 # 26 – 85",
            "rol": "administrativo",
            "password_hash": generar_hash("Admin123*")
        }],
        "pacientes": [],
        "consultas": []
    }
    guardar_datos(datos)
