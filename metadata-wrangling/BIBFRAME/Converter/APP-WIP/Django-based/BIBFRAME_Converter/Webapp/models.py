from django.db import models

class Marc_Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='./MARC')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_format = models.CharField(max_length=5,  default='MARC',)

class Bib_Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='./BIBFRAME')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_format = models.CharField(max_length=5, default='XML',)
