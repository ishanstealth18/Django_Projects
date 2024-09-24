from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class ExpenseDataModel(models.Model):
    expense_category = models.CharField(max_length=100)
    expense_description = models.CharField(max_length=50, null=True, blank=True)
    expense_amount = models.CharField(max_length=5)
    expense_date = models.DateField(max_length=10)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)

