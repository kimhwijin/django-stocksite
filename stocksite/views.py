from django.shortcuts import render

from django.views.generic.base import TemplateView
from django.apps import apps
# Create your views here.

#template
class HomeView(TemplateView):
    template_name = 'cover.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_list'] = ['stock']
        return context
