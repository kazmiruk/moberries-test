from django.db import models


class Customer(models.Model):
    db_table = 'customer'

    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)

    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False, null=False)

    def __str__(self):
        return '{first_name} {last_name}'.format(first_name=self.first_name,
                                                 last_name=self.last_name).strip()
