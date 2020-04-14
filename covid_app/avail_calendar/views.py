from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from .forms import ShiftForm
from .models import CalendarDay

# Create your views here.
class CalendarPage(TemplateView):
    template_name = 'avail_calendar/calendar.html'

class ShiftRequestView(LoginRequiredMixin, View):
    form_class = ShiftForm
    initial = {'key' : 'value'}
    template_name = 'avail_calendar/index.html'

    #Override this with the shift date in the request
    shift_date = ''

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_shift = form.save(commit=False)
            new_shift.clinician = request.user
            #Sets the shift date to today for testing
            shift_date = self.shift_date
            if shift_date == '':
                shift_date = CalendarDay.objects.get_or_create(date = timezone.now().date())[0]
            new_shift.date = shift_date
            new_shift.save()
            return redirect('/admin/')
        return render(request, self.template_name, {'form': form})