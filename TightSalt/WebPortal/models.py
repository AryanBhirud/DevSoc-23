from django.db import models

class student(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.IntegerField()
    regno = models.CharField(max_length=9)
    password = models.CharField(max_length=100, default='0')
    save_img = models.ImageField(upload_to='static/images')
