# Importing all from .dev - which had imported this looks like a circular import
# but we need to do this so we can override existing settings here, e.g. DATABASES
from .dev import *   # noqa

import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Override settings here
