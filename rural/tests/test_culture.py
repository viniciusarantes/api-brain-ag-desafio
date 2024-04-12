from django.urls import reverse
from rest_framework import status, test

from rural.tests.utils import SetupTestMixin


class ListCultureTest(SetupTestMixin, test.APITestCase):
    def test_get_culture_list_success_200(self):
        api_url = reverse('culture-list')
        cultures = [self.make_culture()]
        response = self.client.get(api_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(cultures))


class CreateCultureTest(SetupTestMixin, test.APITestCase):
    def test_post_culture_success_200(self):
        api_url = reverse('culture-list')
        data = {"nome": "Milho"}
        response = self.client.post(api_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('nome'), data.get('nome'))
    
    def test_post_culture_bad_request_400(self):
        api_url = reverse('culture-list')
        data = {}
        response = self.client.post(api_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CultureDetailsTest(SetupTestMixin, test.APITestCase):
    def test_get_culture_success_200(self):
        culture = self.make_culture()
        api_url = f'/culture/{culture.id}/'
        response = self.client.get(api_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('nome'), culture.nome)
    
    def test_get_culture_not_found_404(self):
        api_url = '/culture/999/'
        response = self.client.get(api_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateCultureTest(SetupTestMixin, test.APITestCase):
    def test_patch_culture_success_200(self):
        culture = self.make_culture()
        api_url = f'/culture/{culture.id}/'
        data = {'nome': 'Nome atualizado'}
        response = self.client.patch(api_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('nome'), data.get('nome'))
    
    def test_patch_culture_not_found_404(self):
        api_url = '/culture/999/'
        data = {'nome': 'Nome atualizado'}
        response = self.client.patch(api_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteCultureTest(SetupTestMixin, test.APITestCase):
    def test_delete_culture_success_204(self):
        culture = self.make_culture()
        api_url = f'/culture/{culture.id}/'
        response = self.client.delete(api_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_culture_not_found_404(self):
        api_url = '/culture/999/'
        response = self.client.delete(api_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
