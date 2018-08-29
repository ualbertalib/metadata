from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.generic.edit import DeleteView
from Webapp.models import Document
from Webapp.forms import DocumentForm
import os


def index(request):
    documents = Document.objects.all()
    form = DocumentForm(request.POST, request.FILES)
    folder = 'Webapp/source'
    if not os.path.exists(folder):
        os.makedirs(folder)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'webapp/index.html', { 'documents': documents, 'form': form })

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
        	print (content._size)
        	if content._size > settings.MAX_UPLOAD_SIZE:
        		raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
        	else:
        		form.save()
        return redirect('index')
    else:
        form = DocumentForm()
    return render(request, 'webapp/model_form_upload.html', {
        'form': form
        })

def deleteRecord(request,id =None):
    object = Document.objects.get(id=id)
    file = str(object.document)
    object.delete()
    folder = 'Webapp/source'
    file_path = os.path.join(folder, file)
    print (file_path)
    try:
        if os.path.isfile(file_path):
        	os.unlink(file_path)
    except Exception as e:
        print(e)
    return redirect('deleted')

def deleted(request):
	return render(request, 'webapp/deleted.html')

