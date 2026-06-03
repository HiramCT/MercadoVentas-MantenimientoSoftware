"""
ui.py - Interfaces de usuario (menús, compra, venta, inventario, etc.)
"""
import database as db
from utils import input_password, generar_ticket


# ═══════════════════════════════════════════════════════════════════════
#  INTERFAZ DE USUARIO COMPRADOR
# ═══════════════════════════════════════════════════════════════════════


def interfaz_usuario(user_id, nombre, cursor, conexion):
    """Menú principal para usuarios compradores."""
    while True:
        print(f"\n¡Hola de nuevo {nombre}!")
        print(" ¿Qué deseas hacer hoy?")
        print(" 1.- Comprar producto")
        print(" 2.- Ver / Pagar carrito")
        print(" 3.- Salir al menú principal")
        opcion = input("\nOpción: ")

        if opcion == "1":
            compra(user_id, nombre, cursor, conexion)
        elif opcion == "2":
            ver_carrito(user_id, nombre, cursor, conexion)
        elif opcion == "3":
            print("\nSaliendo al menú principal...")
            return
        else:
            print("\n❌ Opción inválida, vuelve a intentarlo.")


# ═══════════════════════════════════════════════════════════════════════
#  INTERFAZ DE EMPLEADO / ADMIN
# ═══════════════════════════════════════════════════════════════════════


def interfaz_admin(user_id, nombre, cursor, conexion):
    """Menú principal para empleados/administradores."""
    while True:
        print(f"\n¡Hola de nuevo {nombre}!")
        print(" ¿Qué deseas hacer hoy?")
        print(" 1.- Gestión de inventarios")
        print(" 2.- Ver categorías")
        print(" 3.- Registro de ventas")
        print(" 4.- Salir al menú principal")
        opcion = input("\nOpción: ")

        if opcion == "1":
            inventario(user_id, nombre, cursor, conexion)
        elif opcion == "2":
            categorias(user_id, nombre, cursor, conexion)
        elif opcion == "3":
            mostrar_todas_ventas(user_id, nombre, cursor, conexion)
        elif opcion == "4":
            print("\nSaliendo al menú principal...")
            return
        else:
            print("\n❌ Opción inválida, vuelve a intentarlo.")


# ═══════════════════════════════════════════════════════════════════════
#  INVENTARIO (Admin)
# ═══════════════════════════════════════════════════════════════════════


def inventario(user_id, nombre, cursor, conexion):
    """Gestión de productos (CRUD para administradores)."""
    try:
        while True:
            print("\n[----------- INVENTARIO DE PRODUCTOS -----------]\n")
            productos = db.obtener_productos(cursor)
            for p in productos:
                print(f"ID: {p[0]}")
                print(f"Nombre:    {p[1]}")
                print(f"Precio:    ${p[2]:.2f}")
                print(f"Cantidad:  {p[3]}")
                print(f"Categoría: {p[4]}")
                print("-" * 50)

            print("\n 1.- Eliminar producto")
            print(" 2.- Añadir producto")
            print(" 3.- Volver")
            opcion = input("\nOpción: ")

            if opcion == "1":
                prod_id = input("\nIngrese el ID del producto a eliminar: ")
                db.eliminar_producto(cursor, conexion, prod_id)
                print("✅ Producto eliminado con éxito.")

            elif opcion == "2":
                nombre_p = input("\nIngrese el nombre del producto: ")
                try:
                    precio = float(input("Ingrese su precio: "))
                    unidades = int(input("Ingrese la cantidad: "))
                except ValueError:
                    print("❌ Precio o cantidad inválidos. Deben ser números.")
                    continue

                print("\nCategorías disponibles:")
                categorias = db.obtener_categorias(cursor)
                for cat in categorias:
                    print(f"  ID: {cat[0]} - {cat[1]}")
                try:
                    id_cat = int(input("\nID de la categoría: "))
                except ValueError:
                    print("❌ ID inválido.")
                    continue

                db.agregar_producto(cursor, conexion, nombre_p, precio, unidades, id_cat)
                print("✅ Producto añadido con éxito.")

            elif opcion == "3":
                return
            else:
                print("\n❌ Opción inválida.")

    except Exception as e:
        print(f"Error en inventario: {e}")


# ═══════════════════════════════════════════════════════════════════════
#  CATEGORÍAS (Admin)
# ═══════════════════════════════════════════════════════════════════════


