"""
models.py - Clases del dominio de MercadoVentas
Define las entidades: User, Admin, Producto, Carrito, Venta
"""


class User:
    """Representa un usuario comprador del sistema."""
    def __init__(self, nombre, contrasena, correo, numero):
        self.nombre = nombre
        self.contrasena = contrasena
        self.correo = correo
        self.numero = numero


class Admin(User):
    """Representa un empleado/administrador del sistema."""
    def __init__(self, nombre, contrasena, correo, numero):
        super().__init__(nombre, contrasena, correo, numero)


class Producto:
    """Representa un producto del inventario."""
    def __init__(self, id_producto, nombre, precio, cantidad, categoria_id):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.categoria_id = categoria_id

    def __str__(self):
        return f"{self.nombre} - ${self.precio:.2f} ({self.cantidad} disp.)"


class CarritoItem:
    """Representa un ítem dentro del carrito de compras."""
    def __init__(self, id_item, producto_id, nombre_producto,
                 precio_unitario, cantidad, categoria):
        self.id_item = id_item
        self.producto_id = producto_id
        self.nombre_producto = nombre_producto
        self.precio_unitario = precio_unitario
        self.cantidad = cantidad
        self.categoria = categoria

    @property
    def subtotal(self):
        return self.precio_unitario * self.cantidad


class Venta:
    """Representa una venta realizada."""
    def __init__(self, id_venta, usuario_id, producto_id, total, fecha=None):
        self.id_venta = id_venta
        self.usuario_id = usuario_id
        self.producto_id = producto_id
        self.total = total
        self.fecha = fecha