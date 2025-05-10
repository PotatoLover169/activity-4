from django.db import models

# Create your models here.

class Product(models.Model):
    # id is automatically created as an AutoField and primary key
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    created_date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
