from django.db import models
from django.db.models import Max

# Create your models here.

class Competitor(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True, null=True)
    handle = models.CharField(max_length=100, unique=True)

    def get_current_rating(self):
        maxi = self.rating_set.all().aggregate(Max('date'))['date__max']
        return self.rating_set.get(date=maxi)

    def __repr__(self):
        return str(self.handle)

class Rating(models.Model):
    rating = models.IntegerField()
    date = models.CharField(max_length=30)
    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']