from django.db import models
from django import forms

from users.models import User


class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=False)
    address = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Recipient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=False)
    address = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=120, unique=True)
    sortno = models.PositiveIntegerField()
    created_date = models.DateField(auto_now_add=True)
    label = models.ImageField(upload_to='static/images/dropcodes', blank=True, default=None)

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_CHOICE = (
        ('available', 'Available'),
        ('shipping', 'Shipping'),
        ('out for delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('returning', 'Returning'),
    )
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    drop = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)
    sport = models.CharField(max_length=120, unique=False, default=None)
    name = models.CharField(max_length=120, unique=False, default=None)
    link = models.CharField(max_length=120, unique=False, default=None)
    sortno = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='available')
    created_date = models.DateField(auto_now_add=True)
    label = models.ImageField(upload_to='static/images/barcodes', blank=True, default=None)

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.CharField(max_length=120, unique=False)

    def __str__(self):
        return self.variant

class VariantOption(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    variant_option = models.CharField(max_length=123, unique=False)

    def __str__(self):
        return self.variant_option

class ProductNumber(models.Model):
    name = models.CharField(max_length=120, unique=True, default=None)
    number = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICE = (
        ('pending', 'Pending'),
        ('decline', 'Decline'),
        ('approved', 'Approved'),
        ('processing', 'Processing'),
        ('complete', 'Complete'),
        ('bulk', 'Bulk'),
    )
    product = models.ManyToManyField(Product, blank=True)
    buyer = models.ForeignKey(Recipient, on_delete=models.CASCADE, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        print(self.buyer.name)
        return self.status


class Delivery(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    courier_name = models.CharField(max_length=120)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.courier_name
