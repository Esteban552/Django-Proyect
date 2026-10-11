from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category, Product


class CategoryAPITests(APITestCase):
    def test_crear_categoria(self):
        url = reverse('categories-list')
        data = {'name': 'Electronica'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Electronica')
        self.assertTrue(Category.objects.filter(name='Electronica').exists())

    def test_listar_categorias(self):
        Category.objects.create(name='Ropa')
        Category.objects.create(name='Juguetes')

        response = self.client.get(reverse('categories-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(
            sorted(c['name'] for c in response.data),
            ['Juguetes', 'Ropa'],
        )


class ProductAPITests(APITestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username='tester', password='test1234')
        self.categoria = Category.objects.create(name='Electronica')
        token_response = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'tester', 'password': 'test1234'},
            format='json',
        )
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token_response.data['access']
        )
        self.datos_producto = {
            'name': 'Notebook',
            'description': 'Laptop de 16GB RAM',
            'price': '1299.99',
        }

    def test_crear_producto(self):
        response = self.client.post(
            reverse('products-list'), self.datos_producto, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Notebook')
        self.assertEqual(response.data['price'], '1299.99')
        self.assertEqual(Product.objects.count(), 1)

    def test_listar_productos(self):
        Product.objects.create(
            name='Notebook', description='Laptop', price='1299.99', category=self.categoria
        )
        Product.objects.create(
            name='Mouse', description='Inalambrico', price='25.50', category=self.categoria
        )

        response = self.client.get(reverse('products-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(
            sorted(p['name'] for p in response.data),
            ['Mouse', 'Notebook'],
        )

    def test_actualizar_producto(self):
        producto = Product.objects.create(
            name='Notebook', description='Laptop', price='1299.99', category=self.categoria
        )

        response = self.client.patch(
            reverse('products-detail', args=[producto.id]),
            {'name': 'Notebook Pro', 'price': '1599.99'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Notebook Pro')
        self.assertEqual(response.data['price'], '1599.99')
        producto.refresh_from_db()
        self.assertEqual(producto.name, 'Notebook Pro')
        self.assertEqual(producto.description, 'Laptop')
        self.assertEqual(str(producto.price), '1599.99')

    def test_eliminar_producto(self):
        producto = Product.objects.create(
            name='Notebook', description='Laptop', price='1299.99', category=self.categoria
        )

        response = self.client.delete(reverse('products-detail', args=[producto.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_filtrar_productos_por_categoria(self):
        ropa = Category.objects.create(name='Ropa')
        Product.objects.create(
            name='Notebook', description='Laptop', price='1299.99', category=self.categoria
        )
        Product.objects.create(
            name='Camisa', description='Algodon', price='35.00', category=ropa
        )

        response = self.client.get(
            reverse('products-list'), {'category': self.categoria.id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Notebook')

    def test_no_se_puede_listar_productos_sin_token(self):
        self.client.credentials()

        response = self.client.get(reverse('products-list'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_precio_final_autenticado(self):
        producto = Product.objects.create(
            name='Notebook',
            description='Laptop',
            price='100.00',
            category=self.categoria,
        )

        response = self.client.get(reverse('products-precio-final', args=[producto.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['precio_original']), '100.00')
        self.assertEqual(str(response.data['precio_final']), '90.00')

    def test_precio_final_sin_categoria_no_revienta(self):
        producto = Product.objects.create(
            name='Sin categoria', description='X', price='100.00'
        )

        response = self.client.get(reverse('products-precio-final', args=[producto.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['precio_final']), '100.00')

    def test_precio_final_inexistente_devuelve_404(self):
        response = self.client.get(reverse('products-precio-final', args=[999999]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_precio_final_sin_autenticar(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(reverse('products-precio-final', args=[1]))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
