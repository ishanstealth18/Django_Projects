from django.contrib.auth.models import User
from django.test import TestCase
from .models import ExpenseDataModel
from django.test import Client
from django.urls import reverse
from django.test.utils import setup_test_environment


# Create your tests here.


class ExpenseModelTest(TestCase):

    def setUp(self) -> None:

        user1 = User.objects.create_user(first_name="name1", last_name="name2", email="name1@gmail.com",
                                 password="1234", username="name1")
        ExpenseDataModel.objects.create(
            expense_category="dfasfsfadfadfadfadsfadfadfadsfadfadfadsfadfaadsfasdfadfadsfadsfadfadsfadfadfdsafadfsadfadfasfadsfas",
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
        expense_category_length = len(str(expense_record.expense_date))
        self.assertLessEqual(expense_category_length, 10)

    def test_url_response_code(self):
        client = Client()
        register_page_response = client.get(reverse("register_page"))
        #home_page_response = client.get(reverse("home_page"))
        view_expense_page_response = client.get(reverse("view_expense_page"))
        edit_expense_page_response = client.get(reverse("edit_expense_page"))
        update_expense_page_response = client.get(reverse("update_expense_page"))
        delete_expense_page_response = client.get(reverse("delete_expense_page"))
        view_chart_page_response = client.get(reverse("view_chart_page"))
        self.assertEquals(200, register_page_response.status_code)
        #self.assertEquals(200, home_page_response.status_code)
        self.assertEquals(200, view_expense_page_response.status_code)
        self.assertEquals(200, edit_expense_page_response.status_code)
        self.assertEquals(200, update_expense_page_response.status_code)
        self.assertEquals(200, delete_expense_page_response.status_code)
        self.assertEquals(200, view_chart_page_response.status_code)

    def test_user_login_credentials(self):
        c = Client()
        login_response = c.login(username="name1", password=1234)
        self.assertEquals(True, login_response)

