import os
import shutil
import zipfile
import datetime
import traceback

#
#
#
from django import forms
from django.views import generic
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy

#
#
#
from _domain.core  import Paths, Build
from _domain.utils import read_json_object
from _domain.squid import SquidCertDbInitializer
from frame.models  import Upgrader

#
#
#
class BackUpForm(forms.Form):

    include_sqlite = forms.BooleanField(required=False, initial=True)
    include_certs  = forms.BooleanField(required=False, initial=True)
    include_lic    = forms.BooleanField(required=False, initial=True)
    include_ad     = forms.BooleanField(required=False, initial=True)
    anonymize      = forms.BooleanField(required=False, initial=False)

class ViewBackUp(generic.View):

    def get(self, request, *args, **kwargs):
        return render(request, 'node/tools/backup.html', {'form': BackUpForm() })

#
#
#
class ViewBackUpDownloadTarGz(generic.View):

    def get(self, request, *args, **kwargs):

        # construct the form from GET parameters
        form = BackUpForm(request.GET)

        # call to populate cleaned data array
        form.is_valid()

        # create the temp folder structure
        folder = os.path.join(Paths.var_dir(), "temp", "websafety_backup")
        try:
            shutil.rmtree(folder)
        except:
            pass

        etc_dir = os.path.join(folder, "etc")
        var_dir = os.path.join(folder, "var")

        # and recreate
        os.makedirs(var_dir)

        # copy db
        if form.cleaned_data.get('include_sqlite', True):
            shutil.copy2(os.path.join(Paths.var_dir(), "db", "config.sqlite"), os.path.join(var_dir, "config.sqlite"))
            shutil.copy2(os.path.join(Paths.var_dir(), "db", "config.dump.json"), os.path.join(var_dir, "config.dump.json"))

        # construct patters to ignore
        to_ignore = []
        if not form.cleaned_data.get('include_lic', False):
            to_ignore.append("license.pem")
        if not form.cleaned_data.get('include_certs', False):
            to_ignore.extend(["myca.pem", "myca.der"])
        if not form.cleaned_data.get('include_ad', False):
            to_ignore.extend(["krb5.keytab", "krb5.conf", "ldaps.pem"])

        shutil.copytree(
            Paths.etc_dir(), 
            etc_dir, 
            ignore = shutil.ignore_patterns(*to_ignore)
        )

        # pack it
        today    = datetime.date.today()
        arc_name = "websafety_backup_%s_%s" % (Build.version(), today.strftime("%Y_%m_%d"))
        arc_path = os.path.join(Paths.var_dir(), "temp", arc_name)
        shutil.make_archive(arc_path, 'zip', folder)

        # and send it
        response = None
        with open(arc_path + ".zip" , "rb") as fin:
            response = HttpResponse(fin.read(), content_type="application/x-compressed")
            response['Content-Disposition'] = "attachment; filename=\"%s.zip\"" % arc_name

        # and remove
        os.unlink(arc_path + ".zip")

        # and return response
        return response


#
#
#
class RestoreBackUpForm(forms.Form):

    ACTION_CHOICES=[
        ('restore','Restore SQLite configuration database from previously made backup. Everything else remains intact.'), 
        ('import','Import configuration from another product version'),
        ('reset','Reset configuration to default. All your settings will be lost!')
    ]

    file           = forms.FileField(required=False)
    action         = forms.ChoiceField(choices=ACTION_CHOICES, widget=forms.RadioSelect())
    restore_config = forms.BooleanField(required=False, initial=True)
    restore_certs  = forms.BooleanField(required=False, initial=False)
    restore_htmls  = forms.BooleanField(required=False, initial=False)
    restore_lic    = forms.BooleanField(required=False, initial=False)
    restore_ad     = forms.BooleanField(required=False, initial=True)
    dryrun         = forms.BooleanField(required=False,initial=False)

