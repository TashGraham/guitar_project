# tests for login/out
# $ python manage.py test guitar.tests4

from populate_guitar import populate
from django.test import TestCase
from django.conf import settings
from django.urls import reverse, resolve
from django.contrib.auth.models import User

FAILURE_HEADER = f"\n================ TEST FAILURE ================="
FAILURE_FOOTER = f"\n==============================================="

f"{FAILURE_HEADER} {FAILURE_FOOTER}"

# hepler function for tests
def create_user_object():
    user = User.objects.get_or_create(username='testuser',
                                      first_name='Test',
                                      last_name='User',
                                      email='test@test.com')

class LoginTests(TestCase):
    # checking the login functionality
    def test_login_url_correct(self):
        url = ''
        try:
            url = reverse('guitar:login')
        except:
            pass
        self.assertEqual(url, '/guitar/login/', f"{FAILURE_HEADER}Check login URL mapping.{FAILURE_FOOTER}")

    def test_login_functionality(self):
        # user should be able to login, and then should be redirected to index page
        user_object = create_user_object()
        response = self.client.post(reverse('guitar:login'), {'username': 'testuser', 'password': 'testabc123'})
        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}Attempted to log a user in with an ID of {user_object.id}, but instead logged a user in with an ID of {self.client.session['_auth_user_id']}. Check login() view.{FAILURE_FOOTER}")
        except KeyError:
            self.assertTrue(False, f"{FAILURE_HEADER}The login() view didn't log the user in. Check the login() view implementation.{FAILURE_FOOTER}")
        
        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}Logging in was successful but should have been redirected; we got a status code of {response.status_code} instead. Check login() view implementation.{FAILURE_FOOTER}")
        self.assertEqual(response.url, reverse('guitar:index'), f"{FAILURE_HEADER}Not redirected to the homepage after logging in.{FAILURE_FOOTER}")

class LougoutTests(TestCase):
    # checking logout functionality
    def test_bad_request(self):
        # attempts to logout a user who is not logged in
        response = self.client.get(reverse('guitar:logout'))
        self.assertTrue(response.status_code, 302)

    def test_good_request(self):
        # attempts to log in a user who is logged in
        user_object = create_user_object()
        self.client.login(username='testuser', password='testabs123')

        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}Attempted to log a user in with an ID of {user_object.id}, but instead logged a user in with an ID of {self.client.session['_auth_user_id']}. Check your login() view. This happened when testing logout functionality.{FAILURE_FOOTER}")
        except KeyError:
            self.assertTrue(False, f"{FAILURE_HEADER}When attempting to log a user in, it failed. Check your login() view.{FAILURE_FOOTER}")

        # now logging the user out which should cause a redirect to the homepage
        response = self.client.get(reverse('guitar:logout'))
        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}Logging out a user should cause a redirect, but this failed to happen.{FAILURE_FOOTER}")
        self.assertEqual(response.url, reverse('guitar:index'), f"{FAILURE_HEADER}Logging out a user should redirect them to the homepage. This did not happen; check logout() view.{FAILURE_FOOTER}")
        self.assertTrue('_auth_user_id' not in self.client.session, f"{FAILURE_HEADER}Logging out with the logout() view didn't actually log the user out! Check logout() view.{FAILURE_FOOTER}")
