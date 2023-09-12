
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class SearchQuery(models.Model):
	user = models.ForeignKey(User, on_delete = models.PROTECT)
	query = models.TextField()
	date_created = models.DateTimeField(default = timezone.now)


class SearchResult(models.Model):
	query_id = models.ForeignKey(SearchQuery, on_delete = models.PROTECT)
	tweet = models.TextField()
	polarity = models.FloatField(null=True)
	polarity_text = models.CharField(max_length = 200)
	subjectivity = models.FloatField(null=True)
	subjectivity_text = models.CharField(max_length = 200)