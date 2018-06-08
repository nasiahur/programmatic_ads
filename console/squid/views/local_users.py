import os
import re
import errno
import traceback

#
# domain logic (non django)
#
from _domain.core import Paths
from _domain.squid import LocalUsers

#
#
#
from django.contrib import messages
from django import forms
from django.views import generic
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin

#
#
#
class ViewAuthLocalDbUsersList(generic.TemplateView):

    template_name = 'squid/auth/localdb_users.html'

    def get_context_data(self, **kwargs):

        # create local users database wrapper
        database = LocalUsers()

        # save it in context        
        context = super(ViewAuthLocalDbUsersList, self).get_context_data(**kwargs)        
        context['htpasswd_exists'] = database.exists()
        context['object_list']     = database.get_users()
        
        return context

    def get_success_url(self):
        return reverse_lazy("ViewAuthLocalDbUsersList")

    def post(self, request, *args, **kwargs):

        # create local users database wrapper
        database = LocalUsers()

        for selected_id in request.POST.getlist('selected_id'):            
            database.delete_user(selected_id)
            
        # tell the user squid needs to be reloaded or restarted            
        messages.info(self.request, "need_squid_restart")

        # and redirect to success url
        return HttpResponseRedirect(self.get_success_url())

#
#
#    
class AuthLocalDbUserForm(forms.Form):

    user     = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32)
    comment  = forms.CharField(max_length=512, widget=forms.Textarea(), required=False)
    
    def clean_user(self):

        user = self.cleaned_data['user']
        user = user.strip()

        matched = re.match(r"^[\w\.]+$", user, re.M|re.I)
        if not matched:
            raise forms.ValidationError("User name can only be alpha-numeric (including dot).")
        
        for prohibited in [':', ' ', '\r', '\n']:
            if user.find(prohibited) != -1:
                raise forms.ValidationError("User name cannot contain whitespaces and comma symbols.")

        # we only support lower cased user names because of bug 1687
        if user.lower() != user:
            raise forms.ValidationError("Sorry for now only lower cased user names are supported.")

        return user

    def clean_comment(self):

        comment = self.cleaned_data['comment']
        if len(comment) > 0:
            # check to see the comment does not have unicode symbols
            try:
                comment_str = str(comment)
            except Exception as e:
                raise forms.ValidationError("Comment can only contain ASCII symbols. Error '%s'." % (str(e),) )
        return comment

#
#
#
class ViewAuthLocalDbUsersCreate(SuccessMessageMixin, generic.edit.FormView):

    form_class      = AuthLocalDbUserForm
    template_name   ='squid/auth/localdb_users_form.html'
    success_message = "need_squid_restart"    

    def get_success_url(self):
        return reverse_lazy("ViewAuthLocalDbUsersList")

    def form_valid(self, form):

        try:
            user    = form.cleaned_data['user']
            pasw    = form.cleaned_data['password']
            comment = form.cleaned_data['comment']

            database = LocalUsers()
            database.create_user(user, pasw, comment)

            return HttpResponseRedirect(self.get_success_url()) 
            
        except Exception as e:        

            # make a human message
            error_str = "Exception: %s\n\nCall stack:\n%s" % (str(e), traceback.format_exc())

            # save it into form
            form.errors['__all__'] = form.error_class([error_str])

            # failure
            return super(ViewAuthLocalDbUsersCreate, self).form_invalid(form)

#
#
#
class AuthLocalDbUserUpdateForm(forms.Form):

    password = forms.CharField(max_length=32, required=False)
    comment  = forms.CharField(max_length=512, widget=forms.Textarea(), required=False)

    def clean_comment(self):
        comment = self.cleaned_data['comment']
        if len(comment) > 0:
            # check to see the comment does not have unicode symbols
            try:
                comment_str = str(comment)
            except Exception as e:
                raise forms.ValidationError("Comment can only contain ASCII symbols. Error '%s'." % (str(e),) )
        return comment

#
#
#
class ViewAuthLocalDbUsersUpdate(SuccessMessageMixin, generic.View):

    template_name   ='squid/auth/localdb_users_update.html'
    success_message = "need_squid_restart"    
    
    def get_success_url(self):
        return reverse_lazy("ViewAuthLocalDbUsersList")
    
    def get(self, request, *args, **kwargs):

        database = LocalUsers()
        
        user  = database.get_user(self.kwargs['pk'])
        data  = {'comment' : user['comment'] }
        form  = AuthLocalDbUserUpdateForm(initial=data)

        return render(request, self.template_name, {'form': form })

    def post(self, request, *args, **kwargs):

        form  = AuthLocalDbUserUpdateForm(request.POST)
        if form.is_valid():

            database = LocalUsers()

            username = kwargs['pk']
            comment  = form.cleaned_data['comment']
            password = form.cleaned_data['password'].strip()
            if len(password) > 0:
                # remove user and create it again thus changing user password
                database.delete_user(username)
                database.create_user(username, password, comment)
            else:
                # only update comment
                database.update_comment(username, comment)

            # mark as needing reload
            messages.info(self.request, "need_squid_restart")

            return HttpResponseRedirect(self.get_success_url()) 

        return render(request, self.template_name, {'form': form })

#
#
#
class ViewAuthLocalDbExport(generic.View):

    def get(self, request, *args, **kwargs):            

        path = os.path.join(Paths.etc_dir(), "users.htpasswd")
        with open(path, "rb") as fin:
            response = HttpResponse(fin.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = "attachment; filename=\"%s\"" % "users.htpasswd"
            return response

#
#
#
class AuthLocalDbImportForm(forms.Form):
    file = forms.FileField()

#
#
#
class ViewAuthLocalDbImport(SuccessMessageMixin, generic.edit.FormView):

    form_class      = AuthLocalDbImportForm
    template_name   = 'squid/auth/localdb_users_import.html'
    success_message = 'need_squid_restart'
    
    def get_success_url(self):
        return reverse_lazy("ViewAuthLocalDbUsersList")

    def form_valid(self, form):

        try:
            data = self.request.FILES['file']

            # first we try to write the file next to actual one
            old_file = os.path.join(Paths.etc_dir(), "users.htpasswd")
            new_file = old_file + ".new"
            
            # remove the existing new file(s) which may not even exist
            try:
                os.remove(new_file)
            except OSError as e:
                if e.errno != errno.ENOENT:
                    raise

            # write the new file 
            with open(new_file, 'wb') as fout:
                for chunk in data.chunks():
                    fout.write(chunk)

            # now replace the new files 
            if os.path.isfile(old_file):
                os.remove(old_file)
            
            os.rename(new_file, old_file)

            # ok if we got here everything is fine
            return super(ViewAuthLocalDbImport, self).form_valid(form)
            
        except Exception as e:        
            form.errors['__all__'] = form.error_class(["%s" % str(e)])

            # failure
            return super(ViewAuthLocalDbImport, self).form_invalid(form)