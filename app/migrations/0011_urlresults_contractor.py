# Generated by Django 4.1.4 on 2022-12-23 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_urlresults_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='urlresults',
            name='contractor',
            field=models.TextField(blank=True, null=True),
        ),
    ]