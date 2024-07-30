from datetime import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from guitar.models import Category, Part, User, UserProfile
from guitar.forms import UserForm, UserProfileForm, PartForm, ReviewForm

def index(request):
    # getting a list of all the categories from the database
    category_list = Category.objects.all()
    part_list = Part.objects.all()
    # making a context dicct to pass onto template
    context_dict = {}
    context_dict['categories'] = category_list
    context_dict['parts'] = part_list
    # rendering the response early so can add cookie info
    response = render(request, 'guitar/index.html', context=context_dict)
    visitor_cookie_handler(request)
    return response

def about(request):
    visitor_cookie_handler(request)
    # about page contains link back to index
    return HttpResponse("This is the about page. To return to index page please click <a href='/guitar/'>here</a>")

def show_category(request, category_name_slug):
    visitor_cookie_handler(request)
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


def show_part(request, category_name_slug, part_name_slug):
    visitor_cookie_handler(request)
    context_dict = {}

    # trying to get the category and part objects
    try:
        category = Category.objects.get(slug=category_name_slug)
        part = Part.objects.get(slug = part_name_slug)
        context_dict['category'] = category
        context_dict['part'] = part
    except (Category.DoesNotExist, Part.DoesNotExist):
        context_dict['category'] = None
        context_dict['part'] = None
    return render(request, 'guitar/part.html', context=context_dict)

# write review will also be displayed on part.html 
def write_review(request, category_name_slug, part_name_slug):
    visitor_cookie_handler(request)
    context_dict = {}

    category = get_object_or_404(Category, slug=category_name_slug)
    part = get_object_or_404(Part, slug=part_name_slug)

    context_dict['category'] = category
    context_dict['part'] = part

    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.part = part
            review.save()
    else:
        print(form.errors)
    context_dict['form'] = form
    return render(request, 'guitar/part.html', context=context_dict)

@login_required #unregistered people cannot add a part
def add_part(request, category_name_slug):
    visitor_cookie_handler(request)
    # finding category 
    category = get_object_or_404(Category, slug=category_name_slug)

    # if category not found then cannot add part
    if category is None:
        return redirect('/guitar/')
    
    form = PartForm()

    # chekcing the type of request
    if request.method == 'POST':
        form = PartForm(request.POST)

        # checking if form is valid
        if form.is_valid():
            if category:
                # if part and category are valid then saving
                part = form.save(commit=False)
                part.category = category
                part.save()
                return redirect(reverse('guitar:show_category',
                                        kwargs={'category_name_slug':category_name_slug}))
        else:
            # if form had errors then printing those errors
            print(form.errors)
    context_dict = {'form': form, 'category':category}
    return render(request, 'guitar/add_part.html', context=context_dict)

def register(request):
    visitor_cookie_handler(request)
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
    visitor_cookie_handler(request)
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
def profile(request):
    visitor_cookie_handler(request)
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
    context_dict = {
        'user': request.user,
        'user_profile': user_profile
    }
    return render(request, 'guitar/profile.html', context_dict)

@login_required
def user_logout(request):
    visitor_cookie_handler(request)
    logout(request)
    return redirect(reverse('guitar:index'))

# helper function
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

# cookie helper function
def visitor_cookie_handler(request):
    # getting number of visits to site
    # is the cookie doesn't exist then the default (1) is used
    visits = int(request.COOKIES.get('visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    # if it's been more than one day since last visit
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # update last visit cookie now that count has been updated
        request.session['last_visit'] = str(datetime.now())
    else:
        # set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
    # updating the visits cookie
    request.session['visits'] = visits