from django.views.generic import TemplateView
from django.shortcuts import render, redirect

# Create your views here.
class HomePage(TemplateView):
    template_name = 'pagecontent/index.html'

class Dashboard(TemplateView):
    template_name = 'pagecontent/dashboard.html'
