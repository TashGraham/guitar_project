from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# bodies, necks, strings etc are all categories
# a humbucker is a part or a sub category which is from category pick-up
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)
    views = models.IntegerField(default=0)
    # will add more aspects later

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Part(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    pic = models.ImageField(upload_to='part_images', blank=True)
    slug = models.SlugField(unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    sustain = models.FloatField(default=0)
    warmth = models.FloatField(default=0)
    weight = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Part, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional attributes currently just an image 
    # blank=True as picture is not necessary
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username