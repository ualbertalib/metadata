from django import forms

from Webapp.models import Marc_Document, Bib_Document

class Marc_DocumentForm(forms.ModelForm):
	class Meta:
		model = Marc_Document
		fields = ('description', 'document',)

class Bib_DocumentForm(forms.ModelForm):
	class Meta:
		model = Bib_Document
		fields = ('description', 'document',)

class Del_DocumentForm(forms.ModelForm):
	class Meta:
		model = Bib_Document
		fields = ('description', 'document',)

class CheckForm(forms.Form):
    checked = forms.BooleanField(required=False)