from django.contrib.auth.models import User
from django.test import TestCase
from .models import ExpenseDataModel


# Create your tests here.


class ExpenseModelTest(TestCase):

    def setUp(self) -> None:
        user1 = User.objects.create_user(first_name="name1", last_name="name2", email="name1@gmail.com",
                                 password="1234", username="name1")
        ExpenseDataModel.objects.create(
            expense_category="dfasfsfadfadfadfadsfadfadfadsfadfadfadsfadfaadsfasdfadfadsfadsfadfadsfadfadfdsafadfsadfadfasfadsfasdfadsfadsf",
            expense_amount=11.3, user=user1, expense_date="2024-08-02", expense_description="test_description")

    def test_category_input_length(self):
        expense_record = ExpenseDataModel.objects.get(expense_amount="11.3")
        expense_category_length = len(expense_record.expense_category)
        self.assertLessEqual(expense_category_length, 100)

    def test_description_input_length(self):
        expense_record = ExpenseDataModel.objects.get(expense_amount="11.3")
        expense_category_length = len(expense_record.expense_description)
        self.assertLessEqual(expense_category_length, 50)

    def test_amount_input_length(self):
        expense_record = ExpenseDataModel.objects.get(expense_amount="11.3")
        expense_category_length = len(expense_record.expense_amount)
        self.assertLessEqual(expense_category_length, 5)

    def test_date_input_length(self):
        expense_record = ExpenseDataModel.objects.get(expense_amount="11.3")
        expense_category_length = len(expense_record.expense_date)
        self.assertLessEqual(expense_category_length, 10)
