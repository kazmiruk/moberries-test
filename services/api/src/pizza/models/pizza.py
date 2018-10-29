from django.db import models


class Pizza(models.Model):
    db_table = 'pizza'

    name = models.CharField(max_length=200, unique=True)

    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.name
