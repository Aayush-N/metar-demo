from django.shortcuts import render
from django.views.generic.base import TemplateView
# Create your views here.

class LandingPageView(TemplateView):
	'''
	The view displays the initial landing page
	'''
	template_name = "main/index.html"