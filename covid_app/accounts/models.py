from django.db import models
import datetime

class Availability(models.Model):
    avail_start = models.DateTimeField('Availability start time', null=True)
    avail_end = models.DateTimeField('Availability end time', null=True)

    def hours_between(self):
        delta = self.avail_end - self.avail_start
        return int(delta.seconds / 3600)

    def __str__(self):
        return f'({self.hours_between()} hour(s); from {self.avail_start} to {self.avail_end})'

class Specialty(models.Model):
    specialty_name = models.CharField(max_length=200)

    def __str__(self):
        return self.specialty_name
    
class State(models.Model):
    state_name = models.CharField(max_length=200)

    def __str__(self):
        return self.state_name

class Clinician(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    mobile = models.CharField(max_length=20)
    specialty = models.ManyToManyField(Specialty)
    is_doctor = models.BooleanField
    ahpra_number = models.CharField(max_length = 20)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    availability = models.ManyToManyField(Availability)

    def __str__(self):
        return f'({self.firstname} {self.lastname})'