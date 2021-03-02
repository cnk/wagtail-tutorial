from pathlib import PurePath
from django.db import models
from wagtail.core.models import Page
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock

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


class HomePage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('document', DocumentChooserBlock())
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body', classname="full"),
    ]
