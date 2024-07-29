# testing cookies and sessions
# $ python manage.py test guitar.testCookies

import os
import re
import guitar.models
from guitar import forms
from populate_guitar import populate
from datetime import datetime, timedelta
from django.db import models
from django.test import TestCase
from django.conf import settings
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.forms import fields as django_fields

FAILURE_HEADER = f"\n================ TEST FAILURE ================="
FAILURE_FOOTER = f"\n==============================================="

f"{FAILURE_HEADER} {FAILURE_FOOTER}"

class configurationTests(TestCase):
    def test_middleware_present(self):
        # making sure SessionMiddleware is present
        self.assertTrue('django.contrib.sessions.middleware.SessionMiddleware' in settings.MIDDLEWARE)
    
    def test_session_app_present(self):
        # making sure sessions app is present.
        self.assertTrue('django.contrib.sessions' in settings.INSTALLED_APPS)

class sessionPersistanceTests(TestCase):
    # testing if session data is persisted by counting up number of accesses 
    def test_visits_counter(self):
        for i in range(0, 10):
            response = self.client.get(reverse('guitar:index'))
            session = self.client.session

            self.assertIsNotNone(session['visits'])
            self.assertIsNotNone(session['last_visit'])

            # Get the last visit, and subtract one day.
            # Forces an increment of the counter.
            last_visit = datetime.now() - timedelta(days=1)

            session['last_visit'] = str(last_visit)
            session.save()

            self.assertEquals(session['visits'], i+1)
