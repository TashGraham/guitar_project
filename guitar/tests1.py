import os
import importlib
from django.urls import reverse
from django.test import TestCase
from django.conf import settings

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"


class TestsOneStructure(TestCase):

    def setUp(self):
        # set up for tests
        self.project_base_dir = os.getcwd()
        self.guitar_app_dir = os.path.join(self.project_base_dir, 'guitar')

    def test_app_created(self):
        # tests that the app has actually been created
        directory_exists = os.path.isdir(self.guitar_app_dir)
        is_python_package = os.path.isfile(os.path.join(self.guitar_app_dir, '__init__.py'))
        views_module_exists = os.path.isfile(os.path.join(self.guitar_app_dir, 'views.py'))

        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The app directory does not exist{FAILURE_FOOTER}")
        self.assertTrue(is_python_package, f"{FAILURE_HEADER}The directory is missing files{FAILURE_FOOTER}")
        self.assertTrue(views_module_exists, f"{FAILURE_HEADER}The directory is missing files{FAILURE_FOOTER}")
    
    def url_module(self):
        # tests that there is a separate url module for the app
        module_exists = os.path.isfile(os.path.join(self.guitar_app_dir, 'urls.py'))
        self.assertTrue(module_exists, f"{FAILURE_HEADER}The guitar app's urls.py module is missing. Must have two urls.py modules.{FAILURE_FOOTER}")


class TestsOneIndexPage(TestCase):

    def setUp(self):
        self.views_module = importlib.import_module('guitar.views')
        self.views_module_listing = dir(self.views_module)
        
        self.project_urls_module = importlib.import_module('guitar_project.urls')

    def test_view_exists(self):
        # testing index view exists
        name_exists = 'index' in self.views_module_listing
        is_callable = callable(self.views_module.index)
        
        self.assertTrue(name_exists, f"{FAILURE_HEADER}The index() view for guitar does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}The index() view doesn't seem to be a function{FAILURE_FOOTER}")
    
    def test_mappings_exists(self):
        # tests the url mapping is correct
        index_mapping_exists = False
        
        # This is overridden. We need to manually check it exists.
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'index':
                    index_mapping_exists = True
        
        self.assertTrue(index_mapping_exists, f"{FAILURE_HEADER}The index URL mapping could not be found. Check your PROJECT'S urls.py module.{FAILURE_FOOTER}")
        self.assertEquals(reverse('guitar:index'), '/guitar/', f"{FAILURE_HEADER}The index URL lookup failed. Guitar's urls.py module's missing something in there.{FAILURE_FOOTER}")
    

class TestsOneAboutPage(TestCase):

    def setUp(self):
        self.views_module = importlib.import_module('guitar.views')
        self.views_module_listing = dir(self.views_module)
    
    def test_view_exists(self):
        # testing about view exists
        name_exists = 'about' in self.views_module_listing
        is_callable = callable(self.views_module.about)
        
        self.assertTrue(name_exists, f"{FAILURE_HEADER}The sbout() view for guitar does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}The about() view doesn't seem to be a function{FAILURE_FOOTER}")
    
    def test_mapping_exists(self):
        # tests url mapping
        self.assertEquals(reverse('guitar:about'), '/guitar/about/', f"{FAILURE_HEADER}Your about URL mapping is either incorrect.{FAILURE_FOOTER}")
    