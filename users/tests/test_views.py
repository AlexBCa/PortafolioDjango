from django.test import Client
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from users.views import Registrer

class TestViewUser(TestCase):

    def setUp(self):
        self.client = Client()
        self.dashboard_url = reverse('dashboard')
        self.register_url = reverse('register')
        self.factory = RequestFactory()

    def test_Dashboard_template(self):

        response = self.client.get(self.dashboard_url)
        self.assertTemplateUsed(response, 'users/dashboard.html')

    def test_Register_get(self):

        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)

    def test_register_post_success(self):
        self.user = User.objects.create_user(username='alex')
        self.client.force_login(self.user)

        params = {'username': 'Teseet1', 'password1': 'pass1', 'password2': 'pass2', 'email': 'test@example.com'}
        response = self.client.post(self.register_url, params)
        
        request = self.factory.post(self.register_url, params)
        
        request.user = AnonymousUser()
        view = Registrer()
        view.setup(request, params)
        

        print(view.get_success_url())
        self.assertEqual(view.get_success_url(), '/users/')