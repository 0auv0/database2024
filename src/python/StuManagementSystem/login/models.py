from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(primary_key=True,max_length=50)
    password = models.CharField(max_length=50)
    type = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'user'