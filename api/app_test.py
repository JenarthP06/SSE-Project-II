import unittest
import json
import requests
from app import app

class TestAppEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def send_post_request(self, endpoint, data):
        url = f'http://127.0.0.1:5000{endpoint}'
        headers = {'Content-type': 'application/json'}
        response = requests.post(url, json=data, headers=headers)
        return response
    
    def send_get_request(self, endpoint, params=None):
        url = f'http://127.0.0.1:5000{endpoint}'
        headers = {'Content-type': 'application/json'}
        response = requests.get(url, params=params, headers=headers)
        return response

    def test_add_favourite(self):
        data = {"username": "test_user", "show": "test_show"}
        response = self.send_post_request('/addfavourite', data)

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['message'], 'success')

    def test_delete_favourite(self):
        data = {"username": "test_user", "show": "test_show"}
        response = self.send_post_request('/deletefavourite', data)

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['message'], 'success')

    def test_display_favourite(self):
        params = {"username": "test_user"}
        response = self.send_get_request('/displayfavourite', params=params)

        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
