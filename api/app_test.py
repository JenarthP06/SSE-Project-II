import unittest
import requests


class TestUserProfileAPI(unittest.TestCase):
    base_url = "http://127.0.0.1:5000/user"

    def test_create_user_profile(self):
        # Test creating a new user profile
        data = {"username": "test_user", "email": "test@example.com"}
        response = requests.post(f"{self.base_url}", json=data)

        self.assertEqual(response.status_code, 201)
        self.assertIn("user_id", response.json())
        user_id = response.json()["user_id"]

        # Test retrieving the created user profile
        response = requests.get(f"{self.base_url}/{user_id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], data["username"])
        self.assertEqual(response.json()["email"], data["email"])

    def test_create_user_profile_invalid_input(self):
        # Test creating a new user profile with invalid input
        data = {"invalid_field": "test_user"}
        response = requests.post(f"{self.base_url}", json=data)

        self.assertEqual(response.status_code, 400)

    def test_get_nonexistent_user_profile(self):
        # Test retrieving a nonexistent user profile
        response = requests.get(f"{self.base_url}/nonexistent_user")

        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
