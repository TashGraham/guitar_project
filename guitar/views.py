from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect
from guitar.models import Category, Part, User
from guitar.forms import UserForm, UserProfileForm

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


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # saving the user's form data to the database
            user = user_form.save()
            # now hashing the password 
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            # if user hes provided a profile picture then we need to get it from the 
            # input form and put it in the UserProfile model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            # saving the UserProfile model instance
            profile.save()
            # registration successful
            registered = True
        else:
            # printing problems to the terminal
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,'guitar/register.html',
                  context = {'user_form': user_form,
                            'profile_form': profile_form,
                            'registered': registered})


def login(request):
    context_dict = {'error_message': None}
    # if request is an HTTP POST, try to pull relevant info
    if request.method == 'POST':
        # get username and password provided by user
        username = request.POST.get('username')
        password = request.POST.get('password')
        # if username/password combination is valid then a user object is returned
        user = authenticate(username=username, password=password)
        # if we have a user then the credentials were correct
        if user:
            # now checking if the account is active
            if user.is_active:
                # user can now be logged in and returned to homepage
                auth_login(request, user)
                return redirect(reverse('guitar:index'))
            else:
                # if account is inactive then no logging in
                return HttpResponse("Your account is disabled")
        else:
            # invalid credentials - no logging in
            # checking which part is invalid for error message
            if User.objects.filter(username=username).exists():
                context_dict['error_message'] = 'Your password is incorrect.'
            else:
                context_dict['error_message'] = 'Your username is incorrect.'

    # if user has not been logged in successfully then return them to login page
    return render(request, 'guitar/login.html', context_dict)

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('guitar:index'))