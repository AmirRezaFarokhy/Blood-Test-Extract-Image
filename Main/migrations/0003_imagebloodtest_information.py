# Generated by Django 4.1.1 on 2023-07-13 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0002_alter_imagebloodtest_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagebloodtest',
            name='information',
            field=models.CharField(default='Amir', max_length=100),
        ),
    ]
