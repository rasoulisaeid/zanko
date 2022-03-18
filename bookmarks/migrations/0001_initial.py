# Generated by Django 4.0.3 on 2022-03-18 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('favorites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('favorite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='favorites.favorite')),
            ],
            options={
                'ordering': ['created_date'],
            },
        ),
    ]
