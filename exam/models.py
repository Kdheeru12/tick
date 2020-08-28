from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.fields import (
    DateField, DateTimeField, DurationField, Field, IntegerField, TimeField,
)
from django.utils.text import slugify
from django import forms
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import pre_save
# Create your models here.
class Video(models.Model):
    url = models.CharField(max_length=800)
class Profile(models.Model):
    user = models.EmailField(unique=True)
    firstname = models.CharField(max_length=50,null=True,blank=True)
    lastname = models.CharField(max_length=50,null=True,blank=True)
    Class = models.CharField(max_length=300,null=True,blank=True)
    Mobile = models.IntegerField(blank=True,null=True)
    gender = models.CharField(max_length=300,blank=True,null=True)
    date = models.DateField(blank=True,null=True)
    photo = models.ImageField(blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    state = models.CharField(max_length=60,null=True,blank=True)
    city = models.CharField(max_length=80,null=True,blank=True)
    pincode = models.IntegerField(blank=True,null=True)
    age = models.IntegerField(blank=True,null=True)
    intrests = models.TextField(blank=True,null=True)
    lat = models.FloatField(blank=True,null=True)
    lon = models.FloatField(blank=True,null=True)
    def __str__(self):
        return self.firstname
class Users(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.IntegerField()
    gender = models.CharField(max_length=100)
    age = models.IntegerField()
    intrests = models.TextField()
    lat = models.FloatField()
    lon = models.FloatField()
    location = models.TextField()
class Challenge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)    
    title = models.CharField(max_length=800)
    reward = models.IntegerField()
    about = models.TextField(blank=True,null=True)
    start_date = models.DateField()
    image = models.ImageField()
    ip = models.GenericIPAddressField()
    lat = models.FloatField()
    lon = models.FloatField()
    location = models.TextField()
    end_date = models.DateField()
    slug = models.SlugField(unique=True)
    def __str__(self):
        return self.slug
    class Meta:
        db_table="Challenge"
def create_slug(instance,new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Challenge.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug,qs.first().id)
        return create_slug(instance,new_slug=new_slug)
    return slug 
def pre_save_post_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
pre_save.connect(pre_save_post_receiver,sender=Challenge)
class Post(models.Model):
    challenge = models.ForeignKey(Challenge,default=1,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
    slug1 = models.SlugField(unique=True)
    title = models.CharField(max_length=800)
    video = models.FileField()
    upload_date = models.DateField(auto_now=True)
    ip = models.GenericIPAddressField()
    lat = models.FloatField()
    lon = models.FloatField()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="likes", blank=True)    
    is_liked = models.BooleanField(default=False)
    likes_count = models.IntegerField(blank=True,null=True)
    def __str__(self):
        return self.slug1
    def total_likes(self):
        return self.likes.count() 