#
#
#
class ViewRestore(generic.edit.FormView):

    template_name = 'node/tools/restore.html'
    form_class    = RestoreBackUpForm

    def get_success_url(self):
        return reverse_lazy("node:ViewRestore")

    def form_valid(self, form):

        try:
            # try to restore config
            self.do_action(form)

            # mark as needing restart
            messages.info(self.request, "need_squid_restart")

            # if we got here, restore was successful
            return super(ViewRestore, self).form_valid(form)

        except Exception as e:

            # in case of error, dump it
            form.errors['__all__']   = form.error_class(["%s" % str(e)])
            form.errors['traceback'] = "%s" % traceback.format_exc()

            # and fail
            return super(ViewRestore, self).form_invalid(form)

    def do_action(self, form):

        # process reset right away
        action = form.cleaned_data['action']
        if action == "reset":
            return self.do_reset()

        # if we got here, it is definitely not reset, see if file is present
        if not form.cleaned_data['file']:
            raise Exception("File is required for restore and import action!")

        # process the uploaded file
        arch_name  = self.collect_zip()
        unpack_dir = self.unzip(arch_name)

        # set version hint (default empty) 
        version4 = ""
        version2 = ""

        try:
            data     = read_json_object(os.path.join(unpack_dir, "etc", "version.json"))
            version4 = data['version']
            digits   = version4.split(".")            
            version2 = "%s.%s" % (digits[0], digits[1])

        except Exception as e:

            version2 = ""
            version4 = ""

        if action == "restore":
            self.do_restore(unpack_dir, version2, version4)
        elif action == "import":
            self.do_import(form, unpack_dir, version2, version4)
        else:
            raise Exception("Unknown action '%s'" % action)

    def do_reset(self):

        src_db = os.path.join(Paths.var_dir(), "db", "config.sqlite.default")
        dst_db = os.path.join(Paths.var_dir(), "db", "config.sqlite")
        bak_db = os.path.join(Paths.var_dir(), "db", "config.sqlite.backup")

        if not os.path.isfile(src_db):
            raise Exception("Default database '%s' not found or not accessible!" % src_db)

        if os.path.isfile(bak_db):
            os.unlink(bak_db)
        shutil.copy2(dst_db, bak_db)

        shutil.copy2(src_db, dst_db)

    def do_restore(self, unpack_dir, version2, version4):

        # restore is ONLY possible for the same version
        if version4 != Build.version():
            raise Exception("Cannot restore, version mismatch: uploaded %s != our %s" % (version4, Build.version()))

        # we do restore by replacing the database
        src_db = os.path.join(unpack_dir, "var", "config.sqlite")
        dst_db = os.path.join(Paths.var_dir(), "db", "config.sqlite")
        bak_db = os.path.join(Paths.var_dir(), "db", "config.sqlite.backup")

        if not os.path.isfile(src_db):
            raise Exception("Backup database '%s' not found or not accessible!" % src_db)

        if os.path.isfile(bak_db):
            os.unlink(bak_db)
        shutil.copy2(dst_db, bak_db)

        shutil.move(src_db, dst_db)

    def do_import(self, form, unpack_dir, version2, version4):

        # see what we need to do
        test_only      = form.cleaned_data.get('dryrun', False)
        restore_config = form.cleaned_data.get('restore_config', False)
        restore_certs  = form.cleaned_data.get('restore_certs', False)
        restore_htmls  = form.cleaned_data.get('restore_htmls', False)
        restore_lic    = form.cleaned_data.get('restore_lic', False)
        restore_ad     = form.cleaned_data.get('restore_ad', False)

        if restore_config:

            upgrader = Upgrader(test_only, version2)
            upgrader.upgrade(os.path.join(unpack_dir, "etc"))

        files = []
        if restore_htmls:
            files.extend(["blocked_adult.html", "blocked_domains.html", "blocked_general.html", "bypass_partial.html", "blocked_image.gif"])
        if restore_certs:
            files.extend(["myca.der", "myca.pem"])
        if restore_lic:
            files.extend(["license.pem"])
        if restore_ad:
            files.extend(["krb5.conf", "krb5.keytab", "ldaps.pem"])

        # copy files    
        for file in files:

            src_file = os.path.join(unpack_dir, "etc", file)
            if not os.path.isfile(src_file):
                continue

            bak_file = os.path.join(unpack_dir, "etc", file + ".bak")
            dst_file = os.path.join(Paths.etc_dir(), file)

            if os.path.isfile(bak_file):
                os.unlink(bak_file)

            if os.path.isfile(dst_file):
                shutil.move(dst_file, bak_file)
            shutil.move(src_file, dst_file)

        # do some additional actions for certificates
        if restore_certs:
            SquidCertDbInitializer().initialize()


    def collect_zip(self):

        # will write zip data to a temp folder
        folder = os.path.join(Paths.var_dir(), "temp", "websafety_restore")
        try:
            shutil.rmtree(folder)
        except:
            pass
        os.makedirs(folder)

        # collect all chunks into it        
        data = self.request.FILES['file']
        name = os.path.join(folder, "websafety_backup.zip")

        try:
            os.unlink(name)
        except:
            pass

        with open(name, "wb") as fout:
            for chunk in data.chunks():
                fout.write(chunk)

        # fine, zip is there
        return name

    def unzip(self, arch_name):

        parent_dir = os.path.dirname(arch_name)

        with zipfile.ZipFile(arch_name,"r") as fin:
            fin.extractall(parent_dir)

        return parent_dir