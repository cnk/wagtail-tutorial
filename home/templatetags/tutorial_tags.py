import uuid
import bleach
from django import template
from django.utils.safestring import mark_safe
from django_bleach.utils import get_bleach_default_options

register = template.Library()


@register.simple_tag(takes_context=True)
def get_unique_id(context):
    """
    Returns the current block's ID if available. Otherwise, generates a unique ID.
    """
    try:
        # If 'block' is in the context, and it has an 'id' attr, use the block's actual ID.
        id_val = context['block'].id
        # During preview, newly added blocks have an ID, but it's blank...
        if not id_val:
            id_val = str(uuid.uuid4())
    except (KeyError, AttributeError):
        # Otherwise, generate a UUID.
        id_val = str(uuid.uuid4())
    return id_val


@register.filter(name='custom_bleach')
def custom_bleach(value, allowed_tags):
    """
    Works just like the 'bleach' template filter, but takes an argument of a comma-separated string of the tags that
    should be allowed through the filter. This list of tags *overrides* the list in the settings, so be thorough.
    """
    # Use the bleach_args built from the settings, but replace the 'tags' arg with the supplied comma-separated list.
    bleach_args = get_bleach_default_options()
    kwargs = dict(**bleach_args)
    kwargs['tags'] = [tag.strip() for tag in allowed_tags.split(',')]
    bleached_value = bleach.clean(value, **kwargs)
    return mark_safe(bleached_value)
