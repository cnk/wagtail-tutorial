from pathlib import PurePath
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.documents.models import AbstractDocument, Document
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Image, AbstractImage, AbstractRendition

from .blocks import StatsBlock
from .utils import get_collection_path


class CustomImage(AbstractImage):
    photo_credit = models.CharField(max_length=1024, blank=True)
    caption = models.CharField(max_length=1024, blank=True)
    alt = models.CharField(max_length=1024)

    admin_form_fields = Image.admin_form_fields + (
        'photo_credit',
        'caption',
        'alt',
    )

    def get_upload_to(self, filename):
        # This function gets called by wagtail.images.models.get_upload_to().
        original_path = super().get_upload_to(filename)
        # Put the image into a folder named for this image's collection.
        amended_path = PurePath(get_collection_path(self.collection), original_path)
        return str(amended_path)

    @property
    def default_alt_text(self):
        # by default the alt text field (used in rich text insertion) is populated from the title.
        # But we encourage or users to provide an more appropriate alt tag
        return self.alt if self.alt else self.title


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(CustomImage, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )


class CustomDocument(AbstractDocument):
    description = models.CharField(max_length=1024)

    admin_form_fields = Document.admin_form_fields + ('description', )

    def get_upload_to(self, filename):
        # This function gets called by wagtail.documents.models.get_upload_to().
        original_path = super().get_upload_to(filename)
        # Put the document into a folder named for this documents's collection.
        amended_path = PurePath(get_collection_path(self.collection), original_path)
        return str(amended_path)


class HomePage(Page):
    intro = RichTextField(blank=True)
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('hallo_paragraph', blocks.RichTextBlock(editor='legacy')),
        ('image', ImageChooserBlock()),
        ('document', DocumentChooserBlock()),
        ('stats', StatsBlock()),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        StreamFieldPanel('body', classname="full"),
    ]

    api_fields = ['intro', 'body', ]
