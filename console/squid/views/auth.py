import os
import re
import errno
import traceback
import json

#
# domain logic (non django)
#
from _domain.core import Paths
from _domain.utils import FileWriter, JsonDumper
from _domain.squid import \
    AdDetector, \
    LdapTester, \
    LdapsDetector, \
    LocalUsers, \
    KeyTabDumper, \
    KeyTabInitializer, \
    KvnoChecker, \
    PseudoAuthDumper

#
#
#
from django import forms
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.template import loader, Context
from django.forms.utils import ErrorList

#
#
#
from squid.generator import Generator
from squid.models import \
    AuthAd, \
    AuthLocalDb, \
    AuthRadius, \
    AuthLabel, \
    AuthLabelUsers, \
    AuthPseudoAd
    
#
# 
#
class ViewAuthExplicit(SuccessMessageMixin, generic.base.TemplateView):

    template_name   ='squid/auth/mode_explicit.html'
    success_message = "need_squid_restart"

    def get_context_data(self, **kwargs):

        context = super(ViewAuthExplicit, self).get_context_data(**kwargs)        
        
        context['authad']      = AuthAd.objects.first()
        context['authlocaldb'] = AuthLocalDb.objects.first()
        context['authradius']  = AuthRadius.objects.first()
        context['authlabel']   = AuthLabel.objects.first()
        
        return context

#
#
#
class AuthAdForm(forms.ModelForm):    
    
    class Meta:
        model  = AuthAd
        fields = ['dc1addr', 'dc2addr', 'base_dn', 'bind_user', 'bind_pass', 'lookup_mode']

    lookup_mode = forms.ChoiceField(choices=AuthAd.LOOKUP_MODE_CHOICES, widget=forms.RadioSelect)
    
class ViewAuthDomainEdit(SuccessMessageMixin, generic.edit.UpdateView):

    template_name   ='squid/auth/domain.html'
    success_message = "need_squid_restart"
    model           = AuthAd
    form_class      = AuthAdForm

    def get_object(self):
        return AuthAd.objects.first()
    
    def get_success_url(self): 
        return reverse_lazy('ViewAuthDomainEdit')

#
#
#
class ViewAuthDetect(generic.View):

    def get(self, request, *args, **kwargs):

        # call the detector
        detector = AdDetector()
        data     = detector.detect()

        return HttpResponse(json.dumps(data, ensure_ascii=True), content_type='application/json')

#
#
#
class ViewAuthDomainTest(generic.DetailView):
    
    template_name ='squid/auth/domain_test.html'
    model         = AuthAd

    def get_object(self):
        return AuthAd.objects.first()

    def test_ldap(self, object):

        # here we have django model auth domain updated, but we also need to generate JSON files in /opt/websafety/etc
        g = Generator(os.path.join(Paths.etc_dir(), "squid"))
        w = FileWriter(os.path.join(Paths.etc_dir(), "squid"))
        d = JsonDumper()
        
        g.generate_auth(w, d)

        # and run the tests
        result = LdapTester().run();
        if result['exit_code'] == 0:
            return (True, "%s %s" % (result['stdout'], result['stderr']))
        else:
            return (False, "Exit code: %s\nSTDOUT: %s\nSTDERR: %s\n" % (str(result['exit_code']), result['stdout'], result['stderr']))
        pass

    def get_context_data(self, **kwargs):

        context = super(ViewAuthDomainTest, self).get_context_data(**kwargs)

        (result, output) = self.test_ldap(self.object)
        context['success'] = result
        context['output']  = output

        return context

#
#
#    
class ViewAuthDomainLdapsRemove(generic.View):
    
    def get(self, request, *args, **kwargs):            
        path = os.path.join(Paths.etc_dir(), "ldaps.pem")
        if os.path.isfile(path):
            os.remove(path)
        
        return HttpResponseRedirect(reverse_lazy('ViewAuthDomainLdaps'))

