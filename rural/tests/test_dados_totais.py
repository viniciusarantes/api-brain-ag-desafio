from rest_framework import status, test

from rural.tests.utils import SetupTestMixin


class TotalDataTest(SetupTestMixin, test.APITestCase):
    def test_get_total_success_200(self):
        api_url = '/producer/total'
        total_area = 100
        self.make_producer(area_fazenda_ha=total_area)
        self.make_producer(area_fazenda_ha=total_area)
        response = self.client.get(api_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('total_fazendas'), 2)
        self.assertEqual(float(response.data.get('total_hectares')), float(total_area * 2))
