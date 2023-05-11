from django.db import models
from ckeditor.fields import RichTextField
from tinymce.models import HTMLField

class Blog(models.Model):
    title = models.CharField(max_length=250)
    date = models.DateTimeField()
    description = HTMLField(blank=True,null=True)
    urls=models.CharField(max_length=500,blank=True,null=True)
    comments=models.CharField(max_length=500,blank=True,null=True)
     # for displaying project name in admin page
    def __str__(self):
        return self.title
