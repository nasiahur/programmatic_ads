import os
import traceback
import shutil

#
# business logic
#
from _domain.core import Paths, System, Distrib
from _domain.node import NetDeviceEnumerator, NetDeviceDumper, DebianNetworkSettingsGenerator

#
# django
#
from django import forms
from django.views import generic
from django.contrib import messages
from django.template import loader, Context
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy, reverse

#
# ours
#
from node.models import NetManual, NetDevice

#
#
#
class ViewNetworkDeviceList(SuccessMessageMixin, generic.ListView):

    template_name = "node/network/device_list.html"

    def get_queryset(self):
        
        # see if we need to force sync - i.e. read from system
        reread = self.request.GET.get('reread', '')
        if reread in ["1", "on", "yes", "true"]:
            force_sync = True
        else:
            force_sync = False

        # resync devices from system
        self.sync_from_system(force_sync)

        # and return
        return NetDevice.objects.all()

    def remove_stale_devices(self, actual):
        
        # calcuate those to remove
        to_remove = []
        for device in NetDevice.objects.all():
            if device.name not in actual.keys():
                to_remove.append(device)

        # remove all
        for device in to_remove:
            device.delete()

    def add_or_update(self, actual, force_sync):

        device  = None
        devices = NetDevice.objects.filter(name=actual.name)

        # assume we do not need to update the IP address read from system
        update_addr = False
        
        if not devices:
            
            # ok we do not have such a device, add one
            device = NetDevice()
            device.name = actual.name
            device.save()

            # and raise the update address flag
            update_addr = True

        else:

            # we do have a device, get it
            device = devices[0]

            # raise the update the flag if user 'forces' us to read from system
            if force_sync:
                update_addr = True

        # update its settings
        device.state  = actual.state
        device.mac    = actual.mac

        # update IP addresses ONLY if we need to; we need to update the IP addresses of the device when this device is
        # new for our database - so we read its settings from system; or when user specifically told us to force 
        # reading from the system - this can happen if he manually changed the system settings from root console for example
        # and need the system to throw away settings in the database and replace them with the settings from the system
        if update_addr:
            self.update_ip4(device, actual.ip4)
            self.update_ip6(device, actual.ip6)

        # save
        device.save()


    def update_ip4(self, device, addr):

        device.ip4_config     = addr.config_type
        device.ip4_address    = addr.address
        device.ip4_netmask    = addr.netmask
        device.ip4_gateway    = addr.gateway
        device.ip4_dns_srv1   = addr.dns_srv1
        device.ip4_dns_srv2   = addr.dns_srv2
        device.ip4_dns_search = addr.dns_search
        
    def update_ip6(self, device, addr):

        # TODO set IPv6 attributes
        pass

    def sync_from_system(self, force_sync):

        # get all devices from the system
        actual = NetDeviceEnumerator().enumerate()
        
        # remove stale devices from the database
        self.remove_stale_devices(actual)

        # now add or update each actual device
        for key in actual.keys():
            self.add_or_update(actual[key], force_sync)

        # ok now we have synced our database with actual devices from the system

    def get_context_data(self, **kwargs):
        context = super(ViewNetworkDeviceList, self).get_context_data(**kwargs)
        context['devices_dump'] = NetDeviceDumper().dump_devices()
        return context

#
#
#
class NetManualForm(forms.ModelForm):

    class Meta:
        model  = NetManual       
        fields = ['value']

    value = forms.CharField(max_length=512, widget=forms.Textarea(attrs={'size':'90', 'rows':'10', 'class':'input-block-level'}),required=False)

    def clean_value(self):
        value = self.cleaned_data['value']
        if len(value) > 0:
            try:
                value_str = str(value)
            except Exception as e:
                raise forms.ValidationError("Value can only contain ASCII symbols. Error '%s'." % (str(e),) )
        return value

#
#
#
class ViewNetworkManual(SuccessMessageMixin, generic.edit.UpdateView):
    
    model           = NetManual
    form_class      = NetManualForm
    template_name   = "node/network/manual_form.html"
    
    def get_success_url(self):
        return reverse_lazy('node:ViewNetworkManual')

    def get_object(self):
        return NetManual.objects.first()

    def form_valid(self, form):

        try:
            # save the form into the database
            result = super(ViewNetworkManual, self).form_valid(form)

            # get the node and generate all devices
            NetworkGenerateView().generate(
                NetDevice.objects.all(),
                NetManual.objects.first().value
            )

            # tell the user
            messages.info(self.request, "need_reboot")

            # and return successfully
            return result

        except Exception as e:        
            form.errors['__all__'] = form.error_class(["%s\n%s" % (str(e), traceback.format_exc())])

            # failure
            return super(ViewNetworkManual, self).form_invalid(form)

