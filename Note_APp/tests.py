from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class UserTests(TestCase):

    def test_RegistarationOnSubmit_ThenReturn_HTTP_406_NOT_ACCEPTABLE(self):
        url = reverse("register")
        userData = {'username': '', 'email': '',
                    'password': '', 'confirm_password': ''}
        response = self.client.post(path=url, data=userData, format='json')
        self.assertEqual(response.status_code, 406)

    def test_RegistarationOnSubmit_ThenReturn_HTTP_200_OK(self):
        url = reverse("register")
        userData = {'username': 'Archana', 'email': 'archana1@gmail.com',
                    'password': '123', 'confirm_password': '123'}
        response = self.client.post(path=url, data=userData, format='json')
        self.assertEqual(response.status_code, 200)

    def test_RegistarationPasswordMissMatchOnSubmit_ThenReturn_HTTP_400_BAD_REQUEST(self):
        url = reverse("register")
        userData = {'username': 'Archana', 'email': 'archana@gmail.com',
                    'password': '123', 'confirm_password': '1234'}
        response = self.client.post(path=url, data=userData, format='json')
        self.assertEqual(response.status_code, 400)

    def test_LoginOnSubmit_ThenReturn_HTTP_202_ACCEPTED(self):
        url = reverse("login")
        userData = {'username': 'Archana', 'password': '123'}
        response = self.client.post(path=url, data=userData, format='json')
        self.assertEqual(response.status_code, 202)

    def test_LoginOnSubmitWithWrongPassword_ThenReturn_HTTP_406_NOT_ACCEPTABLE(self):
        url = reverse("login")
        userData = {'username': 'Archana', 'password': '1234'}
        response = self.client.post(path=url, data=userData, format='json')
        self.assertEqual(response.status_code, 406)

