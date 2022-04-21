from django.db import models
from points.models import Point
from auth.models import User


class Study(models.Model):
      point = models.ForeignKey(Point, on_delete=models.CASCADE)
      user = models.ForeignKey(User, on_delete=models.CASCADE)
      order = models.CharField(max_length=255, null=True, blank=True)
      level = models.IntegerField(default=1)
      function = models.CharField(max_length=255, default="0")
      created_date = models.DateTimeField(auto_now_add=True)
      updated_date = models.DateTimeField(auto_now=True)

      class Meta:
           verbose_name = "study"
           verbose_name_plural = "studies"
           ordering = ['id']