#
#
#
class ViewLdapsDetect(generic.View):
    
    def get(self, request, *args, **kwargs):     

        # get names
        dc1addr = AuthAd.objects.first().dc1addr
        dc2addr = AuthAd.objects.first().dc2addr

        try:
            (result1, cert_contents1) = self.get_certificate(dc1addr)
            (result2, cert_contents2) = self.get_certificate(dc2addr)

            if result1 and result2:

                # both domain controllers respond over LDAPS, concatenate the certs
                cert_contents  = ""
                cert_contents += cert_contents1
                cert_contents += "\n"
                cert_contents += cert_contents2

                # and save it
                self.save_certificate(cert_contents)

            elif result1 or result2:

                # at least one domain controller responded over LDAPS, get its cert
                cert_contents = ""
                if result1:
                    cert_contents += cert_contents1
                if result2:
                    cert_contents += cert_contents2

                # and save it
                self.save_certificate(cert_contents)
                
            else:

                # otherwise none of the LDAPS servers responded, throw away the error
                raise Exception("Cannot get certificates from both domain controllers. Error: %s" % cert_contents)

            return HttpResponseRedirect(reverse_lazy('ViewAuthDomainLdaps'))

        except Exception as e:
            return HttpResponseRedirect(reverse_lazy('ViewAuthDomainLdaps'))

    def get_certificate(self, dcaddr):

        try:
            # check input params
            if not dcaddr:
                raise Exception("DC address is empty")

            # ask the server
            detector = LdapsDetector()
            output   = detector.dump_from_server(dcaddr)

            # and return nicely
            return (True, output)

        except Exception as e:
            return (False, str(e))

    def save_certificate(self, cert_contents):

        # first we try to write the file next to actual one
        old_pem = os.path.join(Paths.etc_dir(), "ldaps.pem")
        new_pem = old_pem + ".new"

        # remove the existing new file(s) which may not even exist
        try:
            os.remove(new_pem)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

        # write the new pem file 
        with open(new_pem, 'wb') as fout:
            fout.write(cert_contents)

        # run the certmgr that will verify this file - may throw!
        detector = LdapsDetector()
        output   = detector.dump(new_pem)
        
        # now replace the new files 
        if os.path.isfile(old_pem):
            os.remove(old_pem)
        os.rename(new_pem, old_pem)


#
#
#
class AuthDomainLdapsUploadForm(forms.Form):
    file = forms.FileField()
     
class ViewAuthDomainLdaps(SuccessMessageMixin, generic.edit.FormView):

    form_class      = AuthDomainLdapsUploadForm
    template_name   ='squid/auth/domain_ldaps.html'
    success_message = "need_squid_restart"
    
    def get_success_url(self):         
        return reverse_lazy('ViewAuthDomainLdaps')
    
    def get_context_data(self, **kwargs):

        context = super(ViewAuthDomainLdaps, self).get_context_data(**kwargs)     

        # create the detector  
        detector = LdapsDetector()
        
        # dump the info about current LDAPS certificate
        result = False
        output = ""
        raw    = ""
        
        try:
            raw    = detector.dump_raw("ldaps.pem")
            output = detector.dump("ldaps.pem")
            result = True
        except Exception as e:
            output = "ERROR: LDAPS connections will fail!!!\nTechnical info: %s\n" % str(e)

        context['cacert_raw']    = raw
        context['cacert_output'] = output
        context['cacert_result'] = result


        return context

    def form_valid(self, form):

        try:
            data = self.request.FILES['file']

            # first we try to write the file next to actual one
            old_pem = os.path.join(Paths.etc_dir(), "ldaps.pem")
            new_pem = old_pem + ".new"

            # remove the existing new file(s) which may not even exist
            try:
                os.remove(new_pem)
            except OSError as e:
                if e.errno != errno.ENOENT:
                    raise

            # write the new pem file 
            with open(new_pem, 'wb') as fout:
                for chunk in data.chunks():
                    fout.write(chunk)

            # run the certmgr that will verify this file - will throw in case file is invalid
            detector = LdapsDetector()
            detector.dump(new_pem)

            # now replace the new files 
            if os.path.isfile(old_pem):
                os.remove(old_pem)
            os.rename(new_pem, old_pem)
            
            # ok if we got here everything is fine
            return super(ViewAuthDomainLdaps, self).form_valid(form)
            
        except Exception as e:        
            form.errors['__all__'] = form.error_class([
                "%s\n%s" % (str(e), traceback.format_exc()) 
            ])

            # failure
            return super(ViewAuthDomainLdaps, self).form_invalid(form)

#
#
#
class ViewAuthDomainLdapsExport(generic.View):

    def get(self, request, *args, **kwargs):            

        path = os.path.join(Paths.etc_dir(), "ldaps.pem")
        with open(path, "rb") as fin:
            response = HttpResponse(fin.read(), content_type="application/x-x509-ca-cert")
            response['Content-Disposition'] = "attachment; filename=\"%s\"" % "ldaps.pem"
            return response

