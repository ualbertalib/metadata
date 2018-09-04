from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.generic.edit import DeleteView
from Webapp.models import Bib_Document, Marc_Document, Processing
from Webapp.forms import Bib_DocumentForm, Marc_DocumentForm, CheckForm
import os
from .Code.enrich import main


def index(request):
    bib_documents = Bib_Document.objects.all()
    bib_form = Bib_DocumentForm(request.POST, request.FILES)
    marc_documents = Marc_Document.objects.all()
    marc_form = Marc_DocumentForm(request.POST, request.FILES)
    if len(request.FILES) > 0:
    	uploaded_file = request.FILES['document']
    	filename = uploaded_file.name
    	file_ext = filename[-4:]
    	if file_ext == ".xml":
    		bib_folder = 'Webapp/source/BIBFRAME'
    		if bib_form.is_valid():
    			bib_form.save()
    			return redirect('index')
    	if file_ext == ".mrc":
    		marc_folder = 'Webapp/source/MARC'
    		if marc_form.is_valid():
    			marc_form.save()
    			return redirect('index')
    return render(request, 'webapp/index.html', { 'marc_documents': marc_documents, 'bib_documents': bib_documents, 'marc_form': marc_form, 'bib_form': bib_form })

def model_form_upload(request):
    return render(request, 'webapp/model_form_upload.html')

def deleteRecord(request, id =None, format=None):
	print (request)
	print (format)
	folder = 'Webapp/source'
	if format == "mrc":
		object = Marc_Document.objects.get(id=id)
		file = str(object.document)
		object.delete()
		file_path = os.path.join(folder, file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception as e:
			print(e)
	if format == "bib":
		object = Bib_Document.objects.get(id=id)
		file = str(object.document)
		object.delete()
		file_path = os.path.join(folder, file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception as e:
			print(e)
	return redirect('deleted')

def deleted(request):
	return render(request, 'webapp/deleted.html')

def processing(request):
	files = {}
	bib_documents = Bib_Document.objects.all()
	marc_documents = Marc_Document.objects.all()
	form = CheckForm(request.POST or None)
	file_dict = dict(request.POST.lists())
	for item in file_dict['file_selected']:
		try:
			object = Marc_Document.objects.get(document=item)
		except:
			object = Bib_Document.objects.get(document=item)
		Type = object.file_type
		Desc = object.description
		files[item] = []
		files[item].append(Type)
		files[item].append(Desc)
	return render(request, 'webapp/processing.html', { 'marc_documents': marc_documents, 'bib_documents': bib_documents, 'files': files})

def stop(request, id =None, format=None):
	return render(request, 'webapp/stop.html', { 'marc_documents': marc_documents, 'bib_documents': bib_documents, 'files': files})