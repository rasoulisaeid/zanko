# Generated by Django 4.0.3 on 2022-03-12 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subjects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('explains', models.TextField(blank=True, null=True)),
                ('importants', models.TextField(blank=True, null=True)),
                ('regulars', models.TextField(blank=True, null=True)),
                ('reminders', models.TextField(blank=True, null=True)),
                ('attentions', models.TextField(blank=True, null=True)),
                ('quesitons', models.TextField(blank=True, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='images/%Y/%m/%d')),
                ('voice', models.FileField(blank=True, null=True, upload_to='voices/%Y/%m/%d')),
                ('rtl', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subjects.subject')),
            ],
            options={
                'ordering': ['created_date'],
            },
        ),
    ]