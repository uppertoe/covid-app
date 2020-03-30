import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
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

'''
Set up the user its attached profile
'''

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('Please enter an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    #Override default User class to allow login with email address
    username = None
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20)
    specialty = models.ManyToManyField(Specialty)

    def __str__(self):
        return self.user.email

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()