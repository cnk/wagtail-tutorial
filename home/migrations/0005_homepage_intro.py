# Generated by Django 3.1.6 on 2021-03-03 16:03

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_stream_field_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='intro',
            field=wagtail.fields.RichTextField(blank=True),
        ),
    ]
