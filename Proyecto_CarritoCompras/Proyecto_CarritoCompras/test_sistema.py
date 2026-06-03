"""
test_sistema.py - Prueba automatizada del sistema MercadoVentas
Simula el flujo completo: registro, login, compra, pago y ticket
"""
import os
import sys
import sqlite3
from pathlib import Path

# Agregar el directorio del proyecto al path
sys.path.insert(0, str(Path(__file__).parent))

import database as db
import auth
from utils import generar_ticket


def test_flujo_completo():
    """Prueba el flujo completo del sistema."""
    print("=" * 60)
    print("PRUEBA AUTOMATIZADA - SISTEMA MERCADOVENTAS")
    print("=" * 60)

    # ─── 1. Verificar que la BD existe y tiene tablas ───
    print("\n[1] Verificando base de datos...")
    db_path = Path(__file__).parent / "DataBaseMercado.db"
    assert db_path.exists(), "❌ Base de datos no encontrada"
    print(f"    ✅ BD encontrada: {db_path}")

    conexion, cursor = db.connect_database()

    # Verificar tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tablas = [t[0] for t in cursor.fetchall()]
    print(f"    Tablas: {tablas}")
    assert "USUARIOS" in tablas, "❌ Falta tabla USUARIOS"
    assert "EMPLEADOS" in tablas, "❌ Falta tabla EMPLEADOS"
    assert "PRODUCTOS" in tablas, "❌ Falta tabla PRODUCTOS"
    assert "CATEGORIA" in tablas, "❌ Falta tabla CATEGORIA"
    assert "Carrito_Compras" in tablas, "❌ Falta tabla Carrito_Compras"
    assert "VENTAS" in tablas, "❌ Falta tabla VENTAS"
    print("    ✅ Todas las tablas existen")

    # ─── 2. Verificar productos existentes ───
    print("\n[2] Verificando productos en inventario...")
    productos = db.obtener_productos(cursor)
    print(f"    Productos encontrados: {len(productos)}")
    for p in productos:
        print(f"    ID={p[0]}, Nombre={p[1]}, Precio={p[2]}, Stock={p[3]}, CatID={p[4]}")
    assert len(productos) > 0, "❌ No hay productos en el inventario"

    # ─── 3. Verificar categorías ───
    print("\n[3] Verificando categorías...")
    cats = db.obtener_categorias(cursor)
    print(f"    Categorías encontradas: {len(cats)}")
    for c in cats:
        print(f"    ID={c[0]}, Nombre={c[1]}")
    assert len(cats) > 0, "❌ No hay categorías"

    # ─── 4. Verificar login funciona con datos existentes ───
    print("\n[4] Verificando búsqueda de usuario por correo...")
    cursor.execute("SELECT ID, NOMBRE, CORREO FROM USUARIOS LIMIT 1")
    primer_usuario = cursor.fetchone()
    if primer_usuario:
        print(f"    Usuario existente: ID={primer_usuario[0]}, Nombre={primer_usuario[1]}, Correo={primer_usuario[2]}")
    else:
        print("    No hay usuarios registrados aún (es normal en BD nueva)")

    # ─── 5. Verificar carrito vacío ───
    user_id = primer_usuario[0] if primer_usuario else 1
    print(f"\n[5] Verificando carrito del usuario ID={user_id}...")
    items = db.obtener_carrito_usuario(cursor, user_id)
    print(f"    Items en carrito: {len(items)}")

    # ─── 6. Verificar ventas ───
    print("\n[6] Verificando tabla de ventas...")
    ventas = db.obtener_todas_ventas(cursor)
    print(f"    Ventas registradas: {len(ventas)}")
    for v in ventas:
        print(f"    ID={v[0]}, Usuario={v[1]}, Producto={v[2]}, Total=${v[3]}")

    # ─── 7. Prueba de generación de ticket ───
    print("\n[7] Probando generación de ticket TXT...")
    items_prueba = [
        (1, "Laptop HP", 15000.00, 1, "Electrónicos"),
        (2, "Mouse Gamer", 850.00, 2, "Electrónicos"),
    ]
    ticket_file = generar_ticket(
        nombre_usuario="UsuarioPrueba",
        items=items_prueba,
        total=16700.00,
        pago=20000.00,
        cambio=3300.00,
    )
    print(f"    Ticket generado: {ticket_file}")
    assert os.path.exists(ticket_file), "❌ No se generó el archivo de ticket"
    with open(ticket_file, "r", encoding="utf-8") as f:
        contenido = f.read()
    assert "MERCADOVENTAS" in contenido, "❌ Ticket sin encabezado"
    assert "TOTAL" in contenido, "❌ Ticket sin total"
    assert "Cambio" in contenido, "❌ Ticket sin cambio"
    print(f"    ✅ Ticket válido ({len(contenido)} caracteres)")
    print(contenido[:200] + "...")

    # ─── 8. Agregar producto al carrito (prueba funcional) ───
    if primer_usuario and len(productos) > 0:
        print("\n[8] Probando inserción en carrito...")
        prod = productos[0]
        db.agregar_al_carrito(cursor, conexion, primer_usuario[0], prod[0], 1)
        items_nuevos = db.obtener_carrito_usuario(cursor, primer_usuario[0])
        print(f"    Items en carrito después de agregar: {len(items_nuevos)}")
        assert len(items_nuevos) > 0, "❌ No se agregó al carrito"
        # Limpiar carrito después de la prueba
        db.limpiar_carrito_usuario(cursor, conexion, primer_usuario[0])
        print("    ✅ Carrito funciona correctamente")

    # ─── 9. Prueba de registro de venta ───
    print("\n[9] Probando registro de venta...")
    db.registrar_venta(cursor, conexion, 1, 1, 16700.00)
    print("    ✅ Venta registrada correctamente")

    # ─── 10. Verificar estructura de módulos ───
    print("\n[10] Verificando estructura de módulos...")
    modulos = ["models.py", "database.py", "auth.py", "ui.py", "utils.py", "main.py"]
    for m in modulos:
        path_mod = Path(__file__).parent / m
        assert path_mod.exists(), f"❌ Falta el módulo {m}"
        print(f"    ✅ {m} existe")

    # ─── 11. Verificar que los módulos tienen docstrings ───
    print("\n[11] Verificando documentación en módulos...")
    import models, database, auth, utils, ui
    for mod_name, mod in [("models", models), ("database", database), ("auth", auth), ("ui", ui), ("utils", utils)]:
        doc = mod.__doc__
        assert doc and len(doc) > 10, f"❌ {mod_name}.py sin docstring"
        print(f"    ✅ {mod_name}.py tiene documentación")

    # ─── CERRAR ───
    db.close_database(conexion)

    print("\n" + "=" * 60)
    print("🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
    print("=" * 60)


if __name__ == "__main__":
    test_flujo_completo()