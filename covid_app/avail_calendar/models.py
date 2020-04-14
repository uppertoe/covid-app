from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone
from accounts.models import UserLogin, UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, date, timedelta
from django.core.exceptions import ValidationError

# Create your models here.
class CalendarDay(models.Model):
    date = models.DateField(_("Calendar Date"), auto_now=False, auto_now_add=False, unique=True)

    def __str__(self):
        return f'{self.date}'

class Shift(models.Model):
    clinician = models.ForeignKey(UserLogin, on_delete=models.CASCADE)
    date = models.ForeignKey(CalendarDay, on_delete=models.CASCADE)
    start_time = models.TimeField(_("Shift start"), auto_now=False, auto_now_add=False)
    end_time = models.TimeField(_("Shift end"), auto_now=False, auto_now_add=False)

    def hours_between(self):
        delta = self.end_time - self.start_time
        return int(delta.seconds / 3600)

    def is_available(self):
        shift_date = self.date
        start = datetime.combine(shift_date, self.start_time)
        end = datetime.combine(shift_date, self.end_time)
        return start < timezone.now() and end > timezone.now()

    def merge_shifts_in_database(self):
        #Set up lists to hold database objects
        current_clinician_shifts = Shift.objects.filter(clinician = self.clinician, date=self.date)
        current_database_state =[]
        collated_shift_times = []
        
        #Make 2 copies of a nested list from the query; maintain the instance at index[2]
        for shift in current_clinician_shifts:
            collated_shift_times.append([shift.start_time,shift.end_time,shift])
            current_database_state.append([shift.start_time,shift.end_time,shift])
        
        #Add the current, unsaved, instance
        collated_shift_times.append([self.start_time,self.end_time, self])
        
        #Sort by the value at index [0] i.e. the lower bound
        sorted_by_lower_bound_list = sorted(collated_shift_times, key=lambda date: date[0])      
        
        #A list of all objects that should be in the database
        merged = self.merge_list_of_time_periods(sorted_by_lower_bound_list)
    
        #Each record should only be deleted once
        records_to_delete = set()
        
        #If a saved record is not in merged, it has been changed and should be deleted
        for record in current_database_state:
            if record not in merged:
                records_to_delete.add(record[2])
        
        #Check for differences between updated and old records
        for record in merged:
            if record not in current_database_state:
                #Therfore has been changed; only one record will be modified per save (the rest being deleted)
                self.start_time = record[0]
                self.end_time = record[1]
                #Replace the old record with the current instance
                if record[2] != self:
                    records_to_delete.add(record[2])
                    print('A new record replaced an old record')
        
        #Only old instances should reach here
        for record in records_to_delete:
            record.delete()
            print(f'A record was deleted: {record}')

    def merge_list_of_time_periods(self, sorted_by_lower_bound_list):
        merged = []
        for higher in sorted_by_lower_bound_list:
            #Add the first values to merged for comparison
            if not merged:
                merged.append(higher)
            else:
                #Sorting means lower[0] will be < higher[0]
                lower = merged[-1]
                #Is there overlap?
                if lower[1] >= higher[0]:
                    #Find the highest upper bound value
                    upper_bound = max(lower[1], higher[1])
                    #Lower is modified to have the upper bound value; either way higher is disposed of
                    merged[-1][1] = upper_bound
                #Otherwise, there is no overlap and higher is added to the merged list
                else:
                    merged.append(higher)
        return merged

    def save(self, *args, **kwargs):
        #Check that start is before the end
        if self.start_time > self.end_time:
            raise ValidationError(_("The of a shift must precede the end of a shift"))

        #Query the database for other shifts and merge times where necessary
        self.merge_shifts_in_database()

        super(Shift, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.start_time} to {self.end_time} on {self.date}'