#
# kerberos
#
class AuthSchemeKerberosForm(forms.ModelForm):    
    
    class Meta:
        model  = AuthAd
        fields = ['krb5_enable', 'realm', 'krb5_spn', 'krb5_use_gssnoname', 'krb5_no_replay_cache', 'krb5_helper_total', 'krb5_helper_idle', 'krb5_helper_startup', 'krb5_helper_verbose']
    
    keytab = forms.FileField(required=False)                  # additional field NOT stored in the model
    
    def clean_krb5_spn(self):

        value = self.cleaned_data['krb5_spn']
        value = value.strip()

        pattern = r'HTTP\/(.+)@(.+)'
        match   = re.match(pattern, value, re.M|re.I)
        if not match:
            raise forms.ValidationError("Cannot check SPN using regex pattern '%s'. A valid SPN looks like for example HTTP/proxy.example.lan@EXAMPLE.LAN" % pattern)
        else:
            fqdn  = match.group(1)
            realm = match.group(2)

            if realm.upper() != realm:
                raise forms.ValidationError("Specified SPN is incorrect. Realm part after @ must be CAPITAL LETTERS only. You have '%s' and it must be '%s'." % (realm, realm.upper()))

            if fqdn.find(".") == -1:
                raise forms.ValidationError("The FQDN part of SPN (%s) must contain at least one dot. A valid SPN looks like for example HTTP/proxy.example.lan@EXAMPLE.LAN" % fqdn)

        return value

    def clean_realm(self):

        value = self.cleaned_data['realm']
        value = value.strip()

        if not value:
            raise forms.ValidationError("Kerberos realm is required and it MUST be uppercase.")

        if value.upper() != value:
            raise forms.ValidationError("Specified Kerberos is incorrect. Realm must be CAPITAL LETTERS only. You have '%s' and it must be '%s'." % (value, value.upper()))

        return value

