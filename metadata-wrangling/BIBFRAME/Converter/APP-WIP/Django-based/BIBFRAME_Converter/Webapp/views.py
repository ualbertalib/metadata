from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.generic.edit import DeleteView
from Webapp.models import Bib_Document, Marc_Document, Processing, Document
from Webapp.forms import Bib_DocumentForm, Marc_DocumentForm, CheckForm, Del_DocumentForm
import os
from .Code.enrich import main

def index(request):
    bib_documents = Bib_Document.objects.all()
    bib_form = Bib_DocumentForm(request.POST, request.FILES)
    marc_documents = Marc_Document.objects.all()
    marc_form = Marc_DocumentForm(request.POST, request.FILES)
    documents ={}
    for bib in bib_documents:
    	documents[bib.id] = [bib.document, bib.file_type, bib.description, bib.uploaded_at]
    for marc in marc_documents:
    	documents[marc.id] = [marc.document, marc.file_type, marc.description, marc.uploaded_at]
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
    return render(request, 'webapp/index.html', { 'documents': documents, 'marc_documents': marc_documents, 'bib_documents': bib_documents, 'marc_form': marc_form, 'bib_form': bib_form, 'Del_DocumentForm': Del_DocumentForm })

def model_form_upload(request):
    return render(request, 'webapp/model_form_upload.html')

def deleteRecord(request, id =None, format=None):
	print (request)
	print (format)
	folder = 'Webapp/source'
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
	return redirect('deleted')

def deleted(request):
	return render(request, 'webapp/deleted.html')

def processing(request):
	processing_docs = Processing.objects.all()
	form = CheckForm(request.POST or None)
	file_dict = dict(request.POST.lists())
	if 'file_selected' in file_dict.keys():
		for item in file_dict['file_selected']:
			try:
				object = Marc_Document.objects.get(document=item)
			except:
				object = Bib_Document.objects.get(document=item)
			add_process = Processing(description=object.description, 
					name=str(object.document), 
					uploaded_at=object.uploaded_at,
					file_format=object.file_format,
					file_type=object.file_type) 
			try:
				add_process.save()
			except:
				return redirect('processing_duplicate')
				break
	return render(request, 'webapp/processing.html', {'processing_docs': processing_docs})

def processing_duplicate(request):
	return render(request, 'webapp/processing_duplicate.html')

def stop(request, id =None):
	object = Processing.objects.get(id=id)
	object.delete()
	return render(request, 'webapp/stop.html')