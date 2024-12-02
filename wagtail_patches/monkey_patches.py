# imports for things are going to patch
from wagtail.blocks import RichTextBlock
from wagtail.api.v2.serializers import BaseSerializer

# normal imports needed so we can use the objects or methods in our patches
from wagtail.templatetags.wagtailcore_tags import richtext
from rest_framework.fields import CharField
from wagtail import fields as wagtailcore_fields


def rendered_api_representation(self, value, context=None):
    '''
    The default API representation for RichTextBlocks is the source as stored in the database. But
    we want to render the html as we would in our Django templates so we apply the same filter here.
    '''
    return richtext(value.source)


# Now insert this new method where it will override the original versions
RichTextBlock.get_api_representation = rendered_api_representation


class RichTextField(CharField):
    """
    Create a custom DRF field that runs the richtext filter before adding data in the API output.

    Note: this will produce relative for pageslinks
    """
    def to_representation(self, value):
        return richtext(value)


BaseSerializer.serializer_field_mapping.update({
    wagtailcore_fields.RichTextField: RichTextField,
})
