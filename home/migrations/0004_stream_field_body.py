# Generated by Django 3.1.6 on 2021-03-02 19:24

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.documents.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_custom_image_models'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='full title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('hallo_paragraph', wagtail.blocks.RichTextBlock(editor='legacy')), ('image', wagtail.images.blocks.ImageChooserBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('stats', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=False)), ('title_style', wagtail.blocks.ChoiceBlock(choices=[('h2', 'Heading 2'), ('h3', 'Heading 3'), ('h4', 'Heading 4'), ('h5', 'Heading 5'), ('h6', 'Heading 6 (all uppercase)')], requried=True)), ('title_centered', wagtail.blocks.BooleanBlock(default=False, help_text='Check this box to center the title. Otherwise, it will be left-aligned.', required=False, verbose_name='Center title')), ('stats', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('stat', wagtail.blocks.CharBlock(help_text='The big statistic.', label='Statistic')), ('desc', wagtail.blocks.CharBlock(help_text='The description underneath the big statistic. You may use these tags in this field: &lt;a&gt;, &lt;b&gt;, &lt;br&gt;, &lt;i&gt;, &lt;em&gt;, &lt;strong&gt;, &lt;sup&gt;, &lt;sub&gt;', label='Short Description'))]), label='Statistics'))]))]),
        ),
    ]
