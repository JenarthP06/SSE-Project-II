import unittest
import http.client
import json
from app import app


class TestAppEndpoints(unittest.TestCase):
    def setUp(self):
        # Set up a test client
        self.app = app.test_client()

    def send_post_request(self, endpoint, data):
        connection = http.client.HTTPConnection('127.0.0.1', 5000)
        headers = {'Content-type': 'application/json'}
        json_data = json.dumps(data)
        connection.request('POST', endpoint, json_data, headers)
        response = connection.getresponse()
        return response

    def test_add_favourite(self):
        # Test the /addfavourite endpoint
        data = {"username": "test_user", "show": "test_show"}
        response = self.send_post_request('/addfavourite', data)

        # Check if the response is successful
        self.assertEqual(response.status, 200)
        response_data = json.loads(response.read().decode())
        self.assertEqual(response_data['message'], 'success')

    def test_delete_favourite(self):
        # Test the /deletefavourite endpoint
        data = {"username": "test_user", "show": "test_show"}
        response = self.send_post_request('/deletefavourite', data)

        # Check if the response is successful
        self.assertEqual(response.status, 200)
        response_data = json.loads(response.read().decode())
        self.assertEqual(response_data['message'], 'success')

    def test_display_favourite(self):
        # Test the /displayfavourite endpoint
        data = {"username": "test_user"}
        response = self.send_post_request('/displayfavourite', data)

        # Check if the response is successful
        self.assertEqual(response.status, 200)
        # Add more specific assertions based on your expected response

    def tearDown(self):
        # Clean up or reset anything necessary after each test
        pass


if __name__ == '__main__':
    unittest.main()
