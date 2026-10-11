from decimal import Decimal

from .models import Category, Product

CATEGORIA_DEFAULT = 'Sin categoría'


class ProductoNoEncontrado(Exception):
    pass


class EstrategiaDescuento:
    def calcular(self, precio):
        raise NotImplementedError


class DescuentoElectronica(EstrategiaDescuento):
    PORCENTAJE = Decimal('0.90')

    def calcular(self, precio):
        return precio * self.PORCENTAJE


class DescuentoRopa(EstrategiaDescuento):
    PORCENTAJE = Decimal('0.80')

    def calcular(self, precio):
        return precio * self.PORCENTAJE


class SinDescuento(EstrategiaDescuento):
    def calcular(self, precio):
        return precio


ESTRATEGIAS = {
    'Electronica': DescuentoElectronica,
    'Ropa': DescuentoRopa,
}


def obtener_estrategia(categoria_nombre):
    return ESTRATEGIAS.get(categoria_nombre, SinDescuento)()


def listar_categorias():
    return Category.objects.all()


def crear_categoria(nombre):
    return Category.objects.create(name=nombre)


def listar_productos():
    return Product.objects.all()


def obtener_producto(pk):
    try:
        return Product.objects.get(pk=pk)
    except Product.DoesNotExist as exc:
        raise ProductoNoEncontrado(f'No existe el producto con pk={pk}') from exc


def crear_producto(**datos):
    return Product.objects.create(**datos)


def actualizar_producto(instancia, **datos):
    for campo, valor in datos.items():
        setattr(instancia, campo, valor)
    instancia.save()
    return instancia


def crear_producto_con_categoria_default(name, description, price):
    categoria, _ = Category.objects.get_or_create(name=CATEGORIA_DEFAULT)
    return Product.objects.create(
        name=name,
        description=description,
        price=price,
        category=categoria,
    )


def calcular_precio_final(producto):
    categoria = producto.category.name if producto.category_id else None
    estrategia = obtener_estrategia(categoria)
    return estrategia.calcular(producto.price)
