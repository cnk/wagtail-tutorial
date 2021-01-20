from pathlib import PurePath
from wagtail.core.models import Site


def get_collection_path(collection):
    """
    We want to store images and documents in separate folders based on their
    path in our collection hierarchy. This makes it much easier to copy the
    assets for a single site (or even section of a site) within our multisite
    installation.

    Given a collection, this method returns the full path into which files
    in that collection should be uploaded. For example, if the 'Jane Roe'
    collection is a child of the 'People' collection, which is a child of
    the 'hss' collection, this method will return 'hss/People/Jane Roe'.

    For consistency, thd folder name for any default site's collection is
    changed to 'root'.

    """
    # Get the name of this Collection and all its ancestors (except the Root
    # collection). They come out in 'path' order by default, which lets us
    # easily build a filesystem path representing the full Collection path.
    collection_names = list(collection.get_ancestors(inclusive=True)
                                      .exclude(name='Root')
                                      .values_list('name', flat=True))
    # Rename the default site's folder to 'root', for consistency
    if collection_names[0] == Site.objects.get(is_default_site=True).hostname:
        collection_names[0] = 'root'
    # Convert the list of names into a filesystem path string.
    collection_path = str(PurePath(*collection_names))

    return collection_path
