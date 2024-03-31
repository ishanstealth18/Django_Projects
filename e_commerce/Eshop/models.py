from django.db import models

# Create your models here.


class Customers(models.Model):
    username = models.CharField(max_length=155)
    email = models.EmailField()
    password = models.CharField(max_length=155)
    address = models.TextField()
    contact = models.IntegerField()


class Category(models.Model):
    category_name = models.CharField(max_length=155)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.category_name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=155)
    description = models.TextField()
    images = models.ImageField(upload_to='images/')
    price = models.IntegerField()

    #def __str__(self):
        #return self.product_name


class Orders(models.Model):
    quantity = models.IntegerField()
    status = models.CharField(max_length=155)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

