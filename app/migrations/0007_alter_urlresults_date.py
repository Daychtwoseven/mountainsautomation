# Generated by Django 4.1.3 on 2022-12-03 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_urlresults_record_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urlresults',
            name='date',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
