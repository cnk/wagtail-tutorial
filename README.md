# Site from the Wagtail tutorial

This repository exists so I can use it while working on developing the
Wagtail CMS platform. When reporting issues, it is often helpful to have a
minimal site that demonstrates the issue.

## Round 1: Image upload issue

This version (b4ddfff) demonstrates an issue I found while we were upgrading our
site to 2.12. The issue first appeared during our transition from Wagtail 2.10
to 2.11 and is only trigged in very specific circumstances.

The error appears when you need to access the collection object before saving an
image. We want to save data from different collections in different folders in
our S3 bucket - and we want the paths named for the collections. On our custom
image model, we overrode `upload_to` as follows:

    def get_upload_to(self, filename):
        # This function gets called by wagtail.images.models.get_upload_to().
        original_path = super().get_upload_to(filename)
        # Put the image into a folder named for this image's collection.
        amended_path = PurePath(get_collection_path(self.collection), original_path)
        return str(amended_path)

    def get_collection_path(collection):
        collection_names = list(collection.get_ancestors(inclusive=True)
                                          .exclude(name='Root')
                                          .values_list('name', flat=True))
        # Rename the default site's folder to 'root', for consistency
        if collection_names[0] == Site.objects.get(is_default_site=True).hostname:
            collection_names[0] = 'root'
        # Convert the list of names into a filesystem path string.
        return str(PurePath(*collection_names))

If the user doing the uploading has access to multiple collections, there is
a collection field in the form to allow you to choose which collection the
image belongs to. However, if the user is only allowed to add/edit items in one
collection, BaseCollectionMemberForm deletes the collection field from the form.

When the user uploads an image using the chooser in the rich text editor, the
upload goes through the `chooser_upload` view in
`wagtail/images/views/chooser.py`. That method calls form.save() and, if there
is only one possible collection, sets the collection id on the image before
calling `super()` to do the rest of the form saving - such as actually saving
the uploaded file to its final location.

When the user uploads an image from the multiple file upload interface you get
when you click the 'Add' button on `/admin/images/` the upload takes a different
path. It uses the class-based views in `wagtail/images/views/multiple.py`. In
our site, we have a required 'alt' field, so the image uploaded from the drag
and drop interface is not valid and gets saved in the UploadedImage model and
the user is presented with the form instantiated by
`CreateFromUploadedImageView`. That form also inherits from
BaseCollectionMemberForm so does not have a collection field if the user only
has access to a single collection. And if we remove our custom `upload_to`
method, the image created by that form ends up the correct collection - even
though print statements inside CreateFromUploadedImageView's save_object method
show the image originally belongs to the root collection and is only moved to
the correct collection when the form is saved.

The problem I am having is that the post method in CreateFromUploadedImageView
(or more technically in the parent class CreateFromUploadView), calls
`save_object` and the `save_object` method in CreateFromUploadedImageView saves
the file BEFORE it saves the form. So the image collection is set to the root
collection at the time the file is first saved - and is only updated to the
correct collection when the full form is saved a few lines later. This [pull
request](https://github.com/wagtail/wagtail/pull/6717) should fix the issue.


## Round 2: Convert RichText to html in API

The default API rendering of a RichTextField is the representation stored in the
database. This means that internal links to pages, images, and documents have
references to their ids, rather than urls to the assets themselves. 

```html
"value": "<p>This is a test. Same url, in a paragraph in a StreamField. If we only customize per field, <a id=\"5\" linktype=\"page\">this</a> will still have linktype in the API output.</p><p>Image inside a RichText field in side a StreamField:</p><embed alt=\"Half a dozen men holding a shiney blump-like balloon by lines\" embedtype=\"image\" format=\"left\" id=\"2\"/>"
```

In some circumstances (such as using the API in a mobile app), this may be what
you want, so you can use the API to retrieve the image. But in many
circumstances, it would be more convenient to have the rich text field rendered
to html - just as you would when displaying the field in a Django template.
Fortunately, we can reuse the richtext filter to do exactly that!

### Converting Individual RichText Fields

On option is to create a custom serializer and use that for individual fields.
Place this code wherever you have other utility methods.

```python
from rest_framework.fields import Field
from wagtail.core.templatetags.wagtailcore_tags import richtext


class RenderedRichTextField(Field):
    def to_representation(self, value):
        return richtext(value)
```

Then in your page models, use this filter when you add RichText fields to the
page's API representation: 

```python
class HomePage(Page):
    intro = RichTextField(blank=True)

    api_fields = [APIField('intro', serializer=RenderedRichTextField())]
```

This works fine BUT it does not allow you to run the richtext filter on RichText
fields that are port of a StreamField. If you don't have any RichText fields
inside StreamFields, this may be fine. But otherwise, the inconsistency will
cause problems. 

