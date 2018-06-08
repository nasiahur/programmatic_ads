import re
#
#
#
from django import forms
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

#
#
#
from safety.models import Policy, Schedule

#
#
#
from policy_items import PolicyMixin, ListViewEx

#
#
#
class ViewScheduleList(PolicyMixin, ListViewEx):

    model           = Schedule
    success_message = "need_squid_reload"
    template_name   = "safety/rules/schedule_list.html"

    def get_queryset(self):
        return Schedule.objects.filter(policy_id=self.kwargs["pid"])

    def get_success_url(self):
        return reverse_lazy("ViewScheduleList", kwargs={'pid':self.kwargs['pid']})

#
#
#
class ScheduleForm(forms.ModelForm):
    
    class Meta:
        model  = Schedule
        fields = [
            'policy',
            'on_mon', 'on_tue', 'on_wed', 'on_thu', 'on_fri', 'on_sat', 'on_sun',
            'from_hours', 'from_mins',
            'to_hours','to_mins'
        ]

    from_hours = forms.CharField(max_length=2, widget=forms.TextInput(attrs={'size':'5','class':'span2'}))
    from_mins  = forms.CharField(max_length=2, widget=forms.TextInput(attrs={'size':'5','class':'span2'}))
    to_hours   = forms.CharField(max_length=2, widget=forms.TextInput(attrs={'size':'5','class':'span2'}))
    to_mins    = forms.CharField(max_length=2, widget=forms.TextInput(attrs={'size':'5','class':'span2'}))

    def clean(self): 
        form_data = self.cleaned_data

        # see if at least one week day is checked
        checked = False
        for field in ['on_mon', 'on_tue', 'on_wed', 'on_thu', 'on_fri', 'on_sat', 'on_sun']:
            value = form_data[field]
            if value:
                checked = True
                break
        if not checked:
            raise forms.ValidationError("Please, select at least one day of week.")

        # the to hours must be at least more than from
        from_hours = form_data['from_hours']
        to_hours   = form_data['to_hours']
        if int(from_hours) > int(to_hours):
            raise forms.ValidationError("'From Hour' must be at least less than or equal to 'To Hour'.")

        if int(from_hours) == int(to_hours):
            from_mins = form_data['from_mins']
            to_mins   = form_data['to_mins']
            if int(from_mins) >= int(to_mins):
                raise forms.ValidationError("'From Minutes' must be at least less than 'To Minutes'.")
        
        return form_data

    def clean_from_hours(self):  
        value = 0
        try:
            value = int(self.cleaned_data['from_hours'])
            if value < 0 or value > 23:
                raise forms.ValidationError("Hours must be within interval from 00 to 23.")
        except TypeError:      
            raise forms.ValidationError("Hours must be within interval from 00 to 23.")
        except ValueError:
            raise forms.ValidationError("Hours must be within interval from 00 to 23.")
        return value

    def clean_from_mins(self):        
        value = 0
        try:
            value = int(self.cleaned_data['from_mins'])
            if value < 0 or value > 59:
                raise forms.ValidationError("Minutes must be within interval from 00 to 59.")
        except TypeError:      
            raise forms.ValidationError("Minutes must be within interval from 00 to 59.")
        except ValueError:
            raise forms.ValidationError("Minutes must be within interval from 00 to 59.")
        return value

    def clean_to_hours(self):        
        value = 0
        try:
            value = int(self.cleaned_data['to_hours'])
            if value < 0 or value > 23:
                raise forms.ValidationError("Hours must be within interval from 00 to 23.")
        except TypeError:      
            raise forms.ValidationError("Hours must be within interval from 00 to 23.")
        except ValueError:
            raise forms.ValidationError("Hours must be within interval from 00 to 23.")
        return value

    def clean_to_mins(self):  
        value = 0
        try:
            value = int(self.cleaned_data['to_mins'])
            if value < 0 or value > 59:
                raise forms.ValidationError("Minutes must be within interval from 00 to 59.")
        except TypeError:      
            raise forms.ValidationError("Minutes must be within interval from 00 to 59.")
        except ValueError:
            raise forms.ValidationError("Minutes must be within interval from 00 to 59.")
        return value
        

#
#
#
class ViewScheduleCreate(PolicyMixin, SuccessMessageMixin, generic.edit.CreateView):

    model           = Schedule
    form_class      = ScheduleForm
    success_message = "need_squid_reload"
    template_name   = "safety/schedule_form.html"

    def get_success_url(self):
        return reverse_lazy("ViewScheduleList", kwargs={'pid':self.kwargs['pid']})

#
#
#
class ViewScheduleUpdate(PolicyMixin, SuccessMessageMixin, generic.edit.UpdateView):

    model           = Schedule
    form_class      = ScheduleForm
    success_message = "need_squid_reload"
    template_name   = "safety/schedule_form.html"

    def get_success_url(self):
        return reverse_lazy("ViewScheduleList", kwargs={'pid':self.kwargs['pid']})
