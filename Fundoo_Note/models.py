from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    takeNote = models.TextField()
    archive = models.BooleanField(default=False)
    bin = models.BooleanField(default=False)


class Label(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label_name = models.CharField(max_length=15)

    def __str__(self):
        return self.label_name
