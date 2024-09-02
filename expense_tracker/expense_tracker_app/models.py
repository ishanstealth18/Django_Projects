from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class ExpenseDataModel(models.Model):
    expense_category = models.CharField(max_length=100)
    expense_amount = models.DecimalField(max_digits=20, decimal_places=3)
    expense_date = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)

