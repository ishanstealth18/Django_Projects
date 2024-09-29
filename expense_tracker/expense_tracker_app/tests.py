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
        user2 = User.objects.create_user(first_name="name4", last_name="name5", email="name7@gmail.com",
                                         password="1234", username="name7")
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

    def test_login_page(self):
        c = Client(enforce_csrf_checks=False)
        response = c.post("/register.html", {"register_firstname": "abc", "register_lastname": "def", "register_email": "abc@gmail.com", "register_password": 12343})
        response1 = c.post("/register.html",
                          {"register_firstname": "xxx", "register_lastname": "yyy", "register_email": "aaa@gmail.com",
                           "register_password": 12343})
        self.assertEquals(200, response.status_code)
        self.assertEquals(200, response1.status_code)
        self.assertEquals(User.objects.count(), 5)



