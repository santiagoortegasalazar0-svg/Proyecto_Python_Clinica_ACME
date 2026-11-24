import hashlib
import hmac
import os


def generar_hash(contrasena):
    sal = os.urandom(16)
    derivada = hashlib.pbkdf2_hmac("sha256", contrasena.encode("utf-8"), sal, 200000)
    return sal.hex() + "$" + derivada.hex()


def verificar_contrasena(contrasena, hash_guardado):
    try:
        sal_hex, hash_hex = hash_guardado.split("$", 1)
        sal = bytes.fromhex(sal_hex)
        esperado = bytes.fromhex(hash_hex)
        calculado = hashlib.pbkdf2_hmac("sha256", contrasena.encode("utf-8"), sal, 200000)
        return hmac.compare_digest(calculado, esperado)
    except (ValueError, TypeError):
        return False
