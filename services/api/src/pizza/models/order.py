from django.db import models

from pizza.enums import PIZZA_SIZES
from pizza.models.customer import Customer
from pizza.models.customer_address import CustomerAddress
from pizza.models.pizza import Pizza


class Order(models.Model):
    db_table = 'order'

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    customer_address = models.ForeignKey(CustomerAddress, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)

    size = models.SmallIntegerField(null=False, choices=PIZZA_SIZES)

    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False, null=False)

    class Meta:
        indexes = (
            models.Index(fields=['customer', 'is_deleted', '-id']),
        )
        ordering = ('-id', )
