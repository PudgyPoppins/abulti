from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
	pass
	username = models.CharField(max_length=25, unique=True, default="")
	email = models.EmailField(max_length=254, help_text="Enter an email that you have access to", unique=True, default="")
	
	def __str__(self):
		return self.username
