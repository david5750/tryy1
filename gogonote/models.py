from django.db import models

# Create your models here.

class userentry(models.Model):
    Email = models.EmailField(max_length=200,unique=True,null=True)
    Password = models.CharField(max_length=200)
    random1 = models.CharField(max_length=200)
    forget_password_token = models.CharField(max_length=200)
    signup_date = models.DateField(max_length=200)
    success = models.BooleanField(default=False)
    register_token = models.CharField(max_length=200)

class foldername(models.Model):
    Email = models.EmailField(max_length=200)
    foldername = models.CharField(max_length=255)
    random1 = models.CharField(max_length=200)
    random2 = models.CharField(max_length=200,unique=True,null=True)

class notenames(models.Model):
    Email = models.EmailField(max_length=200)
    title = models.CharField(max_length=255)
    note = models.CharField(max_length=555)
    random1 = models.CharField(max_length=200)
    random2 = models.CharField(max_length=200)
    random3 = models.CharField(max_length=200,unique=True,null=True)
