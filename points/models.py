from django.db import models
from subjects.models import Subject

class Point(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    explains = models.TextField(blank=True, null=True)
    importants = models.TextField(blank=True, null=True)
    regulars = models.TextField(blank=True, null=True)
    reminders = models.TextField(blank=True, null=True)
    attentions = models.TextField(blank=True, null=True)
    quesitons = models.TextField(blank=True, null=True)
    image = models.FileField(blank=True, null=True, upload_to="images/%Y/%m/%d")
    voice = models.FileField(blank=True, null=True, upload_to="voices/%Y/%m/%d")
    rtl = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return self.subject.name

