import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class Availability(models.Model):
    avail_start = models.DateTimeField('Availability start time', null=True)
    avail_end = models.DateTimeField('Availability end time', null=True)

    class Meta:
        verbose_name_plural = "Availabilities"

    def hours_between(self):
        delta = self.avail_end - self.avail_start
        return int(delta.seconds / 3600)

    def __str__(self):
        return f'({self.hours_between()} hour(s); from {self.avail_start} to {self.avail_end})'

class Specialty(models.Model):
    specialty_name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Specialties"

    def __str__(self):
        return self.specialty_name
    
class State(models.Model):
    state_name = models.CharField(max_length=200)

    def __str__(self):
        return self.state_name

class User(AbstractUser):
    #Included to allow extension later
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20)
    specialty = models.ManyToManyField(Specialty)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()