#
#
#
class ViewAuthNegotiateSchemeEdit(SuccessMessageMixin, generic.edit.UpdateView):

    template_name   = "squid/auth/negotiate.html"
    success_message = "need_squid_restart"
    model           = AuthAd
    form_class      = AuthSchemeKerberosForm

    def get_object(self):
        return AuthAd.objects.first()

    def get_success_url(self): 
        return reverse_lazy('ViewAuthNegotiateSchemeEdit')

    def write_krb5_conf(self, realm):

        # debug check
        assert(realm)

        # construct paths
        old_conf = os.path.join(Paths.etc_dir(), "krb5.conf")
        new_conf = old_conf + ".new"

        # write new
        with open(new_conf, "wb") as fout:

            template = loader.get_template('squid/conf/krb5.conf')
            context  = {
                "realm" : realm 
            }
            fout.write(template.render(context))

        # replace
        if os.path.isfile(old_conf):
            os.remove(old_conf)
        os.rename(new_conf, old_conf)

    def write_keytab(self, spn, data): # data is forms.FileField

        assert(spn)

        # no data - no nothing
        if data is None:
            return

        # write the file next to actual one
        old_keytab = os.path.join(Paths.etc_dir(), "krb5.keytab")
        new_keytab = old_keytab + ".new"

        # remove the existing new file(s) which may not even exist
        try:
            os.remove(new_keytab)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

        # write the new keytab file 
        with open(new_keytab, 'wb') as fout:
            for chunk in data.chunks():
                fout.write(chunk)

        # run the keytab dump command that will verify this file - will throw in case of bad keytab
        KeyTabDumper().dump(new_keytab)

        # keytab may be valid but we also need to run kinit to see if it works with Squid SPN
        (result, output) = KeyTabInitializer().initialize(new_keytab, spn)
        if result != True:
            raise Exception("Uploaded KeyTab file does not correspond to SPN; error: %s" % output)

        # now replace the old files with new ones
        if os.path.isfile(old_keytab):
            os.remove(old_keytab)
        os.rename(new_keytab, old_keytab)

    def form_valid(self, form):

        try:

            # get realm
            realm = form.cleaned_data['realm']

            # debug check it is fine
            assert(len(realm) > 0)
            assert(realm.upper() == realm)
            
            # aways update the kerberos conf file
            self.write_krb5_conf(realm)

            # update the kerberos keytab file if provided by user                        
            self.write_keytab(form.cleaned_data['krb5_spn'], form.cleaned_data.get('keytab', None))

            # see what we must do
            enable = form.cleaned_data['krb5_enable']
            if enable:

                # ok user wants to enable the authenticator, check if everything is in place
                keytab   = os.path.join(Paths.etc_dir(), "krb5.keytab")
                krb5conf = os.path.join(Paths.etc_dir(), "krb5.conf")

                if os.path.isfile(krb5conf) and os.path.isfile(keytab):
                    
                    # good everything is fine, proceed
                    pass

                else:

                    # no-no, we cannot enable!
                    if not os.path.isfile(keytab):

                        errors = form._errors.setdefault("keytab", ErrorList())
                        errors.append(u"This field is required to enable Kerberos authenticator.")

                        errstr = "Cannot enable Kerberos authenticator. KeyTab file '%s' is not found! Please click on the Browse button and upload the KeyTab from your computer." % keytab

                    else:
                        errstr = "Cannot enable Kerberos authenticator. krb5.conf file '%s' is not found!" % krb5conf

                    # and fail 
                    raise Exception(errstr)

            # if we got here everything is fine (either enabled or disabled successfully)
            return super(ViewAuthNegotiateSchemeEdit, self).form_valid(form)
            
        except Exception as e:        
            form.errors['__all__'] = form.error_class([
                "%s\n%s" % (str(e), traceback.format_exc()) 
            ])

            # failure
            return super(ViewAuthNegotiateSchemeEdit, self).form_invalid(form)

    def get_context_data(self, **kwargs):

        context = super(ViewAuthNegotiateSchemeEdit, self).get_context_data(**kwargs)        

        # this is the path to keytab
        keytab_path = os.path.join(Paths.etc_dir(), "krb5.keytab")
        
        # dump contents of keytab
        try:
            context['keytab'] = KeyTabDumper().dump(keytab_path)
        except Exception as e:
            context['keytab'] = str(e)
        
        # verify keytab is valid for spn
        (result, output) = KeyTabInitializer().initialize(keytab_path, self.object.krb5_spn)
        context['kinit_result'] = result
        context['kinit_output'] = output

        # read krb5.conf
        try:
            path = os.path.join(Paths.etc_dir(), "krb5.conf")
            with open(path, "r") as fin:
                context['krb5conf'] = fin.read()
        except Exception as e:
            context['krb5conf'] = "Error reading %s file: %s" % (path, str(e))


        # construct some params
        use_ldaps = False
        if self.object.lookup_mode in (AuthAd.LOOKUP_MODE_LDAP, AuthAd.LOOKUP_MODE_GC):
            use_ldaps = False
        if self.object.lookup_mode in (AuthAd.LOOKUP_MODE_LDAPS, AuthAd.LOOKUP_MODE_GCS):
            use_ldaps = True

        # check kvno
        (result, output) = KvnoChecker(
            self.object.dc1addr,  
            self.object.lookup_mode,
            use_ldaps,
            self.object.base_dn,
            self.object.bind_user,
            self.object.bind_pass
        ).check(keytab_path, self.object.krb5_spn)
        context['kvno_result'] = result
        context['kvno_output'] = output
        
        return context

