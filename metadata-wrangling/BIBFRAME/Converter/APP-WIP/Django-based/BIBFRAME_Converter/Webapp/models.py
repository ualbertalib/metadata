from django.db import models

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    OID = models.CharField(max_length=355, blank=True)
    old_id = models.CharField(max_length=25, blank=True)
    name = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_format = models.CharField(max_length=5, default='.xml',)
    file_type = models.CharField(max_length=15,  default='BIBFRAME Data',)

class Marc_Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='./MARC')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_format = models.CharField(max_length=5,  default='.mrc',)
    file_type = models.CharField(max_length=15,  default='MARC Data',)

class Bib_Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='./BIBFRAME')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_format = models.CharField(max_length=5, default='.xml',)
    file_type = models.CharField(max_length=15,  default='BIBFRAME Data',)


class Processing(models.Model):
    description = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
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
    all_names = models.CharField(max_length=25, default="1")
    all_titles = models.CharField(max_length=25, default="1")
    all_MARC = models.CharField(max_length=25, default="1")
    p_names = models.CharField(max_length=25, default="N/A")
    c_names = models.CharField(max_length=25, default="N/A")
    name_index = models.CharField(max_length=25, default="0")
    title_index = models.CharField(max_length=25, default="0")
    M_to_B_index = models.CharField(max_length=25, default="0")
    master_file = models.CharField(max_length=255, blank=True)

    def as_marc(self):
    	pd = self.pid.id
    	itemType = self.pid.file_type
    	if itemType == 'MARC Data':
    		return dict(
	        	process_ID=pd,
	            stage=self.stage,
	            all_titles=self.all_titles, 
	            all_names=self.all_names,
	            p_names=self.p_names,
	            c_names=self.c_names,
	            name_index=self.name_index,
	            title_index=self.title_index,
	            M_to_B_index=self.M_to_B_index,
	            name_percent="{0:.2f}".format(round((int(self.name_index)/int(self.all_names))*100,2)),
	            title_percent="{0:.2f}".format(round((int(self.title_index)/int(self.all_titles))*100,2)),
	            M_to_B_percent="{0:.2f}".format(round((int(self.M_to_B_index)/int(self.all_MARC))*100,2)))
    	

    def as_bib(self):
    	pd = self.pid.id
    	itemType = self.pid.file_type
    	if itemType == 'BIBFRAME Data':
    		return dict(
	        	process_ID=pd,
	            stage=self.stage,
	            all_titles=self.all_titles, 
	            all_names=self.all_names,
	            p_names=self.p_names,
	            c_names=self.c_names,
	            name_index=self.name_index,
	            title_index=self.title_index,
	            name_percent="{0:.2f}".format(round((int(self.name_index)/int(self.all_names))*100,2)),
	            title_percent="{0:.2f}".format(round((int(self.title_index)/int(self.all_titles))*100,2)))
