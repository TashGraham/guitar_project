# tests for forms 
# $ python manage.py test guitar.tests5

import os
import inspect
from guitar.models import Category, Part
from populate_guitar import populate
from django.test import TestCase
from django.urls import reverse, resolve
from django.forms import fields as django_fields

FAILURE_HEADER = f"\n================ TEST FAILURE ================="
FAILURE_FOOTER = f"\n==============================================="

f"{FAILURE_HEADER} {FAILURE_FOOTER}"


class FormClassTests(TestCase):
    # testing that the correct form classes exist and they have the correct fields
    def test_module_exists(self):
        project_path = os.getcwd()
        guitar_app_path = os.path.join(project_path, 'guitar')
        forms_module_path = os.path.join(guitar_app_path, 'forms.py')
        self.assertTrue(os.path.exists(forms_module_path), f"{FAILURE_HEADER}Couldn't find the forms.py module.{FAILURE_FOOTER}")

    def test_part_form(self):
        import guitar.forms 
        self.assertTrue('PartForm' in dir(guitar.forms), f"{FAILURE_HEADER}The class PartForm could not be found in the forms.py module.{FAILURE_FOOTER}")

        from guitar.forms import PartForm
        part_form = PartForm()

        self.assertEqual(type(part_form.__dict__['instance']), Part, f"{FAILURE_HEADER}The PartForm does not link to the Part model.{FAILURE_FOOTER}")

        fields = part_form.fields

        expected_fields = {
            'name': django_fields.CharField,
            'views':django_fields.IntegerField,
            'likes':django_fields.IntegerField,
            'slug':django_fields.CharField,
            'sustain':django_fields.FloatField,
            'warmth':django_fields.FloatField,
            'weight':django_fields.FloatField,
            'pic':django_fields.ImageField,
        }

        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys(), f"{FAILURE_HEADER}The field '{expected_field_name}' was not found in the PartForm implementation.{FAILURE_FOOTER}")
            self.assertEqual(expected_field, type(fields[expected_field_name]), f"{FAILURE_HEADER}The field '{expected_field_name}' in PartForm was not of the expected type '{type(fields[expected_field_name])}'.{FAILURE_FOOTER}")

class OtherTests(TestCase):
    # tests other things eg url mapping, templates
    def url_mapping(self):
        try:
            resolved_url = reverse('guitar:add_part', kwargs={'category_name_slug': 'bodies'})
        except:
            resolved_url = ''
        
        self.assertEqual(resolved_url, '/guitar/bodies/add_part/', f"{FAILURE_HEADER}Check url mapping of add_part.{FAILURE_FOOTER}")

    def add_part_template(self):
        # checks whether a template was used for the add_part() view
        populate()
        response = self.client.get(reverse('guitar:add_part', kwargs={'category_name_slug': 'bodies'}))
        self.assertTemplateUsed(response, 'guitar/add_part.html', f"{FAILURE_HEADER}The add_part.html is not used for the add_part() view.{FAILURE_FOOTER}")

    def form_response_test(self):
        populate()
        response = self.client.get(reverse('guitar:add_part', kwargs={'category_name_slug': 'bodies'}))
        context = response.context
        content = response.content.decode()

        self.assertTrue('<form' in content, f"{FAILURE_HEADER}Couldn't find a <form> element in the response for adding a part.{FAILURE_FOOTER}")
        self.assertTrue('action="/guitar/bodies/add_part/"' in content, f"{FAILURE_HEADER}Couldn't find he correct action URL for adding a part in add_part.html template.{FAILURE_FOOTER}")

    def bad_cat_test(self):
        # test for response for trying to add part to non-existing category
        response = self.client.get(reverse('guitar:add_part', kwargs={'category_name_slug': 'fake_cat'}))

        self.assertEquals(response.status_code, 302, f"{FAILURE_HEADER}Weren't redirected when trying to add a part to a non-existent category.{FAILURE_FOOTER}")
        self.assertEquals(response.url, '/guitar/', f"{FAILURE_HEADER}Weren't redirected to homepage when trying to add a part to a non-existent category.{FAILURE_FOOTER}")

    def part_functionality_test(self):
        populate()
        response = self.client.post(reverse('guitar:add_part', kwargs={'category_name_slug': 'bodies'}),
                                            {'name': 'stratocaster', 'views':0, 'likes':0,
                                             'sustain':4.0, 'warmth':4.0, 'weight':3.5})
        
        body_parts = Part.objects.filter(name='stratocaster')
        self.assertEqual(len(body_parts), 1, f"{FAILURE_HEADER}Part object wasn't created when it should've been - check add_part() view.{FAILURE_FOOTER}")

        part = body_parts[0]
        self.assertEqual(part.sustain, 4.0, f"{FAILURE_HEADER}PartForm doesn't seem to be working correctly{FAILURE_FOOTER}")
        self.assertEqual(part.name, 'stratocaster', f"{FAILURE_HEADER}Check PartForm implementation{FAILURE_FOOTER}")
