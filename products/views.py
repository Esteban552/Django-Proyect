from decimal import Decimal

from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from . import services
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return services.listar_categorias()

    def perform_create(self, serializer):
        serializer.instance = services.crear_categoria(serializer.validated_data['name'])


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

    def get_queryset(self):
        return services.listar_productos()

    def perform_create(self, serializer):
        serializer.instance = services.crear_producto(**serializer.validated_data)

    def perform_update(self, serializer):
        instancia = services.actualizar_producto(
            serializer.instance, **serializer.validated_data
        )
        serializer.instance = services.obtener_producto(instancia.pk)

    @action(detail=True, methods=['get'], url_path='precio-final')
    def precio_final(self, request, pk):
        try:
            producto = services.obtener_producto(pk)
        except services.ProductoNoEncontrado as exc:
            raise Http404(str(exc)) from exc

        precio_final = services.calcular_precio_final(producto)

        return Response({
            'producto': producto.name,
            'precio_original': producto.price,
            'precio_final': precio_final.quantize(Decimal('0.01')),
        })
