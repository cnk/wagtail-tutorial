# Local parameters file so we don't have to set environment variabls
from .dev import *   # noqa
import dj_database_url

# Override settings here
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
