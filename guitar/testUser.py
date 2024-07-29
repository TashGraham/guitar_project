# test for user and user registration

import os
import tempfile
from guitar import models
from guitar import forms
from django.test import TestCase
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

f"{FAILURE_HEADER} {FAILURE_FOOTER}"

def create_user_object():
    # helper function to create a User object
    user = User.objects.get_or_create(username='testuser',
                                      first_name='Test',
                                      last_name='User',
                                      email='test@test.com')[0]
    user.set_password('test123')
    user.save()

    return user

def create_super_user_object():
    # helper function to create a super user (admin) account
    return User.objects.create_superuser('admin', 'admin@test.com', 'testpassword')

def get_template(path_to_template):
    # helper function to return the string representationof a template file
    f = open(path_to_template, 'r')
    template_str = ""

    for line in f:
        template_str = f"{template_str}{line}"

    f.close()
    return template_str


class TestsThreeSetupTests(TestCase):
    # test to check auth app
    def test_installed_apps(self):
        # checking 'django.contrib.auth' is in correct place
        self.assertTrue('django.contrib.auth' in settings.INSTALLED_APPS)


class TestsThreeRegistrationTests(TestCase):
    # tests on registering a user

    def test_bad_registration_post_response(self):
        # checks the POST response of the registration view
        request = self.client.post(reverse('guitar:register'))
        content = request.content.decode('utf-8')

        self.assertTrue('<ul class="errorlist">' in content)

    def test_good_form_creation(self):
        # testing the functionality of the forms

        user_data = {'username': 'testuser', 'password': 'test123', 'email': 'test@test.com'}
        user_form = forms.UserForm(data=user_data)

        user_profile_data = {'picture': tempfile.NamedTemporaryFile(suffix=".jpg").name}
        user_profile_form = forms.UserProfileForm(data=user_profile_data)
      
        self.assertTrue(user_form.is_valid(), f"{FAILURE_HEADER}The UserForm was not valid after entering the required data.{FAILURE_FOOTER}")
        self.assertTrue(user_profile_form.is_valid(), f"{FAILURE_HEADER}The UserProfileForm was not valid after entering the required data.{FAILURE_FOOTER}")

        user_object = user_form.save()
        user_object.set_password(user_data['password'])
        user_object.save()

        user_profile_object = user_profile_form.save(commit=False)
        user_profile_object.user = user_object
        user_profile_object.save()

        self.assertEqual(len(User.objects.all()), 1, f"{FAILURE_HEADER}Expected to see a User object created, but it didn't appear. Check UserForm implementation{FAILURE_FOOTER}")
        self.assertEqual(len(models.UserProfile.objects.all()), 1, f"{FAILURE_HEADER}Expected to see a UserProfile object created, but it didn't appear. Check UserProfileForm implementation{FAILURE_FOOTER}")
        self.assertTrue(self.client.login(username='testuser', password='test123'), f"{FAILURE_HEADER}****************************Couldn't log the sample user in during the tests. Check UserForm and UserProfileForm implementation{FAILURE_FOOTER}")

    def test_good_registration_post_response(self):
        # checking the POST response of the registration view
        post_data = {'username': 'webformuser', 'password': 'test123', 'email': 'test@test.com', 'picture': tempfile.NamedTemporaryFile(suffix=".jpg").name}
        request = self.client.post(reverse('guitar:register'), post_data)
        content = request.content.decode('utf-8')

        self.assertTrue('<strong>Thank you for registering!</strong>' in content, f"{FAILURE_HEADER}When a successful registration occurs, couldn't find the expected success message. Check register.html.{FAILURE_FOOTER}")
        self.assertTrue(self.client.login(username='webformuser', password='test123'), f"{FAILURE_HEADER}Couldn't log in the user created using the registration form. Check your implementation of the register() view.{FAILURE_FOOTER}")