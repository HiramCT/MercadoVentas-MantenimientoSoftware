"""
main.py - Punto de entrada del sistema MercadoVentas
Mantenimiento de Software - Proyecto Final
"""
import sys
import database as db
import auth
from ui import interfaz_usuario, interfaz_admin


def menu_principal():
    """Menú de inicio: login, registro o salir."""
    conexion, cursor = db.connect_database()

    try:
        while True:
            print("\n" + "=" * 55)
            print("  ¡Holaaaa!, Bienvenid@ a MERCADOVENTAS")
            print("=" * 55)
            print(" 1.- Iniciar sesión")
            print(" 2.- Crear una cuenta")
            print(" 3.- Salir")
            print("=" * 12)
            opcion = input("Opción: ")

            if opcion == "1":
                resultado = auth.iniciar_sesion(cursor)
                if resultado:
                    user_id, nombre, rol = resultado
                    if rol == "usuario":
                        interfaz_usuario(user_id, nombre, cursor, conexion)
                    else:
                        interfaz_admin(user_id, nombre, cursor, conexion)

            elif opcion == "2":
                print("\n¿Crear cuenta en el portal de empleados o de usuarios?")
                print(" 1.- Empleado")
                print(" 2.- Usuario")
                tipo = input("Opción: ")

                if tipo == "1":
                    auth.registrar_empleado(cursor, conexion)
                elif tipo == "2":
                    auth.registrar_usuario(cursor, conexion)
                else:
                    print("\n❌ Opción inválida.")

            elif opcion == "3":
                print("\n¡Gracias por usar MercadoVentas! Hasta pronto.")
                sys.exit(0)

            else:
                print("\n❌ Opción inválida, vuelve a intentarlo.")

    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario. ¡Hasta luego!")
    finally:
        db.close_database(conexion)


if __name__ == "__main__":
    menu_principal()