def categorias(user_id, nombre, cursor, conexion):
    """Gestión de categorías (CRUD para administradores)."""
    try:
        while True:
            print("\n[----------------- CATEGORÍAS -----------------]")
            cats = db.obtener_categorias(cursor)
            for c in cats:
                print(f"ID:          {c[0]}")
                print(f"Nombre:      {c[1]}")
                print(f"Descripción: {c[2]}")
                print("-" * 50)

            print("\n 1.- Eliminar categoría")
            print(" 2.- Añadir categoría")
            print(" 3.- Volver")
            opcion = input("\nOpción: ")

            if opcion == "1":
                cat_id = input("\nIngrese el ID de la categoría a eliminar: ")
                db.eliminar_categoria(cursor, conexion, cat_id)
                print("✅ Categoría eliminada con éxito.")

            elif opcion == "2":
                nombre_cat = input("\nIngrese el nombre de la categoría: ")
                descripcion = input("Ingrese su descripción: ")
                db.agregar_categoria(cursor, conexion, nombre_cat, descripcion)
                print("✅ Categoría añadida con éxito.")

            elif opcion == "3":
                return
            else:
                print("\n❌ Opción inválida.")

    except Exception as e:
        print(f"Error en categorías: {e}")


# ═══════════════════════════════════════════════════════════════════════
#  COMPRA (Usuario)
# ═══════════════════════════════════════════════════════════════════════


def compra(user_id, nombre, cursor, conexion):
    """Permite al usuario navegar categorías y añadir productos al carrito."""
    try:
        while True:
            print("\n¿Qué te interesa hoy? He aquí nuestras secciones:\n")
            cats = db.obtener_categorias(cursor)
            print("[------------ CATEGORÍAS ------------]")
            for c in cats:
                print(f"  ID: {c[0]}  [{c[1]}]")

            opcion = input("\nSelecciona la categoría que te interese (ID): ")

            productos = db.obtener_productos_por_categoria(cursor, opcion)
            if not productos:
                print("\nNo hay productos en esta categoría.")
                seguir = input("¿Deseas ver otra categoría? (1=Si / 2=No): ")
                if seguir != "1":
                    return
                continue

            print("\n[------------------------------- PRODUCTOS -------------------------------]")
            for p in productos:
                print(f"  ID: {p[0]}  |  {p[1]}  |  ${p[2]:.2f}  |  Stock: {p[3]}")

            try:
                prod_id = int(input("\nSelecciona el producto a comprar (ID): "))
            except ValueError:
                print("ID inválido.")
                continue

            # Buscar el producto seleccionado
            producto = None
            for p in productos:
                if p[0] == prod_id:
                    producto = p
                    break

            if not producto:
                print("❌ Producto no encontrado.")
                continue

            añadir = input("¿Añadir al carrito? (1=Si / 2=No): ")
            if añadir == "1":
                try:
                    unidades = int(input("¿Cuántas unidades?: "))
                except ValueError:
                    print("Cantidad inválida.")
                    continue

                if unidades <= 0:
                    print("La cantidad debe ser mayor a 0.")
                    continue

                if unidades <= producto[3]:
                    nueva_cantidad = producto[3] - unidades
                    db.agregar_al_carrito(cursor, conexion, user_id, prod_id, unidades)
                    db.actualizar_stock_producto(cursor, conexion, prod_id, nueva_cantidad)
                    print("✅ Se ha añadido al carrito.")
                else:
                    print(f"\n❌ Lo siento, no hay suficiente stock. Disponible: {producto[3]}")

            seguir = input("\n¿Deseas seguir comprando? (1=Si / 2=No): ")
            if seguir != "1":
                return

    except Exception as e:
        print(f"Error en compra: {e}")


# ═══════════════════════════════════════════════════════════════════════
#  CARRITO / VENTA (Usuario)
# ═══════════════════════════════════════════════════════════════════════


