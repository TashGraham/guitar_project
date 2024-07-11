from django.contrib import admin
from guitar.models import Category, Part, UserProfile

admin.site.register(Category)
admin.site.register(Part)
admin.site.register(UserProfile)