from django.db import models


# Create your models here.

class Product(models.Model):
    STOCK_LEVEL_CHOICES = [
        ('in_stock', 'In Stock'),
        ('low_stock', 'Low Stock'),
        ('out_of_stock', 'Out of Stock'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    quantity = models.IntegerField(default=0)
    stock_level = models.CharField(max_length=20, choices=STOCK_LEVEL_CHOICES, default='in_stock')

    def __str__(self):
        return self.name
