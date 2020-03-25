from django import forms
from website.models import Documents, CSV_Documents
from django.contrib.auth.models import User, Group
#import pdb; pdb.set_trace()

class searchForm(forms.Form):
    query = forms.CharField(label='search', max_length=500)

# old file upload methods
class DocumentForm(forms.ModelForm):
	class Meta:
		model = Documents
		fields = ('description', 'document',)

class CSV_DocumentForm(forms.ModelForm):
	class Meta:
		model = CSV_Documents
		fields = ('description', 'document',)

# file upload method supporting multi file uploads
class UploadFileForm(forms.Form):
    Description = forms.CharField(max_length=255)
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))