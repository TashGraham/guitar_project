# tests for models and database

import os
import warnings
import importlib
from guitar.models import Category, Part
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class testsTwoDatabase(TestCase):
    # tests for database
    def setUp(self):
        pass


    # making sure gitignore includes the database
    def gitignoreDatabase(self, path):
        f = open(path, 'r')

        for line in f:
            line = line.strip()
            if line.startswith('db.sqlite3'):
                # if we find 'db.sqlite3' then gitignore does include database so test passes
                return True
            
        f.close()
        return False
    

    # checking the settings module contains a DATABASES variable
    def databasesInSettings(self):
        self.assertTrue(settings.DATABASES, f"{FAILURE_HEADER}Project settings module must have a DATABASES variable.{FAILURE_FOOTER}")
        self.assertTrue('default' in settings.DATABASES, f"{FAILURE_HEADER}Must have a 'default' database configuration in the DATABSES configuration variable.{FAILURE_FOOTER}")


    # tests for gitignore, databse and git repository (other gitignore test does not test for git)
    def moreGitignoreDatabase(self):

        git_base_dir = os.popen('git rev-parse --show-toplevel').read().strip()

        if git_base_dir.startswith('fatal'):
            warnings.warn("You don't appear to be using a Git repository for your codebase.")
        else:
            gitignore_path = os.path.join(git_base_dir, '.gitignore')

            if os.path.exists(gitignore_path):
                self.assertTrue(self.gitignoreDatabase(gitignore_path), f"{FAILURE_HEADER}The .gitignore file does not include 'db.sqlite3'.{FAILURE_FOOTER}")
            else:
                warnings.warn("You don't appear to have a .gitignore file in place in your repository.")



class TestsTwoModel(TestCase):
    # tests for the Models - set up and attributes
    def setUp(self):
        category_bd = Category.objects.get_or_create(name='Bodies', views=12)
        Category.objects.get_or_create(name='Bridges', views=8)
        #url, views, likes, sustain, warmth, weight
        Part.objects.get_or_create(category=category_bd[0],name='Telecaster',
                                   url='https://warmoth.com/guitar-bodies/telecaster', 
                                   views=4,likes=3,sustain=3.5,warmth=2.5,weight=2.5)

    def testCategoryModel(self):
        # testing the category model with the attributes set above
        category_bd = Category.objects.get(name='Bodies')
        self.assertEqual(category_bd.views, 12, f"{FAILURE_HEADER}Tests on the Category model failed.{FAILURE_FOOTER}")
        
        category_br = Category.objects.get(name='Bridges')
        self.assertEqual(category_br.views, 8, f"{FAILURE_HEADER}Tests on the Category model failed.{FAILURE_FOOTER}")

    def testPartModel(self):
        # testing the part model with the attributes set above
        category_bd = Category.objects.get(name='Bodies')
        part = Part.objects.get(name='Telecaster')
        self.assertEqual(part.url, 'https://warmoth.com/guitar-bodies/telecaster', f"{FAILURE_HEADER}Tests on the Page model failed.{FAILURE_FOOTER}")
        self.assertEqual(part.views, 4, f"{FAILURE_HEADER}Tests on the Page model failed.{FAILURE_FOOTER}")
        self.assertEqual(part.likes, 3, f"{FAILURE_HEADER}Tests on the Page model failed.{FAILURE_FOOTER}")
        self.assertEqual(part.sustain, 3.5, f"{FAILURE_HEADER}Tests on the Page model failed.{FAILURE_FOOTER}")
        self.assertEqual(part.warmth, 2.5, f"{FAILURE_HEADER}Tests on the Page model failed.{FAILURE_FOOTER}")
        self.assertEqual(part.weight, 2.5, f"{FAILURE_HEADER}Tests on the Page model failed.{FAILURE_FOOTER}")
        self.assertEqual(part.category, category_bd, f"{FAILURE_HEADER}Tests on the Page model failed.{FAILURE_FOOTER}")

    def testStrMethod(self):
        # test to check correct __str__() method been implemented
        category_bd = Category.objects.get(name='Bodies')
        part = Part.objects.get(name='Telecaster')

        self.assertEqual(str(category_bd), 'Bodies', f"{FAILURE_HEADER}The __str__() method in the Category class has not been implemented correctly.{FAILURE_FOOTER}")
        self.assertEqual(str(part), 'Telecaster', f"{FAILURE_HEADER}The __str__() method in the Part class has not been implemented correctly.{FAILURE_FOOTER}")



class TestsTwoPopulationScript(TestCase):
    # testing whether the population script puts the expected data into a test database
    def setUp(self):
        # importing and running the population script, calling the populate() method
        try:
            import popluate_guitar
        except ImportError:
            raise ImportError(f"{FAILURE_HEADER}populate_guitar could not be imported.{FAILURE_FOOTER}")
        
        if 'populate' not in dir(popluate_guitar):
            raise NameError(f"{FAILURE_HEADER}The populate() function does not exist in the populate_guitar module.{FAILURE_FOOTER}")
        
        # now calling the population script
        popluate_guitar.populate()

    def testCategories(self):
        # there should be four categories created: Bodies, Pick-Ups, Nuts, Bridges
        categories = Category.objects.filter()
        categories_len = len(categories)
        categories_strs = map(str, categories)

        self.assertEqual(categories_len, 4, f"{FAILURE_HEADER}Expecting 4 categories to be created from the populate_guitar module; found {categories_len}.{FAILURE_FOOTER}")
        self.assertTrue('Bodies' in categories_strs, f"{FAILURE_HEADER}The category 'Bodies' was expected but not created by poulation_guitar.{FAILURE_FOOTER}")
        self.assertTrue('Pick-Ups' in categories_strs, f"{FAILURE_HEADER}The category 'Pick-Ups' was expected but not created by poulation_guitar.{FAILURE_FOOTER}")
        self.assertTrue('Nuts' in categories_strs, f"{FAILURE_HEADER}The category 'Nuts' was expected but not created by poulation_guitar.{FAILURE_FOOTER}")
        self.assertTrue('Bridges' in categories_strs, f"{FAILURE_HEADER}The category 'Bridges' was expected but not created by poulation_guitar.{FAILURE_FOOTER}")

    def testParts(self):
        # test to check whether each part for each category exists
        # calls a helper function: check_category_parts()

        details = {'Bodies': ['single cut', 'double cut', 'contour', 'telecaster'],
            'Pick-Ups': ['humbucker', 'single coil', 'P90'],
            'Nuts': ['plastic', 'bone', 'tusq', 'brass'],
            'Bridges': ['tune-o-matic', 'ashtray', 'hard tail', 'tremolo'],
            }
        
        for category in details:
            part_names = details[category]
            self.check_category_parts(category, part_names)


    def check_category_parts(self, category, part_names):
        # checks the database for parts for a given category
        category = Category.objects.get(name=category)
        parts = Part.objects.filter(category=category)
        parts_len = len(parts)
        # parts_names_len = len(part_names)

        self.assertEqual(parts_len, len(part_names), f"{FAILURE_HEADER}Expected {len(part_names)} parts in the {category} category. {parts_len} found.{FAILURE_FOOTER}")

        for name in part_names:
            try:
                part = Part.objects.get(name=name)
            except Part.DoesNotExist:
                raise ValueError(f"{FAILURE_HEADER}The part '{name}' belonging to category '{category}' was not found in the database produced by populate_guitar.{FAILURE_FOOTER}")
            
            self.assertEqual(part.category, category)