#
#
#
class ViewNetworkDeviceIpv4Update(SuccessMessageMixin, generic.edit.UpdateView):

    model           = NetDevice
    success_message = "need_reboot"
    template_name   = "node/network/device_form_ipv4.html"
    fields          = ['ip4_config', 'ip4_address', 'ip4_netmask', 'ip4_gateway', 'ip4_dns_srv1', 'ip4_dns_srv2', 'ip4_dns_search']

    def get_success_url(self):
        return reverse_lazy('node:ViewNetworkDeviceIpv4Update', kwargs = {'pk' : self.kwargs['pk'] })

    def get_context_data(self, **kwargs):
        context = super(ViewNetworkDeviceIpv4Update, self).get_context_data(**kwargs)
        context['device_dump'] = NetDeviceDumper().dump_device(self.object.name)
        return context

    def form_valid(self, form):

        try:
            # save the form into the database
            result = super(ViewNetworkDeviceIpv4Update, self).form_valid(form)

            # get the node and generate all devices
            NetworkGenerateView().generate(
                NetDevice.objects.all(),
                NetManual.objects.first().value
            )

            # and return successfully
            return result

        except Exception as e:        
            form.errors['__all__']   = form.error_class(["%s\n%s" % (str(e), traceback.format_exc())])

            # failure
            return super(ViewNetworkDeviceIpv4Update, self).form_invalid(form)

#
#
#
class NetworkGenerateView:

    def generate(self, devices, manual):

        # for debug only
        if System.WS_WINDOWS == System.name():
            return self.generate_linux_debian(devices, manual)

        if System.WS_LINUX == System.name():
            return self.generate_linux(devices, manual)

        raise Exception("NetworkGenerateView::generate - generator is not implemented for system: '%s'" % System.name())

    def generate_linux(self, devices, manual):

        # debug check
        assert(System.WS_LINUX == System.name())

        # what distrib we have
        distrib = Distrib.name()

        # we only generate network settings for debian/ubuntu for now
        if distrib in [Distrib.WS_DEBIAN9, Distrib.WS_UBUNTU16]:            
            return self.generate_linux_debian(devices, manual)

        raise Exception("NetworkGenerateView::generate_linux - generator is not implemented for distrib: '%s'" % Distrib.name())
    
    def generate_linux_debian_manual(self, manual):

        # construct file names
        cur_file = os.path.join(Paths.etc_dir(), "node", "etc_network_interfaces.manual")
        bak_file = cur_file + ".bak"
        new_file = cur_file + ".new"

        # clear the environment
        if os.path.exists(bak_file):
            os.unlink(bak_file)
        if os.path.exists(new_file):
            os.unlink(new_file)

        # always generate manual file (even if manual is empty)
        t = loader.get_template("node/network/etc_network_interfaces.manual")
        m = manual.replace("\r\n", "\n")
        c = {"manual": m }

        # the contents
        contents = t.render(c)

        # write data into new file
        with open(new_file, "w") as fout:
            fout.write(contents)
            fout.flush()

        # move files around
        if os.path.exists(cur_file):
        	shutil.move(cur_file, bak_file)
        shutil.move(new_file, cur_file)

    def generate_linux_debian(self, devices, manual):

        # generate manual settings (always)
        self.generate_linux_debian_manual(manual)

    	# generate all interfaces
        contents = ""
        for device in devices:

            t = loader.get_template("node/network/etc_network_interface")
            c = {"device": device}

            contents += t.render(c)

        # generate final file
        t = loader.get_template("node/network/etc_network_interfaces")
        c = {"contents" : contents, "manual" : manual }

        # this is what needs to be written to /etc/network/interfaces
        data = t.render(c)
        
        # and generate it
        DebianNetworkSettingsGenerator().generate(data)

#
#
#
class ViewNetworkDeviceIpv6Update(SuccessMessageMixin, generic.edit.UpdateView):

    model           = NetDevice
    template_name   = "node/network/device_form_ipv6.html"
    fields          = ['ip6_config', 'ip6_address', 'ip6_subnet', 'ip6_gateway', 'ip6_dns_srv1', 'ip6_dns_srv2', 'ip6_dns_search']
    success_message = "need_reboot"
    
    def get_success_url(self):
        return reverse_lazy('node:ViewNetworkDeviceIpv6Update', kwargs = {'pk' : self.kwargs['pk'] })

    def get_context_data(self, **kwargs):
        context = super(ViewNetworkDeviceIpv6Update, self).get_context_data(**kwargs)
        context['device_dump'] = NetDeviceDumper().dump_device(self.object.name)
        return context

    def form_valid(self, form):

        try:
            # save the form into the database
            result = super(ViewNetworkDeviceIpv6Update, self).form_valid(form)

            # get the node and generate all devices
            NetworkGenerateView().generate(
                NetDevice.objects.all(),
                NetManual.objects.first().value
            )

            # and return successfully
            return result

        except Exception as e:        
            form.errors['__all__']   = form.error_class(["%s\n%s" % (str(e), traceback.format_exc())])

            # failure
            return super(ViewNetworkDeviceIpv6Update, self).form_invalid(form)
    