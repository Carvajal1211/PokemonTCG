# Generated by Django 3.2.22 on 2023-10-26 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20231023_0205'),
    ]

    operations = [
        migrations.AddField(
            model_name='precio',
            name='code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='precio',
            name='imagen',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]