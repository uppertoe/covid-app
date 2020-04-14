from django.test import TestCase
from . import models

# Create your tests here.
class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username = 'test', password='test')
        login = self.client.login(username='test', password='test')