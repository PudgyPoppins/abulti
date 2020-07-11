from django.db import models
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.

STATUS = (
	(0,"Draft"),
	(1,"Publish")
)

class Post(models.Model):
	title = models.CharField(max_length=200, unique=True)
	slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
	content = models.TextField()
	created_on = models.DateTimeField(default=timezone.now)
	status = models.IntegerField(choices=STATUS, default=0)

	class Meta:
		ordering = ['-created_on']

	def __str__(self): 
		return self.title


	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		super(Post, self).save(*args, **kwargs)