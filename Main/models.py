from django.db import models

class ImageBloodTest(models.Model):
    information = models.CharField(max_length=100, default='Amir')
    image = models.ImageField(upload_to='images', null=True)


 