from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.generic.edit import DeleteView
from Webapp.models import Bib_Document, Marc_Document, Processing, Document
from Webapp.forms import Bib_DocumentForm, Marc_DocumentForm, CheckForm, Del_DocumentForm
import os
from .Code.enrich import main
from .Code.Utils import PrintException

def index(request):
	docs = Document.objects.all()
	bib_documents = Bib_Document.objects.all()
	bib_form = Bib_DocumentForm(request.POST, request.FILES)
	marc_documents = Marc_Document.objects.all()
	marc_form = Marc_DocumentForm(request.POST, request.FILES)
	checksum="thisisadummyobjectonlynumber123456"
	if docs.filter(OID=checksum).exists():
		pass
	else:
		adddummy = Document(description="a dummy object", 
		    		OID=checksum, 
		    		old_id= 123,
		    		name="dumy_object", 
		    		file_type="dummy data",
		    		uploaded_at="2014-09-04 23:34:40.834676",
		    		file_format=".dum")
		adddummy.save()
	for bib in bib_documents:
		checksum = str(bib.id)+str("___")+str(bib.document)+str("___")+str(bib.uploaded_at)
		if docs.filter(OID=checksum).exists():
			pass
		else:
			addbib = Document(description=bib.description, 
	    		OID=checksum, 
	    		old_id= bib.id,
	    		name=bib.document, 
	    		file_type=bib.file_type,
	    		uploaded_at=bib.uploaded_at,
	    		file_format=bib.file_format)
			addbib.save()
	for mrc in marc_documents:
		checksum = str(mrc.id)+str("___")+str(mrc.document)+str("___")+str(mrc.uploaded_at)
		if docs.filter(OID=checksum).exists():
			pass
		else:
			addDoc = Document(description=mrc.description, 
	    		OID=checksum, 
	    		old_id=mrc.id,
	    		name=mrc.document, 
	    		file_type=mrc.file_type,
	    		uploaded_at=mrc.uploaded_at,
	    		file_format=mrc.file_format)
			addDoc.save()
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
	return render(request, 'webapp/index.html', { 'docs': docs, 'marc_form': marc_form, 'bib_form': bib_form})

def model_form_upload(request):
    return render(request, 'webapp/model_form_upload.html')

def deleteRecord(request, id =None, format=None, old_id=None):
	print (request)
	print (format)
	folder = 'Webapp/source'
	doc = Document.objects.get(id=id)
	doc.delete()
	if format == ".xml":
		object = Bib_Document.objects.get(id=old_id)
		file = str(object.document)
		object.delete()
		file_path = os.path.join(folder, file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception as e:
			print(e)
	if format == ".mrc":
		object = Marc_Document.objects.get(id=old_id)
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

def processingQueue(request):
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
					file_type=object.file_type,
					status="started")
			try:
				add_process.save()
			except:
				return redirect('processing_duplicate')
				break
	return render(request, 'webapp/processing.html', {'processing_docs': processing_docs})

def processing(request, processing_docs):
	print ("1")
	return render(request, 'webapp/processing.html', {'processing_docs': processing_docs})

def processing_duplicate(request):
	return render(request, 'webapp/processing_duplicate.html')

def stop(request, id =None):
	object = Processing.objects.get(id=id)
	object.delete()
	return render(request, 'webapp/stop.html')