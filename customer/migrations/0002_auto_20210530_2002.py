# Generated by Django 3.1.4 on 2021-05-30 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='name',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contact',
            name='phn',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
    ]
