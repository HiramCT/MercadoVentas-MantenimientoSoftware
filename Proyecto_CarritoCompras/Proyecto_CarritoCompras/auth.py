"""
auth.py - Módulo de autenticación: registro e inicio de sesión
"""
import bcrypt
import database as db
from utils import input_password


def registrar_usuario(cursor, conexion):
    """Registra un nuevo usuario comprador."""
    print("\n[------- ¡Holaaaa!, Bienvenid@ nuevo usuario a MercadoVentas -------]")
    name = input("\nIngrese su nombre completo: ")
    password = input_password("Ingrese una contraseña (¡Recuérdala siempre! ;D): ")
    passwordC = input_password("Confirma tu contraseña: ")

    while password != passwordC:
        print("\n¡Uups!, parece que las contraseñas no coinciden, vuelve a intentarlo\n")
        password = input_password("Ingrese una contraseña (¡Recuérdala siempre! ;D): ")
        passwordC = input_password("Confirma tu contraseña: ")

    pwd = password.encode("utf-8")
    salt = bcrypt.gensalt()
    contra_encriptada = bcrypt.hashpw(pwd, salt)

    mail = input("Ingrese su correo electrónico: ")
    numero = input("Ingrese su número de teléfono: ")

    db.crear_usuario(cursor, conexion, name, contra_encriptada, mail, numero)
    print("\n✅ Usuario registrado exitosamente.")
    return True


def registrar_empleado(cursor, conexion):
    """Registra un nuevo empleado/administrador."""
    print("\n[------- ¡Holaaaa!, Bienvenid@ nuevo empleado a MercadoVentas -------]")
    name = input("\nIngrese su nombre completo: ")
    password = input_password("Ingrese una contraseña (¡Recuérdala siempre! ;D): ")
    passwordC = input_password("Confirma tu contraseña: ")

    while password != passwordC:
        print("\n¡Uups!, parece que las contraseñas no coinciden, vuelve a intentarlo\n")
        password = input_password("Ingrese una contraseña (¡Recuérdala siempre! ;D): ")
        passwordC = input_password("Confirma tu contraseña: ")

    pwd = password.encode("utf-8")
    salt = bcrypt.gensalt()
    contra_encriptada = bcrypt.hashpw(pwd, salt)

    mail = input("Ingrese su correo electrónico: ")
    numero = input("Ingrese su número de teléfono: ")

    db.crear_empleado(cursor, conexion, name, contra_encriptada, mail, numero)
    print("\n✅ Empleado registrado exitosamente.")
    return True


def iniciar_sesion(cursor):
    """
    Intenta iniciar sesión como usuario o empleado.
    Retorna (id, nombre, rol) o None si falla.
    """
    print("\n[------- ¡Holaaaa!, Bienvenid@ a MercadoVentas -------]")
    mail = input("\nIngrese su correo: ")
    password = input_password("Ingrese su contraseña: ").encode("utf-8")

    # Buscar en USUARIOS
    usuario = db.buscar_usuario_por_correo(cursor, mail)
    if usuario:
        user_id, nombre, contrasena_hash = usuario
        if bcrypt.checkpw(password, contrasena_hash):
            print(f"\n✅ Inicio de sesión exitoso. ¡Bienvenido {nombre}!")
            return user_id, nombre, "usuario"

    # Buscar en EMPLEADOS
    empleado = db.buscar_empleado_por_correo(cursor, mail)
    if empleado:
        emp_id, nombre, contrasena_hash = empleado
        if bcrypt.checkpw(password, contrasena_hash):
            print(f"\n✅ Inicio de sesión exitoso. ¡Bienvenido {nombre}!")
            return emp_id, nombre, "empleado"

    print("\n❌ Lo siento, los datos proporcionados no coinciden. Intenta de nuevo.")
    return None