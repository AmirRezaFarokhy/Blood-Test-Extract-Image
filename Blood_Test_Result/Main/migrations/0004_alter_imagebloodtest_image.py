# Generated by Django 4.1.1 on 2023-07-14 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0003_imagebloodtest_information'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagebloodtest',
            name='image',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]
