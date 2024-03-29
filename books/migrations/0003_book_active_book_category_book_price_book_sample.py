# Generated by Django 4.0.3 on 2022-05-12 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_book_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='price',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='sample',
            field=models.CharField(default='1', max_length=255),
        ),
    ]