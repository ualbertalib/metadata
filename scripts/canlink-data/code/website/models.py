from django.db import models
from django.contrib.auth.models import User, Group

class Institution_code(models.Model):
    name = models.CharField(max_length=255, blank=True)
    skey = models.CharField(max_length=15,  default='skey',)

class Documents(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='./MARC')
    name = models.CharField(max_length=255, blank=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_format = models.CharField(max_length=5, default='.mrc',)
    file_type = models.CharField(max_length=15,  default='MARC Data',)

class CSV_Documents(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='./CSV')
    name = models.CharField(max_length=255, blank=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_format = models.CharField(max_length=5, default='.csv',)
    file_type = models.CharField(max_length=15,  default='CSV Data',)

class RDF_Documents(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='./RDF')
    name = models.CharField(max_length=255, blank=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_format = models.CharField(max_length=5, default='.csv',)
    file_type = models.CharField(max_length=15,  default='CSV Data',)

class Processing(models.Model):
    description = models.CharField(max_length=355, blank=True)
    name = models.CharField(max_length=355, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=False)
    file_format = models.CharField(max_length=5,default='.xml')
    file_type = models.CharField(max_length=155,default='BIBFRAME Data')
    start_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='not started')
    class Meta:
        unique_together = ["name", "uploaded_at", "file_type", "description"]

class P_progress(models.Model):
    pid = models.ForeignKey(Processing, on_delete=models.CASCADE)
    stage = models.CharField(max_length=255, default="MARC_to_MARC-XML")
    num_of_rec = models.CharField(max_length=25, default="1")
    M_to_B_index = models.CharField(max_length=25, default="0")
    rdf_index = models.CharField(max_length=25, default="0")
    master_file = models.CharField(max_length=255, blank=True)


    def as_marc(self):
    	pd = self.pid.id
    	itemType = self.pid.file_type
    	if itemType == 'MARC_Data':
    		return dict(
	        	process_ID=pd,
	            stage=self.stage,
	            M_to_B_index=self.M_to_B_index,
	            rdf_index=self.rdf_index,
	            M_to_B_percent="{0:.2f}".format(round((int(self.M_to_B_index)/int(self.num_of_rec))*100,2)),
	            rdf_percent="{0:.2f}".format(round((int(self.rdf_index)/int(self.num_of_rec))*100,2)))

    def as_rdf(self):
    	pd = self.pid.id
    	itemType = self.pid.file_type
    	if itemType == 'RDF_Data':
    		return dict(
	        	process_ID=pd,
	            stage=self.stage,
    			rdf_index=self.rdf_index,
	            rdf_percent="{0:.2f}".format(round((int(self.rdf_index)/int(self.num_of_rec))*100,2)))
    	
class Progress_archive(models.Model):
	process_ID = models.CharField(max_length=255, blank=True)
	description = models.CharField(max_length=255, blank=True)
	name = models.CharField(max_length=255, blank=True)
	uploaded_at = models.DateTimeField(auto_now_add=False)
	file_format = models.CharField(max_length=5,default='.xml')
	file_type = models.CharField(max_length=155,default='RDF_Data')
	start_time = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=50, default='not started')
	stage = models.CharField(max_length=255, default="starting")
	M_to_B_index = models.CharField(max_length=25, default="100")
	rdf_index = models.CharField(max_length=255, blank=True)
	num_of_rec = models.CharField(max_length=255, blank=True)
	master_file = models.CharField(max_length=255, blank=True)

