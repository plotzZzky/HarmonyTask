from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
import json
import os

from .models import Recovery


# Esta função apaga todas as imagens geradas pelo test na pasta profiles/
# NÂO RENOMEAR essa função, o nome é o padrão definido pelo unittest
def tearDownModule():
    path = 'media/profiles/'
    if os.path.isdir(path):
        files = os.listdir(path)

        for file in files:
            path_file = os.path.join(path, file)
            if os.path.isfile(path_file):
                os.unlink(path_file)


class LoginTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'temporary',
            'password': '1234x567'}
        self.client = APIClient()
        self.user = User.objects.create_user(**self.credentials)
        self.token = Token.objects.create(user=self.user)  # type:ignore
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.credentials_error = {'username': 'user_error', 'password': '12334555'}

    def test_login_status(self):
        response = self.client.post('/users/login/', self.credentials)
        self.assertEqual(response.status_code, 200)

    def test_login_has_token(self):
        response = self.client.post('/users/login/', self.credentials)
        json_response = response.json()
        result = True if 'token' in json_response else False
        self.assertTrue(result)

    def test_login_content_type(self):
        response = self.client.post('/users/login/', self.credentials)
        try:
            j = json.loads(response.content)
        except Exception:
            j = False
        self.assertNotEqual(j, False)

    def test_login_status_error(self):
        response = self.client.post('/users/login/', self.credentials_error)
        self.assertEqual(response.status_code, 401)

    def test_login_status_error_empty(self):
        response = self.client.post('/users/login/', {})
        self.assertEqual(response.status_code, 400)


class RegisterTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'mewuser',
            'email': 'newuser@mail.com',
            'password': '1234x567',
            'pwd': '1234x567',
            'question': 'question',
            'answer': 'answer',
        }

    def test_register_status(self):
        response = self.client.post('/users/register/', self.credentials)
        self.assertEqual(response.status_code, 200)

    def test_register_check_token(self):
        response = self.client.post('/users/register/', self.credentials)
        user = User.objects.get(username=self.credentials['username'])
        token = Token.objects.get(user=user)  # type: ignore
        result = json.loads(response.content)
        self.assertEqual(result['token'], token.key)

    def test_register_status_error_username(self):
        credentials = {
            'username': 'aa',
            'email': 'newuser@mail.com',
            'password1': '1234x567',
            'password2': '1234x567'
        }
        response = self.client.post('/users/register/', json.dumps(credentials), content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_register_status_error_email(self):
        credentials = {
            'username': 'newuser',
            'email': '',
            'password1': '1234x567',
            'password2': '1234x567'
        }
        response = self.client.post('/users/register/', json.dumps(credentials), content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_register_status_error_password(self):
        credentials = {
            'username': 'newuser',
            'email': 'newuser@mail.com',
            'password1': '',
            'password2': '1234x567'
        }
        response = self.client.post('/users/register/', json.dumps(credentials), content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_register_status_error_pwd(self):
        credentials = {
            'username': 'newuser',
            'email': 'newuser@mail.com',
            'password1': '1234x567',
            'password2': ''
        }
        response = self.client.post('/users/register/', json.dumps(credentials), content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_register_status_error_pwd_diferent(self):
        credentials = {
            'username': 'newuser',
            'email': 'newuser@mail.com',
            'password1': '1233x567',
            'password2': '1234x567'
        }
        response = self.client.post('/users/register/', json.dumps(credentials), content_type="application/json")
        self.assertEqual(response.status_code, 401)


class RecoveryTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'usertest',
            'email': 'newuser@mail.com',
            'password': '1234x567',
        }
        self.recovery = {
            'question': 'question',
            'answer': 'answer',
        }
        self.client = APIClient()
        self.user = User.objects.create_user(**self.credentials)
        self.token = Token.objects.create(user=self.user)  # type:ignore
        self.recovery = Recovery.objects.create(
            user=self.user,
            question=self.recovery['question'],
            answer=self.recovery['answer'],
        )
        self.credentials_error = {'username': 'user_error', 'password': '12334555'}

    def test_receive_question_status(self):
        data = {"username": 'usertest'}
        response = self.client.post('/users/question/', data)
        self.assertEqual(response.status_code, 200)

    def test_receive_question_content(self):
        data = {"username": 'usertest'}
        response = self.client.post('/users/question/', data)
        json_response = response.json()
        result = True if 'question' in json_response else False
        self.assertTrue(result)
