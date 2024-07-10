from django.shortcuts import render
from django.http import HttpResponse
from guitar.models import Category, Part

def index(request):
    # getting a list of all the categories from the database
    category_list = Category.objects.all()
    part_list = Part.objects.all()
    # making a context dicct to pass onto template
    context_dict = {}
    context_dict['categories'] = category_list
    context_dict['parts'] = part_list
    # rendering the response
    return render(request, 'guitar/index.html', context=context_dict)

def about(request):
    # about page contains link back to index
    return HttpResponse("This is the about page. To return to index page please click <a href='/guitar/'>here</a>")

def show_category(request, category_name_slug):
    # context dict to pass to the template rendering engine
    context_dict = {}

    # making sure category exists first
    try:
        category = Category.objects.get(slug=category_name_slug)
        # now getting parts in this category
        parts = Part.objects.filter(category=category)
        # adding parts and category to context dict
        context_dict['parts'] = parts
        context_dict['category'] = category
    except Category.DoesNotExist:
        # if we cannot find category then template will display appropriate message
        context_dict['category'] = None
        context_dict['parts'] = None

    return render(request, 'guitar/category.html', context=context_dict)