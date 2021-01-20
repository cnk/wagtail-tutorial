from django.db import models
from wagtail.core.models import Page
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


class CustomImage(AbstractImage):
    photo_credit = models.CharField(max_length=1024, blank=True)
    caption = models.CharField(max_length=1024, blank=True)
    alt = models.CharField(max_length=1024)

    admin_form_fields = Image.admin_form_fields + (
        'photo_credit',
        'caption',
        'alt',
    )

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
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]
