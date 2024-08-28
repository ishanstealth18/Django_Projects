from django.db import models

# Create your models here.


class ExpenseDataModel(models.Model):
    expense_category = models.CharField(max_length=100)
    expense_amount = models.IntegerField()
    expense_date = models.DateTimeField()

