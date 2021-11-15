from django.db import models

# Create your models here.

class Article(models.Model):

    title = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='article/', null=True)