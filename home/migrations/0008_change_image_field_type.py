# Generated by Django 3.2.25 on 2024-12-03 04:36

from django.db import migrations
import wagtail.images.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_index_image_filehash_json_homepage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customimage',
            name='file',
            field=wagtail.images.models.WagtailImageField(height_field='height', upload_to=wagtail.images.models.get_upload_to, verbose_name='file', width_field='width'),
        ),
        migrations.AlterField(
            model_name='customrendition',
            name='file',
            field=wagtail.images.models.WagtailImageField(height_field='height', upload_to=wagtail.images.models.get_rendition_upload_to, width_field='width'),
        ),
    ]
