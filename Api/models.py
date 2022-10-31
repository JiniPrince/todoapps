from email.policy import default
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Todo(models.Model):
    task_name=models.CharField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    created_data=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.task_name