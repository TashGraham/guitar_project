import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'guitar_project.settings')
import django
django.setup()
from guitar.models import Category, Part

def populate():
    # single cut, double cut, contour/st, telecaster/tl
    body_parts = [
        {'name':'single cut',
         'url':'',
         'views':0,
         'likes':0,
         'sustain':4.5, # 1-5 where 5 is the most sustain
         'warmth':4.5, # 5 is warmest
         'weight':4.5}, # 5 is heaviest
         {'name':'double cut',
         'url':'',
         'views':0,
         'likes':0,
         'sustain':4,
         'warmth':4,
         'weight':3},
         {'name':'contour',
         'url':'',
         'views':0,
         'likes':0,
         'sustain':4.5,
         'warmth':3.5,
         'weight':2.5},
         {'name':'telecaster',
         'url':'',
         'views':0,
         'likes':0,
         'sustain':3.5,
         'warmth':2.5,
         'weight':2.5}  ]
    
    # humbucker, single coil, P90
    pickUp_parts = [
        {'name':'humbucker',
         'url':'',
         'views':0,
         'likes':0,
         'sustain':-1,
         'warmth':5,
         'weight':-1},
         {'name':'single coil',
         'url':'',
         'views':0,
         'likes':0,
         'sustain':-1,
         'warmth':1.5,
         'weight':-1},
         {'name':'P90',
         'url':'',
         'views':0,
         'likes':0,
         'sustain':-1,
         'warmth':3,
         'weight':-1}   ]
    
    # plastic, bone, tusq, brass
    nut_parts = [
        {'name':'plastic',
         'url':'',
         'views':0,
         'likes':0,
         'sustain':1,
         'warmth':2,
         'weight':-1},
         {'name':'bone',
         'url':'',
         'views':0,
         'likes':0,
         'sustain':4,
         'warmth':3,
         'weight':-1},
         {'name':'tusq',
         'url':'',
         'views':0,
         'likes':0,
         'sustain':4,
         'warmth':3,
         'weight':-1},
         {'name':'brass',
         'url':'',
         'views':0,
         'likes':0,
         'sustain':5,
         'warmth':1,
         'weight':-1},   ]
    
    # tune-o-matic, ashtray, hard tail, tremolo
    bridge_parts = [
        {'name':'tune-o-matic',
         'url':'',
         'views':0,
         'likes':0,
         'sustain':4,
         'warmth':-1,
         'weight':-1},
         {'name':'ashtray',
         'url':'',
         'views':0,
         'likes':0,
         'sustain':2,
         'warmth':-1,
         'weight':-1},
         {'name':'hardtail',
         'url':'',
         'views':0,
         'likes':0,
         'sustain':4,
         'warmth':-1,
         'weight':-1},
         {'name':'tremolo',
         'url':'',
         'views':0,
         'likes':0,
         'sustain':3,
         'warmth':-1,
         'weight':-1}    ]

    # categories hold the different parts 
    # might add other sections to the categories later
    cats = {'Bodies': {'parts':body_parts, 'views':23},
            'Pick-Ups': {'parts':pickUp_parts, 'views':23},
            'Nuts': {'parts':nut_parts, 'views':23},
            'Bridges': {'parts':bridge_parts, 'views':23},
            }
    
    for cat, cat_data in cats.items():
        c = add_cat(cat, views=cat_data['views'])
        for p in cat_data['parts']:
            add_part(p['name'], c, p['url'], views=p['views'], likes=p['likes'], sustain=p['sustain'], warmth=p['warmth'], weight=p['weight'])

    for c in Category.objects.all():
        for p in Part.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_part(name, cat, url, views, likes, sustain, warmth, weight):
    p = Part.objects.get_or_create(name=name, category=cat)[0]
    p.views = views
    p.likes = likes
    p.url = url
    p.sustain = sustain
    p.warmth = warmth
    p.weight = weight
    p.save()
    return p
    
def add_cat(name, views=0):
    c = Category.objects.get_or_create(name=name, views=views)[0]
    c.save()
    return c

if __name__ == '__main__':
    print('Starting Guitar population script')
    populate()