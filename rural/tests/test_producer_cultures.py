from rest_framework import status, test

from rural.tests.utils import SetupTestMixin


class AddProducerCulturesTest(SetupTestMixin, test.APITestCase):
    def test_add_culture_success_200(self):
        api_url = '/producer/add_culture'
        producer = self.make_producer()
        culture = self.make_culture()
        data = {
            "produtor_id": producer.id,
            "cultura_vegetal": [culture.id]
        }
        response = self.client.post(api_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('cultura_vegetal')), 1)
    
    def test_add_culture_not_found_producer_404(self):
        api_url = '/producer/add_culture'
        culture = self.make_culture()
        data = {
            "produtor_id": 999,
            "cultura_vegetal": [culture.id]
        }
        response = self.client.post(api_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('Produtor id não encontrado' in response.data.get('detail'))
    
    def test_add_culture_not_found_culture_404(self):
        api_url = '/producer/add_culture'
        producer = self.make_producer()
        data = {
            "produtor_id": producer.id,
            "cultura_vegetal": [888, 999]
        }
        response = self.client.post(api_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('Culturas Vegetais não encontradas' in response.data.get('detail'))


class RemoveProducerCulturesTest(SetupTestMixin, test.APITestCase):
    def test_remove_culture_success_200(self):
        api_url = '/producer/remove_culture'
        producer = self.make_producer_with_culture(2)
        data = {
            "produtor_id": producer.id,
            "cultura_vegetal": [1]
        }
        response = self.client.post(api_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('cultura_vegetal')), 1)
    
    def test_remove_culture_not_found_producer_404(self):
        api_url = '/producer/remove_culture'
        culture = self.make_culture()
        data = {
            "produtor_id": 999,
            "cultura_vegetal": [culture.id]
        }
        response = self.client.post(api_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('Produtor id não encontrado' in response.data.get('detail'))
    
    def test_remove_culture_not_found_culture_404(self):
        api_url = '/producer/remove_culture'
        producer = self.make_producer()
        data = {
            "produtor_id": producer.id,
            "cultura_vegetal": [888, 999]
        }
        response = self.client.post(api_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('Culturas Vegetais não encontradas' in response.data.get('detail'))