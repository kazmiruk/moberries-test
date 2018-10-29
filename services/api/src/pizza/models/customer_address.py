from django.db import models

from pizza.models.customer import Customer


class CustomerAddress(models.Model):
    db_table = 'customer_address'

    customer = models.ForeignKey(Customer, null=False, on_delete=models.CASCADE)
    address = models.TextField(null=False)

    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.address
