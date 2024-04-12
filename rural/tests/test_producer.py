from django.urls import reverse
from rest_framework import status, test

from rural.tests.utils import SetupTestMixin


class ListProducerTest(SetupTestMixin, test.APITestCase):
    def test_get_producer_list_200(self):
        api_url = reverse('producer-list')
        producers = [self.make_producer()]
        response = self.client.get(api_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(producers))


class CreateProducerTest(SetupTestMixin, test.APITestCase):
    def test_post_producer_success_201(self):
        api_url = reverse('producer-list')
        data = self.get_producer_obj()
        response = self.client.post(api_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('cpf_cnpj'), data.get('cpf_cnpj'))
    
    def test_post_producer_required_field_400(self):
        api_url = reverse('producer-list')
        data = self.get_producer_obj()
        del data['nome_produtor']
        response = self.client.post(api_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_producer_invalid_cpf_length_400(self):
        api_url = reverse('producer-list')
        data = self.get_producer_obj()
        data['cpf_cnpj'] = '123'
        response = self.client.post(api_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("CPF/CNPJ inválido" in response.data.get('detail'))
    
    def test_post_producer_invalid_cpf_value_400(self):
        api_url = reverse('producer-list')
        data = self.get_producer_obj()
        data['cpf_cnpj'] = '111.111.111-11'
        response = self.client.post(api_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("CPF/CNPJ inválido" in response.data.get('detail'))
    
    def test_post_producer_invalid_cnpj_value_400(self):
        api_url = reverse('producer-list')
        data = self.get_producer_obj()
        data['cpf_cnpj'] = '12.123.123/0001-12'
        response = self.client.post(api_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("CPF/CNPJ inválido" in response.data.get('detail'))
    
    def test_post_producer_invalid_area_limit_400(self):
        api_url = reverse('producer-list')
        data = self.get_producer_obj()
        data['area_agricultavel_ha'] = 20
        data['area_vegetacao_ha'] = 30
        data['area_fazenda_ha'] = 45
        response = self.client.post(api_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("ultrapassa a área total" in response.data.get('detail'))


class ProducerDetailsTest(SetupTestMixin, test.APITestCase):
    def test_get_producer_by_id_success_200(self):
        producer = self.make_producer()
        api_url = f'/producer/{producer.id}/'
        response = self.client.get(api_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('cpf_cnpj'), producer.cpf_cnpj)
    
    def test_get_producer_by_id_not_found_404(self):
        api_url = '/producer/999/'
        response = self.client.get(api_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateProducerTest(SetupTestMixin, test.APITestCase):
    def test_patch_producer_success_200(self):
        producer = self.make_producer()
        api_url = f'/producer/{producer.id}/'
        data = {'nome_produtor': 'Nome atualizado'}
        response = self.client.patch(api_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('nome_produtor'), data.get('nome_produtor'))
    
    def test_patch_producer_not_found_404(self):
        api_url = '/producer/999/'
        data = {'nome_produtor': 'Nome atualizado'}
        response = self.client.patch(api_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_patch_producer_invalid_cpf_400(self):
        producer = self.make_producer()
        api_url = f'/producer/{producer.id}/'
        data = {'cpf_cnpj': '123'}
        response = self.client.patch(api_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("CPF/CNPJ inválido" in response.data.get('detail'))
    
    def test_patch_producer_invalid_area_limit_400(self):
        producer = self.make_producer(
            area_fazenda_ha=100,
            area_agricultavel_ha=70,
            area_vegetacao_ha=30
        )
        api_url = f'/producer/{producer.id}/'
        data = {'area_vegetacao_ha': 50}
        response = self.client.patch(api_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("ultrapassa a área total" in response.data.get('detail'))


class DeleteProducerTest(SetupTestMixin, test.APITestCase):
    def test_delete_producer_success_204(self):
        producer = self.make_producer()
        api_url = f'/producer/{producer.id}/'
        response = self.client.delete(api_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_producer_not_found_404(self):
        api_url = '/producer/999/'
        response = self.client.delete(api_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
