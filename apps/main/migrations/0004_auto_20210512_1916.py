# Generated by Django 3.2.2 on 2021-05-13 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210512_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='change',
            name='entryDate',
            field=models.DateTimeField(verbose_name='Entry Date'),
        ),
        migrations.AlterField(
            model_name='change',
            name='targetDate',
            field=models.DateTimeField(verbose_name='Target End Date'),
        ),
    ]
