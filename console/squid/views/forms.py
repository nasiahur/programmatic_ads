#
#
#
from django import forms

#
#
#
from utility.validator import AddressIP, AddressSubnet, AddressRange

#
#
#
class AsciiOnly:

    @staticmethod
    def clean(original_value):

        if len(original_value) > 0:
            
            # check to see the comment does not have unicode symbols
            try:
                value_str = str(original_value)
            except Exception as e:
                raise forms.ValidationError("Value can only contain ASCII symbols. Error '%s'." % (str(e),) )

        return original_value

class Strip:

    @staticmethod
    def clean(original_value):
        return original_value.strip()

class NoWildcards:

    @staticmethod
    def clean(original_value):

        value = original_value        
        if "?" in value or "*" in value:
            raise forms.ValidationError("Domain '%s' cannot be added, becase it contains wildcards which are not supported." % (value) )

        return value


#
#
#
class ItemForm(forms.ModelForm):

    def clean_value(self):
        return Strip.clean(self.cleaned_data['value'])

    def clean_comment(self):
        return AsciiOnly.clean(self.cleaned_data['comment'])
        

#
#
#
class DomainNameForm(ItemForm):

    def clean_value(self):
        
        value = Strip.clean(self.cleaned_data['value'])
        if len(value) < 2:
            raise forms.ValidationError("Domain '%s' cannot be added, becase it is too short." % (value) )

        value = AsciiOnly.clean(value)
        value = NoWildcards.clean(value)
        
        return value

#
#
#
class IpForm(ItemForm):

    def clean_value(self):      

        value = Strip.clean(self.cleaned_data['value'])
        value = AddressIP().check(value)

        return value

#
#
#
class SubnetForm(ItemForm):

    def clean_value(self):

        value = Strip.clean(self.cleaned_data['value'])
        value = AddressSubnet().check(value)

        return value

#
#
#
class RangeForm(ItemForm):

    def clean_value(self):

        value = Strip.clean(self.cleaned_data['value'])
        value = AddressRange().check(value)

        return value

#
#
#
class AdvancedForm(forms.ModelForm):

    def clean_value(self):
        return Strip.clean(self.cleaned_data['value'])

    def clean_comment(self):
        return AsciiOnly.clean(self.cleaned_data['comment'])