def ver_carrito(user_id, nombre, cursor, conexion):
    """Muestra el carrito, permite eliminar items y proceder al pago."""
    try:
        items = db.obtener_carrito_usuario(cursor, user_id)
        if not items:
            print(f"\n[--------- Carrito de {nombre} ---------]")
            print("🛒 Tu carrito está vacío.")
            return

        while True:
            print(f"\n[--------- Carrito de {nombre} ---------]")
            total = 0.0
            detalle_items = []

            for item in items:
                # item: (id_carrito, nombre_producto, precio, cantidad, categoria)
                precio = float(item[2])
                cant = item[3]
                subtotal = precio * cant
                total += subtotal
                detalle_items.append((item[1], precio, cant, subtotal, item[4]))
                print(f"  ID: {item[0]} | {item[1]:<25} | ${precio:>6.2f} x {cant} = ${subtotal:>7.2f} | Cat: {item[4]}")

            print(f"\n  {'='*50}")
            print(f"  TOTAL A PAGAR: ${total:.2f}")

            print("\n 1.- Proceder al pago")
            print(" 2.- Eliminar artículo")
            print(" 3.- Regresar")
            opcion = input("\nOpción: ")

            if opcion == "1":
                procesar_pago(user_id, nombre, cursor, conexion, items, total)
                return

            elif opcion == "2":
                try:
                    item_id = input("\nIngrese el ID del artículo a eliminar: ")
                    db.eliminar_item_carrito(cursor, conexion, user_id, item_id)
                    print("✅ Artículo eliminado del carrito.")
                except Exception as e:
                    print(f"Error al eliminar: {e}")
                # Refrescar items
                items = db.obtener_carrito_usuario(cursor, user_id)
                if not items:
                    print("\n🛒 Tu carrito está vacío.")
                    return

            elif opcion == "3":
                return
            else:
                print("\n❌ Opción inválida.")

    except Exception as e:
        print(f"Error en carrito: {e}")


# ═══════════════════════════════════════════════════════════════════════
#  PAGO Y CAMBIO (NUEVA FUNCIONALIDAD)
# ═══════════════════════════════════════════════════════════════════════


def procesar_pago(user_id, nombre, cursor, conexion, items, total):
    """
    Procesa el pago: solicita monto, calcula cambio,
    registra ventas en BD y genera ticket TXT.
    """
    print("\n" + "=" * 50)
    print("              💳 PROCESO DE PAGO")
    print("=" * 50)

    print(f"\n  TOTAL A PAGAR: ${total:.2f}")
    print("-" * 50)

    # Solicitar monto con validación
    while True:
        try:
            pago = float(input("  Monto con el que pagas: $"))
            if pago < total:
                print(f"  ❌ El monto es insuficiente. Faltan ${total - pago:.2f}")
            else:
                break
        except ValueError:
            print("  ❌ Ingresa un monto válido.")

    cambio = pago - total

    print(f"\n  {'PAGO':>30}: ${pago:.2f}")
    print(f"  {'TOTAL':>30}: ${total:.2f}")
    print(f"  {'CAMBIO':>30}: ${cambio:.2f}")
    print("-" * 50)

    confirmar = input("\n  ¿Confirmar pago? (1=Si / 2=No): ")
    if confirmar != "1":
        print("  Pago cancelado.")
        return

    # Registrar cada producto como venta individual
    for item in items:
        # item: (id_carrito, nombre_producto, precio, cantidad, categoria)
        producto_id = None
        cursor.execute(
            "SELECT ID FROM PRODUCTOS WHERE NOMBRE_ARTICULO = ?", (item[1],)
        )
        resultado = cursor.fetchone()
        if resultado:
            producto_id = resultado[0]

        subtotal = float(item[2]) * item[3]
        db.registrar_venta(cursor, conexion, user_id, producto_id, subtotal)

    # Generar ticket
    ticket_file = generar_ticket(nombre, items, total, pago, cambio)
    print(f"\n  ✅ Pago realizado con éxito.")
    print(f"  🧾 Ticket generado: {ticket_file}")

    # Limpiar carrito
    db.limpiar_carrito_usuario(cursor, conexion, user_id)

    input("\n  Presiona Enter para continuar...")


# ═══════════════════════════════════════════════════════════════════════
#  MOSTRAR VENTAS (Admin)
# ═══════════════════════════════════════════════════════════════════════


def mostrar_todas_ventas(user_id, nombre, cursor, conexion):
    """Muestra todas las ventas registradas."""
    try:
        ventas = db.obtener_todas_ventas(cursor)
        if not ventas:
            print("\nNo hay ventas registradas aún.")
        else:
            print("\n[------------------ TODAS LAS VENTAS ------------------]")
            for v in ventas:
                print(f"  ID: {v[0]} | Usuario: {v[1]} | Producto: {v[2]} | Total: ${v[3]:.2f}")
                print("-" * 60)
    except Exception as e:
        print(f"Error al mostrar ventas: {e}")

    input("\nPresiona Enter para volver al menú...")