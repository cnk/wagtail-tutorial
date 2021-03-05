from rest_framework.fields import Field
from wagtail.core.templatetags.wagtailcore_tags import richtext


class RenderedRichTextField(Field):
    """
    Runs the richtext filter before including this field's data in the API output.

    Note: this will produce relative for pageslinks
    """

    def to_representation(self, value):
        return richtext(value)
