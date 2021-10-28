# /bin/bash

python manage.py dumpdata \
  --natural-foreign \
  --natural-primary \
  --format yaml \
  --indent 4 \
  --output multisite.yml \
  --exclude auth.permission \
  auth wagtailcore wagtailimages wagtaildocs
