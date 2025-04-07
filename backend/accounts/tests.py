from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class SignupAPITestCase(APITestCase):
    """Test cases for the user registration (signup) endpoint."""

    def setUp(self):
        self.signup_url = reverse('signup')
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "Password123!",
            "password2": "Password123!"
        }

    def test_signup_success(self):
        """
        Test that a user is successfully registered when valid data is provided.
        """
        response = self.client.post(self.signup_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, self.user_data['username'])

    def test_signup_password_mismatch(self):
        """
        Test that an error is returned when the passwords do not match.
        """
        data = self.user_data.copy()
        data['password2'] = "DifferentPassword123!"
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_signup_missing_email(self):
        """
        Test that an error is returned when the email field is missing.
        """
        data = self.user_data.copy()
        data.pop('email')
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_signup_existing_username(self):
        """
        Test that an error is returned when attempting to register with an existing username.
        """
        # Register the first user
        self.client.post(self.signup_url, self.user_data, format='json')
        # Attempt to register another user with the same username
        data = self.user_data.copy()
        data['email'] = "anotheremail@example.com"  # Change email to test duplicate username
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Django validation may return the error in different formats, so we check if 'username' is mentioned.
        self.assertTrue('username' in response.data)
