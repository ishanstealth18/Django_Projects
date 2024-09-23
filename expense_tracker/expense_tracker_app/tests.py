from django.test import TestCase
from .models import ExpenseDataModel


# Create your tests here.


class ExpenseModelTest(TestCase):

    def setUp(self) -> None:
        ExpenseDataModel.objects.create(
            expense_category="dfasfsfadfadfadfadsfadfadfadsfadfadfadsfadfaadsfasdfadfadsfadsfadfadsfadfadfdsafadfsadfadfasfadsfasdfadsfadsf",
            expense_amount=11.3, expense_date="2024-08-02", expense_description="test_description")

    def test_category_input_length(self):
        expense_record = ExpenseDataModel.objects.get(expense_amount="11.3")
        expense_category_length = len(expense_record.expense_category)
        self.assertGreaterEqual(expense_category_length, 100)
