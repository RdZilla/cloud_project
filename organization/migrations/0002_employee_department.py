# Generated by Django 5.1.2 on 2024-12-22 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='department',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Отдел'),
        ),
    ]
