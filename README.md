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


## Round 2: Convert RichText to html in APIv2

The default API rendering of a RichTextField is the representation stored in the
database. This means that internal links to pages, images, and documents have
references to their ids, rather than urls to the assets themselves.

```html
"value": "<p>This is a test. Same url, in a paragraph in a StreamField. If we only customize per field, <a id=\"5\" linktype=\"page\">this</a> will still have linktype in the API output.</p><p>Image inside a RichText field in side a StreamField:</p><embed alt=\"Half a dozen men holding a shiney blump-like balloon by lines\" embedtype=\"image\" format=\"left\" id=\"2\"/>"
```

In some circumstances (such as using the API in a mobile app), this may be what
you want, so you can use the API to retrieve the image. But in many
circumstances, it would be more convenient to have the rich text field rendered
to html - just as you get when displaying the field in a Django template.
Fortunately, we can reuse the richtext filter to do exactly that!

### Converting Individual RichText Fields

One option is to create a custom serializer and use that for individual fields.
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
Now the same intro example from above renders as:

```html
"value": "<p>This is a test. Same url, in a paragraph in a StreamField. If we only customize per field, <a href=\"http://localhost/foo\">this</a> will still have linktype in the API output.</p><p>Image inside a RichText field in side a StreamField:</p><img alt=\"Half a dozen men holding a shiney blump-like balloon by lines\" class=\"richtext-image left\" height=\"369\" src=\"/media/images/balloon-tracking-1961.width-500.png\" width=\"498\"/>"
```

This works fine BUT it does not allow you to run the richtext filter on RichText
blocks that are port of a StreamField. If you don't have any RichText blocks
inside StreamFields, this may be fine. But otherwise, the inconsistency will
cause problems.

A better method is probably this second one - which overrides the API
representation of all RichTextFields and RichTextBlocks.

### Converting All RichText Fields

If you want **all** RichTextFields to return rendered HTML, you will need to
customize the representation for RichTextFields and RichTextBlock by overriding
the methods used to serialize their content.

For RichTextBlocks, we need to define a custom version of
`get_api_representation` and reopen the RichTextBlock class to insert this into
it. 

```python
from wagtail.core.blocks import RichTextBlock
from wagtail.core.templatetags.wagtailcore_tags import richtext

def rendered_api_representation(self, value, context=None):
    '''
    The default API representation for RichTextBlocks is the source as stored
    in the database. But we want to render the html as we would in our 
    Django templates so we apply the same filter here.
    '''
    return richtext(value.source)

# Now insert this new method where it will override the original versions
RichTextBlock.get_api_representation = rendered_api_representation
```

When we overrode our individual RichTextFields in the first section, we defined
a `to_representation` method on in our custom class. So the first thing I tried
was assigning `rendered_api_representation` as RichTextField.to_representation -
but nothing happened. Then I looked more closely at the code above - it is
inheriting from `rest_framework.fields.Field` NOT
`wagtail.core.fields.RichTextField`. And in the block, we are running the filter
on `value.source`; but in the custom serializer field, we are running the filter
on `value`. 

I am pretty sure we don't want to override `to_representation` for all DRF
Fields, so we need to figure out what serializer Field subclass Wagtail is using
when serializing RichTextFields. Looking at `wagtail.api.serializers`, I don't
see a specific RichTextField. But I do see some interesting looking setup code
in the `BaseSerializer` class. Wagtail's BaseSerializer inherits from DRF's
ModelSerializer and the first thing it does is update a
`serializer_field_mapping`. I wonder if we could slip our custom render class in
there? Looks like yes.

```python
# imports for things are going to patch
from wagtail.api.v2.serializers import BaseSerializer

# normal imports needed so we can use the objects or methods in our patches
from wagtail.core.templatetags.wagtailcore_tags import richtext
from rest_framework.fields import CharField
from wagtail.core import fields as wagtailcore_fields


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
```

You will notice that I changed some of my naming to more closely match the
serializer fields I see in `wagtail/api/v2/serializers.py`. I am not a big fan
of giving the model classes and the serializer class the same name because I
think it makes it hard to tell which kind of object you have. You will see in
the mapping, we needed to specify the module name for the model class to avoid
it clashing with the serializer field class of the same name. But the matching
names is how DRF does things so it makes our code more consistent if we do too.

I also decided to inherit from the CharField serializer because Wagtail stores
rich text fields in a TextField and the [default
mapping](https://github.com/encode/django-rest-framework/blob/d635bc9c71b6cf84d137a68610ae2e628f8b62b3/rest_framework/serializers.py#L876)
for model TextFields is to use the CharField serializer. With both the overrides
in place, all our rich text fields are converted to HTML in our pages api.

*Please note*: the urls we get from the richtext filter are absolute paths
*without* the domain name: `src=\"/media/images/BoxerDay.width-800.jpg\"`. That
is consistent with the download url we get from the images API (below). But I am
not exactly sure how this plays out if your API consumer is on a different
domain than the CMS. It is probably a good thing but implies that your API
client will need asset routes using the same sort of path structure as the CMS.

```json
{
    "id": 1,
    "meta": {
        "type": "home.CustomImage",
        "detail_url": "http://localhost:8787/api/v2/images/1/",
        "tags": [],
        "download_url": "/media/original_images/BoxerDay.jpg"
    },
    "title": "BoxerDay",
    "width": 1242,
    "height": 792
}
```
