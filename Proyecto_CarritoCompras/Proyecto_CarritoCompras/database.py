"""
database.py - Capa de acceso a base de datos SQLite
Todas las consultas SQL están encapsuladas aquí.
"""
import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).parent / "DataBaseMercado.db"


def connect_database():
    """Abre conexión con la base de datos SQLite."""
    conexion = sqlite3.connect(str(DB_PATH))
    cursor = conexion.cursor()
    return conexion, cursor


def close_database(conexion):
    """Cierra la conexión a la base de datos."""
    if conexion:
        conexion.close()


# ─── USUARIOS ────────────────────────────────────────────────────────


def crear_usuario(cursor, conexion, nombre, contrasena_encriptada, correo, numero):
    cursor.execute(
        "INSERT INTO USUARIOS VALUES (?,?,?,?,?)",
        (None, nombre, contrasena_encriptada, correo, numero),
    )
    conexion.commit()


def crear_empleado(cursor, conexion, nombre, contrasena_encriptada, correo, numero):
    cursor.execute(
        "INSERT INTO EMPLEADOS VALUES (?,?,?,?,?,?)",
        (None, nombre, contrasena_encriptada, correo, numero, 0.00),
    )
    conexion.commit()


def buscar_usuario_por_correo(cursor, correo):
    cursor.execute(
        "SELECT ID, NOMBRE, CONTRASENA FROM USUARIOS WHERE CORREO = ?", (correo,)
    )
    return cursor.fetchone()  # (id, nombre, contrasena) | None


def buscar_empleado_por_correo(cursor, correo):
    cursor.execute(
        "SELECT ID, NOMBRE, CONTRASENA FROM EMPLEADOS WHERE CORREO = ?", (correo,)
    )
    return cursor.fetchone()  # (id, nombre, contrasena) | None


# ─── PRODUCTOS ────────────────────────────────────────────────────────


def obtener_productos(cursor):
    cursor.execute("SELECT * FROM PRODUCTOS")
    return cursor.fetchall()


def agregar_producto(cursor, conexion, nombre, precio, cantidad, categoria_id):
    cursor.execute(
        "INSERT INTO PRODUCTOS VALUES (?,?,?,?,?)",
        (None, nombre, precio, cantidad, categoria_id),
    )
    conexion.commit()


def eliminar_producto(cursor, conexion, producto_id):
    cursor.execute("DELETE FROM PRODUCTOS WHERE ID = ?", (producto_id,))
    conexion.commit()


def obtener_productos_por_categoria(cursor, categoria_id):
    cursor.execute(
        "SELECT ID, NOMBRE_ARTICULO, PRECIO, CANTIDAD FROM PRODUCTOS WHERE CATEGORIA_ID = ?",
        (categoria_id,),
    )
    return cursor.fetchall()


def actualizar_stock_producto(cursor, conexion, producto_id, nueva_cantidad):
    cursor.execute(
        "UPDATE PRODUCTOS SET CANTIDAD = ? WHERE ID = ?",
        (nueva_cantidad, producto_id),
    )
    conexion.commit()


# ─── CATEGORÍAS ──────────────────────────────────────────────────────


def obtener_categorias(cursor):
    cursor.execute("SELECT * FROM CATEGORIA")
    return cursor.fetchall()


def agregar_categoria(cursor, conexion, nombre, descripcion):
    cursor.execute("INSERT INTO CATEGORIA VALUES (?,?,?)", (None, nombre, descripcion))
    conexion.commit()


def eliminar_categoria(cursor, conexion, categoria_id):
    cursor.execute("DELETE FROM CATEGORIA WHERE ID = ?", (categoria_id,))
    conexion.commit()


# ─── CARRITO ─────────────────────────────────────────────────────────


def agregar_al_carrito(cursor, conexion, usuario_id, producto_id, unidades):
    cursor.execute(
        "INSERT INTO Carrito_Compras VALUES (?,?,?,?)",
        [None, usuario_id, producto_id, unidades],
    )
    conexion.commit()


def obtener_carrito_usuario(cursor, usuario_id):
    cursor.execute(
        """
        SELECT Carrito_Compras.ID, PRODUCTOS.NOMBRE_ARTICULO,
               PRODUCTOS.PRECIO, Carrito_Compras.CANTIDAD, CATEGORIA.NOMBRE
        FROM Carrito_Compras
        INNER JOIN PRODUCTOS ON Carrito_Compras.PRODUCTO_ID = PRODUCTOS.ID
        INNER JOIN CATEGORIA ON PRODUCTOS.CATEGORIA_ID = CATEGORIA.ID
        WHERE Carrito_Compras.USER_ID = ?
        """,
        (usuario_id,),
    )
    return cursor.fetchall()


def eliminar_item_carrito(cursor, conexion, usuario_id, item_id):
    cursor.execute(
        "DELETE FROM Carrito_Compras WHERE USER_ID = ? AND ID = ?",
        (usuario_id, item_id),
    )
    conexion.commit()


def limpiar_carrito_usuario(cursor, conexion, usuario_id):
    cursor.execute("DELETE FROM Carrito_Compras WHERE USER_ID = ?", (usuario_id,))
    conexion.commit()


# ─── VENTAS ──────────────────────────────────────────────────────────


def registrar_venta(cursor, conexion, usuario_id, producto_id, total):
    cursor.execute(
        "INSERT INTO VENTAS VALUES (?,?,?,?)",
        (None, usuario_id, producto_id, total),
    )
    conexion.commit()


def obtener_todas_ventas(cursor):
    cursor.execute(
        """
        SELECT VENTAS.ID, USUARIOS.NOMBRE, PRODUCTOS.NOMBRE_ARTICULO, VENTAS.TOTAL
        FROM VENTAS
        INNER JOIN USUARIOS ON VENTAS.USUARIO_ID = USUARIOS.ID
        INNER JOIN PRODUCTOS ON VENTAS.PRODUCTO_ID = PRODUCTOS.ID
        """
    )
    return cursor.fetchall()