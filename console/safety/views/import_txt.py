from django import forms
from django.views import generic
from django.shortcuts import render
from django.contrib import messages 
from django.db.models import Max
from django.apps import apps
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

#
#
#
from safety.models import *

#
# tool to upload a textual file into the list of entries
#
IMPORT_WEBSAFETY_FILE_CHOICES = (
    ('MemberName', 'Member Name'),
    ('MemberIp', 'Member Ip'),
    ('MemberRange', 'Member Range'),
    ('MemberSubnet', 'Member Subnet'),
    ('ExclusionDomain', 'Exclusion Domain'),
    ('ExclusionIp', 'Exclusion Ip'),
    ('ExclusionRange', 'Exclusion Range'),
    ('ExclusionSubnet', 'Exclusion Subnet'),
    ('ExclusionUrl', 'Exclusion Url'),
    ('ExclusionContentType', 'Exclusion Content Type'),
    ('RuleDomain', 'Rule Domain'),
    ('RuleUrl', 'Rule Url'),
    ('RuleUserAgent', 'Rule User Agent'),
    ('RuleContentType', 'Rule Content Type'),
    ('RuleCharset', 'Rule Charset'),
    ('RuleFileName', 'Rule File Name'),
)

#
#
#
class UploadFileForm(forms.Form):

    file = forms.FileField()
    type = forms.ChoiceField(choices=IMPORT_WEBSAFETY_FILE_CHOICES)

#
#
#
class ViewImportTxt(generic.View):

    def get(self, request, *args, **kwargs):
        policy_list = Policy.objects.all()
        return render(request, 'safety/tools/upload.html', {'form': UploadFileForm(), 'policy_list' : policy_list })

    def collect(self, data):

        collected = ""
        for chunk in data.chunks():
            collected += chunk

        result = []
        array  = collected.split('\n')
        for line in array:
            line = line.strip('\n')
            line = line.strip('\r')
            line = line.strip(' ')

            if len(line) > 0:
                result.append(line)

        return result

    def drop_comments(self, items):

        result = []
        for item in items:
            pos = item.find("#")
            if pos != -1:
                item = item[:pos].strip()
            if len(item) > 0:
                result.append(item)
        return result

    def get_safety_model(self, model_name):

        models = {
            "MemberName"           : MemberName,
            "MemberIp"             : MemberIp,
            "MemberRange"          : MemberRange,
            "MemberSubnet"         : MemberSubnet,
            "ExclusionDomain"      : ExclusionDomain,
            "ExclusionIp"          : ExclusionIp,
            "ExclusionRange"       : ExclusionRange,
            "ExclusionSubnet"      : ExclusionSubnet,
            "ExclusionUrl"         : ExclusionUrl,
            "ExclusionContentType" : ExclusionContentType,
            "RuleDomain"           : RuleDomain,
            "RuleUrl"              : RuleUrl,
            "RuleUserAgent"        : RuleUserAgent,
            "RuleContentType"      : RuleContentType,
            "RuleCharset"          : RuleCharset,
            "RuleFileName"         : RuleFileName
        }
        for model in models:
            if model == model_name:
                return models[model]

        raise Exception("Cannot find model '%s' in safety app" % model_name)

    def import_file(self, model_name, policy_id, array):

        policy = Policy.objects.get(pk=policy_id)
        query  = getattr(policy, model_name.lower() + "_set")

        for item in array:
            found = query.filter(value__exact=item)
            if len(found) > 0:
                continue

            new_entry        = self.get_safety_model(model_name)()
            new_entry.policy = policy
            new_entry.value  = item
            new_entry.save()

    def post(self, request, *args, **kwargs):

        policy_list = Policy.objects.all()

        # get the form
        form = UploadFileForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'safety/tools/upload.html', {'form': form, 'policy_list' : policy_list })

        # try to import and redisplay if failed
        
        try:

            # process data
            array = []
            if 'file' in self.request.FILES:
                array = self.collect(self.request.FILES['file'])

            # drop all comments
            array = self.drop_comments(array)

            # see if policy id is specified
            if not 'policy' in request.POST:
                raise Exception("Policy id is not found in POST")

            self.import_file(form.cleaned_data['type'], int(request.POST['policy']), array)

        except Exception as e:
            return render(request, 'safety/tools/upload.html', {'form': form, 'error': str(e), 'policy_list' : policy_list })

        # mark as needing reload
        messages.info(self.request, "need_squid_restart")

        # and redirect
        return HttpResponseRedirect(reverse_lazy("ViewImportTxt"))