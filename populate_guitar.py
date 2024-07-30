import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'guitar_project.settings')
import django
django.setup()
from guitar.models import Category, Part, Review

def populate():
    # single cut, double cut, contour/st, telecaster/tl
    body_parts = [
        {'name':'Single cut',
         'pic':'',
         'views':0,
         'likes':0,
         'sustain':4.5, # 1-5 where 5 is the most sustain
         'warmth':4.5, # 5 is warmest
         'weight':4.5, # 5 is heaviest
         'reviews':[
             {'username':'GuitarPlayer105',
              'title':'single cut review',
              'content':'amazing body, love the warmth',
              'rating':'4.5'}
         ]},
         {'name':'Double cut',
         'pic':'',
         'views':0,
         'likes':0,
         'sustain':4,
         'warmth':4,
         'weight':3,
         'reviews':[]},
         {'name':'Contour',
         'pic':'',
         'views':0,
         'likes':0,
         'sustain':4.5,
         'warmth':3.5,
         'weight':2.5,
         'reviews':[]},
         {'name':'Telecaster',
         'pic':'',
         'views':0,
         'likes':0,
         'sustain':3.5,
         'warmth':2.5,
         'weight':2.5,
         'reviews':[]}  ]
    
    # humbucker, single coil, P90
    pickUp_parts = [
        {'name':'Humbucker',
         'pic':'humbucker.jpg',
         'views':0,
         'likes':0,
         'sustain':-1,
         'warmth':5,
         'weight':-1,
         'reviews':[]},
         {'name':'Single coil',
         'pic':'',
         'views':0,
         'likes':0,
         'sustain':-1,
         'warmth':1.5,
         'weight':-1,
         'reviews':[]},
         {'name':'P90',
         'pic':'',
         'views':0,
         'likes':0,
         'sustain':-1,
         'warmth':3,
         'weight':-1,
         'reviews':[]}   ]
    
    # plastic, bone, tusq, brass
    nut_parts = [
        {'name':'Plastic',
         'pic':'',
         'views':0,
         'likes':0,
         'sustain':1,
         'warmth':2,
         'weight':-1,
         'reviews':[]},
         {'name':'Bone',
         'pic':'',
         'views':0,
         'likes':0,
         'sustain':4,
         'warmth':3,
         'weight':-1,
         'reviews':[]},
         {'name':'Tusq',
         'pic':'',
         'views':0,
         'likes':0,
         'sustain':4,
         'warmth':3,
         'weight':-1,
         'reviews':[]},
         {'name':'Brass',
         'pic':'',
         'views':0,
         'likes':0,
         'sustain':5,
         'warmth':1,
         'weight':-1,
         'reviews':[]},   ]
    
    # tune-o-matic, ashtray, hard tail, tremolo
    bridge_parts = [
        {'name':'Tune-o-matic',
         'pic':'',
         'views':0,
         'likes':0,
         'sustain':4,
         'warmth':-1,
         'weight':-1,
         'reviews':[]},
         {'name':'Ashtray',
         'pic':'',
         'views':0,
         'likes':0,
         'sustain':2,
         'warmth':-1,
         'weight':-1,
         'reviews':[]},
         {'name':'Hardtail',
         'pic':'',
         'views':0,
         'likes':0,
         'sustain':4,
         'warmth':-1,
         'weight':-1,
         'reviews':[]},
         {'name':'Tremolo',
         'pic':'',
         'views':0,
         'likes':0,
         'sustain':3,
         'warmth':-1,
         'weight':-1,
         'reviews':[]}    ]

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
            part = add_part(p['name'], c, p['pic'], views=p['views'], 
                     likes=p['likes'], sustain=p['sustain'], 
                     warmth=p['warmth'], weight=p['weight'])
            for r in p['reviews']:
                add_review(part, r['username'], r['title'], 
                           r['content'], r['rating'])

    for c in Category.objects.all():
        for p in Part.objects.filter(category=c):
            print(f'- {c}: {p}')
            for r in Review.objects.filter(part=p):
                print(f'- {p}: {r}')

def add_part(name, cat, pic, views, likes, sustain, warmth, weight):
    p = Part.objects.get_or_create(name=name, category=cat)[0]
    p.views = views
    p.likes = likes
    p.pic = pic
    p.sustain = sustain
    p.warmth = warmth
    p.weight = weight
    p.save()
    return p
    
def add_cat(name, views=0):
    c = Category.objects.get_or_create(name=name, views=views)[0]
    c.save()
    return c

def add_review(part, username, title, content, rating):
    r = Review.objects.get_or_create(title=title, part=part)[0]
    r.username = username
    r.content = content
    r.rating = rating
    r.save()
    return r

if __name__ == '__main__':
    print('Starting Guitar population script')
    populate()