#
#
#
class ViewAuthNegotiateSchemeGetKeyTab(generic.View):

    def get(self, request, *args, **kwargs):            
        path = os.path.join(Paths.etc_dir(), "krb5.keytab")
        with open(path, "rb") as fin:
            response = HttpResponse(fin.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = "attachment; filename=\"%s\"" % "krb5.keytab"
            return response

#
#
#
class ViewAuthNtlmSchemeEdit(SuccessMessageMixin, generic.edit.UpdateView):

    template_name   = "squid/auth/ntlm.html"
    success_message = "need_squid_restart"    
    model           = AuthAd
    fields          = ['ntlm_enable', 'ntlm_helper_verbose', 'ntlm_helper_total', 'ntlm_helper_idle', 'ntlm_helper_startup']

    def get_object(self):
        return AuthAd.objects.first()

    def get_success_url(self): 
        return reverse_lazy('ViewAuthNtlmSchemeEdit')

#
#
#
class ViewAuthLdapSchemeEdit(SuccessMessageMixin, generic.edit.UpdateView):

    template_name   = "squid/auth/ldap.html"
    success_message = "need_squid_restart"
    model           = AuthAd    
    fields          = ['ldap_enable', 'ldap_title', 'ldap_credsttl', 'ldap_helper_verbose', 'ldap_helper_total', 'ldap_helper_idle', 'ldap_helper_startup']

    def get_object(self):
        return AuthAd.objects.first()

    def get_success_url(self): 
        return reverse_lazy('ViewAuthLdapSchemeEdit')

#
#
#
class ViewAuthGroupMembershipEdit(SuccessMessageMixin, generic.edit.UpdateView):

    template_name   = "squid/auth/group_membership.html"
    success_message = "need_squid_restart"
    model           = AuthAd    
    fields          = ['cachetime', 'timeout']

    def get_object(self):
        return AuthAd.objects.first()

    def get_success_url(self): 
        return reverse_lazy('ViewAuthGroupMembershipEdit')

#
# auth local db
#
class ViewAuthLocalDbEdit(SuccessMessageMixin, generic.edit.UpdateView):

    template_name   ='squid/auth/localdb_general.html'
    success_message = "need_squid_restart"
    model           = AuthLocalDb
    fields          = ['enable', 'title', 'helper_verbose', 'helper_total', 'helper_idle', 'helper_startup']

    def get_object(self):
        return AuthLocalDb.objects.first()

    def get_success_url(self): 
        return reverse_lazy('ViewAuthLocalDbEdit')

    def form_valid(self, form):

        try:
            enable = form.cleaned_data['enable']
            if enable:            
                database = LocalUsers()
                users    = database.get_users()
                if len(users) == 0:
                    raise Exception("cannot activate Local User Authentication without at least one user configured.")

            return super(ViewAuthLocalDbEdit, self).form_valid(form)
            
        except Exception as e:        
            form.errors['__all__'] = form.error_class(["%s" % str(e)])

            # failure
            return super(ViewAuthLocalDbEdit, self).form_invalid(form)

#
# auth radius
#
class ViewAuthRadiusEdit(SuccessMessageMixin, generic.edit.UpdateView):

    template_name   ='squid/auth/radius_form.html'
    success_message = "need_squid_restart"
    model           = AuthRadius
    fields          = ['enable', 'server', 'secret', 'title', 'helper_verbose', 'helper_total', 'helper_idle', 'helper_startup']

    def get_object(self):
        return AuthRadius.objects.first()

    def get_success_url(self): 
        return reverse_lazy('ViewAuthRadiusEdit')

#
# auth - user labelling
#
class ViewAuthLabelEdit(SuccessMessageMixin, generic.edit.UpdateView):

    template_name   ='squid/auth/label_general.html'
    success_message = "need_squid_restart"
    model           = AuthLabel
    fields          = ['enable', 'resolve_ip_as_user_name']

    def get_object(self):   
        return AuthLabel.objects.first()

    def get_success_url(self): 
        return reverse_lazy('ViewAuthLabelEdit')

class ViewAuthLabelList(generic.ListView):

    template_name ='squid/auth/label_users.html'
    model         = AuthLabelUsers
    
    def get_success_url(self):
        return reverse_lazy("ViewAuthLabelList")

    def post(self, request, *args, **kwargs):

        for selected_id in request.POST.getlist('selected_id'):   
            item = get_object_or_404(AuthLabelUsers, pk=selected_id)
            item.delete()         
            
        # tell the user squid needs to be reloaded or restarted            
        messages.info(self.request, "need_squid_restart")

        # and redirect to success url
        return HttpResponseRedirect(self.get_success_url())

class AuthLabelUsersForm(forms.ModelForm):

    class Meta:
        model  = AuthLabelUsers
        fields = ['user_ip', 'user_name', 'user_mac', 'comment']
    
    def clean_user_name(self):
        user = self.cleaned_data['user_name']
        user = user.strip()

        for prohibited in [' ', '\t', '\r', '\n']:
            if user.find(prohibited) != -1:
                raise forms.ValidationError("User name cannot contain whitespaces.")

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

class ViewAuthLabelCreate(SuccessMessageMixin, generic.edit.CreateView):

    template_name   ='squid/auth/label_users_form.html'
    success_message = "need_squid_restart"    
    model           = AuthLabelUsers
    form_class      = AuthLabelUsersForm
    
    def get_success_url(self):
        return reverse_lazy("ViewAuthLabelList")

    def form_valid(self, form):

        try:
            if 'user_ip' in form.cleaned_data:
                if 'user_mac' in form.cleaned_data:

                    user_ip  = form.cleaned_data['user_ip'].strip()
                    user_mac = form.cleaned_data['user_mac'].strip()

                    if len(user_ip) == 0 and len(user_mac) == 0:
                        raise Exception("Please specify either IP or MAC address.")

            return super(ViewAuthLabelCreate, self).form_valid(form)
            
        except Exception as e:        
            form.errors['__all__'] = form.error_class(["%s" % str(e)])

            # failure
            return super(ViewAuthLabelCreate, self).form_invalid(form)
    
class ViewAuthLabelUpdate(SuccessMessageMixin, generic.edit.UpdateView):

    template_name   ='squid/auth/label_users_form.html'
    success_message = "need_squid_restart"    
    model           = AuthLabelUsers
    form_class      = AuthLabelUsersForm

    def get_success_url(self):
        return reverse_lazy("ViewAuthLabelList")

    def form_valid(self, form):

        try:
            if 'user_ip' in form.cleaned_data:
                if 'user_mac' in form.cleaned_data:

                    user_ip  = form.cleaned_data['user_ip'].strip()
                    user_mac = form.cleaned_data['user_mac'].strip()

                    if len(user_ip) == 0 and len(user_mac) == 0:
                        raise Exception("Please specify either IP or MAC address.")

            return super(ViewAuthLabelUpdate, self).form_valid(form)
            
        except Exception as e:        
            form.errors['__all__'] = form.error_class(["%s" % str(e)])

            # failure
            return super(ViewAuthLabelUpdate, self).form_invalid(form)

#
# 
#
class ViewAuthPseudo(SuccessMessageMixin, generic.base.TemplateView):

    template_name   ='squid/auth/mode_pseudo.html'
    success_message = "need_squid_restart"

    def get_context_data(self, **kwargs):

        context = super(ViewAuthPseudo, self).get_context_data(**kwargs)                
        context['authpseudoad'] = AuthPseudoAd.objects.first()        
        context['authlabel']    = AuthLabel.objects.first()
        
        return context

class ViewAuthPseudoEdit(SuccessMessageMixin, generic.edit.UpdateView):

    template_name   ='squid/auth/pseudo_general.html'
    success_message = "need_squid_restart"
    model           = AuthPseudoAd
    fields          = ['enable', 'server1', 'port1', 'server2', 'port2', 'token', 'helper_total', 'helper_idle', 'helper_startup', 'helper_verbose', 'positive_ttl', 'negative_ttl']

    def get_object(self):   
        return AuthPseudoAd.objects.first()

    def get_success_url(self): 
        return reverse_lazy('ViewAuthPseudoEdit')

    def get_context_data(self, **kwargs):

        context = super(ViewAuthPseudoEdit, self).get_context_data(**kwargs)                
        
        # we can only use transparent auth when other types of auth are disabled
        authad      = AuthAd.objects.first()
        authlocaldb = AuthLocalDb.objects.first()
        authradius  = AuthRadius.objects.first()
        allow       = False

        if not authlocaldb.enable:
            if not authradius.enable:
                if not authad.ldap_enable:
                    if not authad.ntlm_enable:
                        if not authad.krb5_enable:
                            allow = True

        context['allow_enable'] = allow
        context['authpseudoad'] = AuthPseudoAd.objects.first()        
        
        return context

class ViewAuthPseudoList(generic.base.TemplateView):

    template_name ='squid/auth/pseudo_users.html'
    
    def get_context_data(self, **kwargs):

        context = super(ViewAuthPseudoList, self).get_context_data(**kwargs)

        object_list     = []
        error_message   = ""
        error_occured   = False
        error_traceback = ""

        try:

            authpseudoad = AuthPseudoAd.objects.first()        

            # we dump ONLY when at least server1 and/or server2 configured
            if authpseudoad.server1 or authpseudoad.server2:
                object_list  = PseudoAuthDumper(
                    authpseudoad.server1, authpseudoad.port1, 
                    authpseudoad.server2, authpseudoad.port2, 
                    authpseudoad.token).dump()
                
        except Exception as e:
            error_occured   = True
            error_message   = str(e)
            error_traceback = "\n%s" % traceback.format_exc()

        context['object_list']     = object_list
        context['error_occured']   = error_occured
        context['error_message']   = "Exception: %s\n\n" % error_message
        context['error_traceback'] = error_traceback
        
        return context


    