from django.db import models
from chapters.models import Chapter
from auth.models import User

class Point(models.Model):
    chapter = models.ForeignKey(Chapter, related_name="points", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="points", on_delete=models.CASCADE)
    type = models.CharField(blank=True, null=True, max_length=255)
    title = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    image = models.FileField(blank=True, null=True, upload_to="images/%Y/%m/%d")
    voice = models.FileField(blank=True, null=True, upload_to="voices/%Y/%m/%d")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return self.user.phone + " | " + self.type

