#
#
#
from django import forms
from django.views import generic
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect

#
#
#
from .items import ViewItemList, ViewItemCreate, ViewItemUpdate

from squid.models import RefreshPattern

#
# refresh patterns
#
class ViewCacheRefreshPatternList(ViewItemList):

    model         = RefreshPattern
    template_name = "squid/cache/refresh/pattern/list.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewCacheRefreshPatternList")

class RefreshPatternForm(forms.ModelForm):

    class Meta:
        model  = RefreshPattern
        fields = '__all__'

    def clean_percent(self):
        
        percent = self.cleaned_data['percent']
        try:
            if int(percent) < 0 or int(percent) > 100:
                raise Exception("Percent must be within [0:100] interval.")
        except Exception as e:
            raise forms.ValidationError(str(e))

        return percent

    def clean_regex(self):
        regex = self.cleaned_data['regex'].strip()
        if regex.find("\n") != -1:
            raise forms.ValidationError("Regex value must be written as one line")

        return regex

class ViewCacheRefreshPatternCreate(ViewItemCreate):

    model         = RefreshPattern
    form_class    = RefreshPatternForm
    template_name = "squid/cache/refresh/pattern/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewCacheRefreshPatternList")

class ViewCacheRefreshPatternUpdate(ViewItemUpdate):

    model         = RefreshPattern
    form_class    = RefreshPatternForm
    template_name = "squid/cache/refresh/pattern/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewCacheRefreshPatternList")