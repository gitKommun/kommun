from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json

class UserAuthTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.registration_url = reverse('register-main-contact-community')
        self.login_url = reverse('user-login')
        self.user_data = {
            "email": "testuser@example.com",
            "password": "testpassword123",
            "name": "Test",
            "surnames": "User"
        }
        
    def test_user_registration_and_login(self):
        print("Testing user registration and login")
        # User registration
        response = self.client.post(self.registration_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print("User registration validated")

        # User login
        response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.csrf_token = response.cookies['csrftoken'].value
        self.sessionid = response.cookies['sessionid'].value
        print("User login validated")
        
        # Set credentials for further requests
        self.client.cookies['csrftoken'] = self.csrf_token
        self.client.cookies['sessionid'] = self.sessionid

        # Example request using session and CSRF token
        example_url = reverse('get_user_data')
        response = self.client.get(example_url, format='json', HTTP_X_CSRFTOKEN=self.csrf_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user_data['email'])
        self.assertEqual(response.data['name'], self.user_data['name'])
        self.assertEqual(response.data['surnames'], self.user_data['surnames'])
        print("Get user data /me validated")
        
        
    def test_user_logout(self):
        print("Testing user logout")
        # User registration
        self.client.post(self.registration_url, self.user_data, format='json')

        # User login
        response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.csrf_token = response.cookies['csrftoken'].value
        self.sessionid = response.cookies['sessionid'].value
        
        # Set credentials for further requests
        self.client.cookies['csrftoken'] = self.csrf_token
        self.client.cookies['sessionid'] = self.sessionid

        # User logout
        logout_url = reverse('user-logout')
        response = self.client.post(logout_url, format='json', HTTP_X_CSRFTOKEN=self.csrf_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['logged_out'])
        print("User logout validated")
        

