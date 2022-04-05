# Generated by Django 4.0.3 on 2022-04-04 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_remove_tag_point'),
        ('points', '0003_remove_point_rtl'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='point',
            name='tags',
            field=models.ManyToManyField(through='points.TagPoint', to='tags.tag'),
        ),
        migrations.AddField(
            model_name='tagpoint',
            name='point',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='points', to='points.point'),
        ),
        migrations.AddField(
            model_name='tagpoint',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='tags.tag'),
        ),
    ]
