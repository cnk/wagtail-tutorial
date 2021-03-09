# Generated by Django 3.1.6 on 2021-03-08 19:55

from django.db import migrations, Error


def copy_docs(from_model, to_model):
    err_count = 0
    for doc in from_model.objects.all():
        new_doc = to_model(
            id=doc.id,
            title=doc.title,
            file=doc.file,
            created_at=doc.created_at,
            uploaded_by_user_id=doc.uploaded_by_user_id,
            collection_id=doc.collection_id,
            file_size=doc.file_size,
            file_hash=doc.file_hash,
        )
        if to_model.__name__ == 'CustomDocument':
            # Fake the required description field when creating a CustomDocument
            new_doc.description = doc.title

        try:
            new_doc.save()
        except Error as e:
            err_count += 1
            print(f'Problem saving document {doc.id} {doc.title}')
            print(e)
    if err_count == 0:
        # Delete database entries in from_model WITHOUT deleting the files.
        print('Since we manually set the ids (do preserve references), you will need to manually reset the id sequence.')
        print('Please run the following manage command and the copy the output into psql. `./manage.py sqlsequencereset home`')
        print(f'Make sure you change your WAGTAILDOCS_DOCUMENT_MODEL setting to "home.{to_model.__name__}"')


def forward(apps, schema_editor):
    Document = apps.get_model('wagtaildocs', 'document')
    CustomDocument = apps.get_model('home', 'customdocument')
    copy_docs(Document, CustomDocument)


def backward(apps, schema_editor):
    Document = apps.get_model('wagtaildocs', 'document')
    CustomDocument = apps.get_model('home', 'customdocument')
    copy_docs(CustomDocument, Document)


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_customdocument'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
