from django.contrib.auth.models import User
from django.test import TestCase
from .models import ExpenseDataModel
from django.test import Client
from django.urls import reverse
from django.test.utils import setup_test_environment
import names


# Create your tests here.


class ExpenseModelTest(TestCase):
    databases = {"default"}

    def setUp(self) -> None:
        global data_found
        global user1
        self.user1 = User.objects.create_user(first_name="name1", last_name="name2", email="name1@gmail.com",
                                              password="1234", username="name1")
        ExpenseDataModel.objects.create(
            expense_category="dfasfsfadfadfadfadsfadfadfadsfadfadfadsfadfaadsfasdfadfadsfadsfadfadsfadfadfdsafadfsadfadfasfadsfas",
            expense_amount=11.3, user=self.user1, expense_date="2024-08-02", expense_description="test_description")

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
        # home_page_response = client.get(reverse("home_page"))
        view_expense_page_response = client.get(reverse("view_expense_page"))
        edit_expense_page_response = client.get(reverse("edit_expense_page"))
        update_expense_page_response = client.get(reverse("update_expense_page"))
        delete_expense_page_response = client.get(reverse("delete_expense_page"))
        view_chart_page_response = client.get(reverse("view_chart_page"))
        self.assertEquals(200, register_page_response.status_code)
        # self.assertEquals(200, home_page_response.status_code)
        self.assertEquals(200, view_expense_page_response.status_code)
        self.assertEquals(200, edit_expense_page_response.status_code)
        self.assertEquals(200, update_expense_page_response.status_code)
        self.assertEquals(200, delete_expense_page_response.status_code)
        self.assertEquals(200, view_chart_page_response.status_code)

    def test_user_login_credentials(self):
        c = Client()
        login_response = c.login(username="name1", password=1234)
        base_url = reverse('base_page')
        # Validate redirect using follow attribute
        response = c.post(base_url, {'login_username': "name1", 'login_password': 1234}, follow=True)
        self.assertEquals(True, login_response)
        # Redirect validation
        self.assertRedirects(response, "home.html", status_code=302, target_status_code=200)

    def test_register_page(self):
        # calling test Client()
        c = Client(enforce_csrf_checks=False)
        record_count = 3
        response = None
        # Assign details for 3 different users and posting it to URL or sending a request
        for record in range(record_count):
            names.get_full_name(gender='male')
            random_fname = names.get_first_name()
            random_lname = names.get_last_name()
            random_email = random_fname + "@gmail.com"
            response = c.post("/register.html", {"register_firstname": random_fname, "register_lastname": random_lname,
                                                 "register_email": random_email, "register_password": 12343})

        self.assertEquals(200, response.status_code)
        # Check if 3 users + 1 in Setup function are created in database
        self.assertEquals(User.objects.count(), record_count + 1)

    def test_create_expense_record(self):
        c = Client()
        # Getting url of Home Page via page name from urls.py
        home_url = reverse("home_page")
        # Logging in using test Client function
        c.login(username="name1", password=1234)
        # Sending request to home url with data as input. This will invoke home_page function in Views.py file and test
        # the logic
        response = c.post(home_url, {"input_category": "Grocery", "input_description": "Walmart", "input_amount": 23.55,
                                     "input_date": "2024-09-11", "user": self.user1})
        self.assertEquals(200, response.status_code)
        # Checking if total records in Expense model
        self.assertEquals(ExpenseDataModel.objects.count(), 2)

    def test_view_expense_data(self):
        c = Client()
        # Getting view expense page url using name
        view_expense_url = reverse("view_expense_page")
        home_url = reverse("home_page")
        # Logging in using test Client function
        c.login(username="name1", password=1234)
        # Sending request to home url with data as input. This will invoke home_page function in Views.py file and test
        # the logic.
        # Basically it will create fake records in test database of Expense model
        c.post(home_url, {"input_category": "Grocery", "input_description": "Walmart", "input_amount": 23.55,
                                     "input_date": "2024-09-11", "user": self.user1})
        c.post(home_url, {"input_category": "EMI", "input_description": "Costco", "input_amount": 23.56,
                                      "input_date": "2024-09-12", "user": self.user1})
        # Sending request to view expense page with date range as input data
        response = c.post(view_expense_url, {"expense_from_date": "2024-08-01", "expense_to_date": "2024-11-03"})
        # Getting all the records using test client response context, 'all_data' is the one sent in context from
        # views.py
        records = response.context["all_data"]
        self.assertEquals(len(records), 3)

    # Unit test for validating Update expense
    def test_edit_expense(self):
        c = Client()
        edit_expense_url = reverse("edit_expense_page")
        home_url = reverse("home_page")
        # Logging in using test Client function
        c.login(username="name1", password=1234)
        # Sending request to home url with data as input. This will invoke home_page function in Views.py file and test
        # the logic.
        # Basically it will create fake records in test database of Expense model
        c.post(home_url, {"input_category": "Grocery", "input_description": "Walmart", "input_amount": 23.55,
                                     "input_date": "2024-09-11", "user": self.user1})
        c.post(home_url, {"input_category": "EMI", "input_description": "Costco", "input_amount": 23.56,
                                      "input_date": "2024-09-12", "user": self.user1})
        # Getting all the ids from test Expense data model
        record_id_list = ExpenseDataModel.objects.all().values_list('id')
        # Sending a request using POST to Edit Expense page with input data, 'submit_updated_expense_details' is name
        # of the button
        # which is clicked to edit the expense record. This will go to 'edit_expense' function and test the logic
        expense_edit_response = c.post(edit_expense_url,
                                       {"submit_updated_expense_details": True, "record_id": 2,
                                        "expense_category": "Restaurant", "expense_description": "Pukka Desi",
                                        "expense_amount": 111.52, "expense_date": "2024-09-09"})
        print(expense_edit_response.request)
        # Checking no of Expense records in Expense Model after updating 1 record
        self.assertEquals(len(record_id_list), 3)
        # Getting and printing the updated record
        updated_record = list(ExpenseDataModel.objects.all().values())
        print(updated_record)
        # Logic to check if the record is updated by searching the updated data in the records
        data_found = False
        for data in updated_record:
            if data["expense_description"] == "Pukka Desi":
                data_found = True
                break
        self.assertEquals(data_found, True)

    def test_delete_expense(self):
        c = Client()
        edit_expense_url = reverse("edit_expense_page")
        home_url = reverse("home_page")
        # Logging in using test Client function
        c.login(username="name1", password=1234)
        # Sending request to home url with data as input. This will invoke home_page function in Views.py file and test
        # the logic.
        # Basically it will create fake records in test database of Expense model
        c.post(home_url, {"input_category": "Grocery", "input_description": "Walmart", "input_amount": 23.55,
                                     "input_date": "2024-09-11", "user": self.user1})
        c.post(home_url, {"input_category": "EMI", "input_description": "Costco", "input_amount": 23.56,
                                      "input_date": "2024-09-12", "user": self.user1})
        # Sending POST request to delete the records, 'delete_expense_details' is the name of the button for deleting
        # the record in edit_expense.html
        c.post(edit_expense_url, {"delete_expense_details": True, "delete_record_id": 2})
        c.post(edit_expense_url, {"delete_expense_details": True, "delete_record_id": 3})
        # Getting the number of records after sending request to delete the expense records
        record_id_list = ExpenseDataModel.objects.all().values_list('id')
        self.assertEquals(len(record_id_list), 1)

    def test_expense_total_amount(self):
        c = Client()
        view_chart_url = reverse("view_chart_page")
        home_url = reverse("home_page")
        # Logging in using test Client function
        c.login(username="name1", password=1234)
        # Sending request to home url with data as input. This will invoke home_page function in Views.py file and test
        # the logic.
        # Basically it will create fake records in test database of Expense model
        c.post(home_url, {"input_category": "Grocery", "input_description": "Walmart", "input_amount": 23.55,
                          "input_date": "2024-09-11", "user": self.user1})
        c.post(home_url, {"input_category": "Grocery", "input_description": "Costco", "input_amount": 23.56,
                          "input_date": "2024-09-12", "user": self.user1})
        # Sending POST request to View Chart page to get records for the input date range
        response = c.post(view_chart_url, {"from_date": "2024-08-01", "to_date": "2024-11-03"})
        # Getting the total from the logic in view_chart function in Views.py. This will test the logic to calculate the
        # total for each expense category
        total_expense_amount = response.context["total"]
        # Validate the total for 2 records of Grocery expense category in this function on line 192 and 194
        self.assertEquals(total_expense_amount["Grocery"], 47.11)

