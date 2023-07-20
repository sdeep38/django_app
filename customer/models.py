from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

# Create your models here.
class Contact(models.Model):
    email = models.EmailField(max_length=254)
    name = models.CharField(max_length=100)
    phn = models.CharField(max_length=10)
    desc = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name

BLOODGRP_CHOICES = (
    ("A+", "A+"),
    ("B+", "B+"),
    ("AB+", "AB+"),
    ("O+", "O+"),
    ("A-", "A-"),
    ("B-", "B-"),
    ("AB-", "AB-"),
    ("O-", "O-")
)

GENDER_CHOICES = (
    ("Male", "Male"),
    ("Female", "Female")
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    blood_grp = models.CharField(max_length=5, choices=BLOODGRP_CHOICES, default="A+")
    gender = models.CharField(max_length=8, choices=GENDER_CHOICES, default="Male")
    mobile = models.CharField(max_length=10, null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
    
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    
class Notice(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True, default="Untitled Notice")
    body = models.TextField()
    new_tag = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title
    

