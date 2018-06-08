from django import forms

#
# generic form for name <=> value models
#
class ValueCommentForm(forms.ModelForm):
    
    value   = forms.CharField(max_length=512, widget=forms.TextInput(attrs={'size':'50','class':'input-block-level'}))
    comment = forms.CharField(max_length=512, widget=forms.Textarea(attrs={'size':'90', 'rows':'3', 'class':'input-block-level'}),required=False)

    def clean_value(self):
        value = self.cleaned_data['value']
        value = value.strip()
        return value

    def clean_comment(self):
        comment = self.cleaned_data['comment']
        if len(comment) > 0:
        	# check to see the comment does not have unicode symbols
        	try:
        		comment_str = str(comment)
        	except Exception as e:
        		raise forms.ValidationError("Comment can only contain ASCII symbols. Error '%s'." % (str(e),) )
        return comment