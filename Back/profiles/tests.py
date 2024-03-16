from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ObjectDoesNotExist
from PIL import Image
import io

from .models import Profile, Favorite


class ProfileTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'temporary',
            'password': '1234x567'}
        self.client = APIClient()
        self.user = User.objects.create_user(**self.credentials)
        self.token = Token.objects.create(user=self.user)  # type:ignore
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.credentials_error = {'username': 'user_error', 'password': '12334555'}
        self.profile = self.create_profile()

        self.profile_data = {
            "picture": self.uploaded_file,
            "name": 'name',
            "lastName": 'lastname',
            "area": 'Outros',
            "profession": 'user',
            "email": 'user@mail.com',
            "telephone": '(00)0000-0000',
            "description": 'my profile',
            "active": 'true'
        }

    def create_profile(self):
        image_temp = Image.new('RGB', (100, 100))
        image_io = io.BytesIO()
        image_temp.save(image_io, format='PNG')
        image_io.seek(0)
        self.uploaded_file = SimpleUploadedFile('test_image.png', image_io.read(), content_type='image/png')

        profile = Profile.objects.create(
            user=self.user,
            picture=self.uploaded_file,
            name='name',
            lastname='lastname',
            area='Outros',
            profession='user',
            email='user@mail.com',
            telephone='(00)0000-0000',
            description='my profile',
            active=True
        )
        return profile

    def test_get_all_profile_status(self):
        response = self.client.get('/profiles/all/')
        self.assertTrue(response.status_code, 200)

    def test_get_all_profile_json(self):
        response = self.client.get('/profiles/all/')
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_get_all_profiles_no_login_error(self):
        self.client.credentials()
        response = self.client.get('/profiles/all/')
        self.assertEqual(response.status_code, 401)

    def test_get_user_profile(self):
        user_id = self.user.profile.id
        response = self.client.post('/profiles/all/', {'profileId': user_id})
        self.assertEqual(response.status_code, 200)

    def test_get_user_profile_json(self):
        response = self.client.post('/profiles/all/')
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_get_user_profile_id_not_exists_error(self):
        user_id = 9999
        response = self.client.post('/profiles/all/', {'profileId': user_id})
        self.assertEqual(response.status_code, 404)

    # Your Profile
    def test_get_your_profile_status(self):
        response = self.client.get('/profiles/your/')
        self.assertEqual(response.status_code, 200)

    def test_get_your_profile_is_json(self):
        response = self.client.post('/profiles/your/')
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_update_your_profile_status(self):
        response = self.client.post('/profiles/your/', self.profile_data)
        self.assertEqual(response.status_code, 200)

    def test_update_your_profile_is_json(self):
        response = self.client.post('/profiles/your/', self.profile_data)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_create_your_profile_status(self):
        profile = Profile.objects.get(pk=self.profile.id)
        profile.delete()
        response = self.client.post('/profiles/your/', self.profile_data)
        self.assertEqual(response.status_code, 200)

    def test_create_your_profile_status_error(self):
        profile = Profile.objects.get(pk=self.profile.id)
        profile.delete()
        response = self.client.post('/profiles/your/')
        self.profile = self.create_profile()  # recria o perfil para evitar bugar outros testes
        self.assertEqual(response.status_code, 500)

    # Favorites
    def test_create_favorite_status(self):
        data = {'profileId': self.profile.id}
        response = self.client.post('/profiles/favorites/', data)
        self.assertEqual(response.status_code, 200)

    def test_remove_favorite_status(self):
        data = {'profileId': self.profile.id}
        self.client.post('/profiles/favorites/', data)  # cria o perfil
        response = self.client.post('/profiles/favorites/', data)  # remove o perfil
        self.assertEqual(response.status_code, 200)
        try:
            Favorite.objects.get(user=self.user)
            r = True
        except ObjectDoesNotExist:
            r = False
        self.assertFalse(r)

    def test_create_favorite_status_error(self):
        response = self.client.post('/profiles/favorites/')
        self.assertEqual(response.status_code, 400)
