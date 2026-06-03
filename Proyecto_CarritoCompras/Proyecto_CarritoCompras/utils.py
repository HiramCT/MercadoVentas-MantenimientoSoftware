"""
utils.py - Utilidades: entrada de contraseña con máscara, ticket de compra
"""
import sys
import time
from datetime import datetime


def input_password(mensaje="Ingrese su contraseña: "):
    """
    Lee una contraseña mostrando símbolos (•) en lugar de texto.
    Compatible con Windows y Unix.
    """
    if sys.platform == "win32":
        return _input_password_windows(mensaje)
    else:
        return _input_password_unix(mensaje)


def _input_password_windows(mensaje):
    """Implementación para Windows usando msvcrt."""
    import msvcrt

    print(mensaje, end="", flush=True)
    password = []
    while True:
        ch = msvcrt.getwch()
        if ch == "\r" or ch == "\n":  # Enter
            print()
            break
        elif ch == "\b" or ch == "\x7f":  # Backspace
            if password:
                password.pop()
                print("\b \b", end="", flush=True)
        elif ch == "\x03":  # Ctrl+C
            raise KeyboardInterrupt
        else:
            password.append(ch)
            print("•", end="", flush=True)
    return "".join(password)


def _input_password_unix(mensaje):
    """Implementación para Unix usando getpass con máscara manual."""
    # Alternativa portable: usar getpass directamente (no muestra caracteres)
    # pero usamos lectura carácter por carácter para mostrar •
    import termios
    import tty

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        print(mensaje, end="", flush=True)
        password = []
        while True:
            ch = sys.stdin.read(1)
            if ch in ("\r", "\n"):
                print()
                break
            elif ch in ("\b", "\x7f"):
                if password:
                    password.pop()
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
            elif ch == "\x03":
                raise KeyboardInterrupt
            else:
                password.append(ch)
                sys.stdout.write("•")
                sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return "".join(password)


def generar_ticket(nombre_usuario, items, total, pago, cambio, archivo="ticket.txt"):
    """
    Genera un archivo TXT con el ticket de compra.
    Retorna el nombre del archivo generado.
    """
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nombre_archivo = f"ticket_{nombre_usuario.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write("=" * 50 + "\n")
        f.write("         MERCADOVENTAS - TICKET DE COMPRA\n")
        f.write("=" * 50 + "\n")
        f.write(f"Fecha:       {ahora}\n")
        f.write(f"Cliente:     {nombre_usuario}\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Producto':<25} {'Cant.':>6} {'P.Unit.':>8} {'Subtotal':>10}\n")
        f.write("-" * 50 + "\n")

        for item in items:
            # item: (ID, nombre, precio, cantidad, categoria)
            nombre = item[1][:24]
            precio = float(item[2])
            cant = item[3]
            subtotal = precio * cant
            f.write(f"{nombre:<25} {cant:>6} ${precio:>6.2f} ${subtotal:>7.2f}\n")

        f.write("-" * 50 + "\n")
        f.write(f"{'TOTAL':>39} ${total:>7.2f}\n")
        f.write(f"{'Pagado':>39} ${pago:>7.2f}\n")
        f.write(f"{'Cambio':>39} ${cambio:>7.2f}\n")
        f.write("=" * 50 + "\n")
        f.write("   ¡Gracias por tu compra, vuelve pronto!\n")
        f.write("=" * 50 + "\n")

    return nombre_archivo


def limpiar_pantalla():
    """Limpia la terminal."""
    import os
    os.system("cls" if os.name == "nt" else "clear")