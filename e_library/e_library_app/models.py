import os.path

from django.db import models

# Create your models here.


class RegisterModel(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)


class CategoryChoices(models.TextChoices):
    Education = "Education"
    Fiction = "Fiction"
    Science = "Science"


class AddBookModel(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField()
    pages = models.IntegerField()
    pdf = models.FileField(null=True, blank=True)
    category = models.CharField(max_length=100, choices=CategoryChoices.choices)
    contributed_by = models.CharField(max_length=100, null=True, blank=True)

    def filename(self):
        return os.path.basename(self.pdf.path)


