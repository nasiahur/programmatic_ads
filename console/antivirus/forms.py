#
# system
#

'''
import re
import socket
import struct
import multiprocessing

#
# django
#
from django import forms
from django.shortcuts import get_object_or_404

#
# our
#
from squid.models import *
from safety.models import *
from utility.forms import ValueCommentForm
from utility.validator import *

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

       
class ExclusionDomainNameImportForm(forms.Form): 
    file = forms.FileField()

####################################################################################################
#
#
# MEMBERS
#
#
####################################################################################################
        
class MemberLdapTestForm(forms.Form):
    search = forms.CharField(max_length=1024)
    leave_tmp = forms.BooleanField(required=False)  

    def clean_value(self):
        value = self.cleaned_data['value']
        if len(value.strip()) == 0:
            raise forms.ValidationError("Cannot test LDAP search with empty user name") 
        return value
        


####################################################################################################
#
#
# RULE
#
#
####################################################################################################
       
class RuleBlockFileForm(forms.ModelForm):

    value = forms.CharField(max_length=512, widget=forms.TextInput(
        attrs={'size':'50','class':'input-block-level'})
    )
    comment = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'size':'90', 'rows':'3', 'class':'input-block-level'}),
        required=False
    )
    

'''