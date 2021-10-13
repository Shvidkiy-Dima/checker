import os

configuration = os.environ.get('SETTINGS_CONFIGURATION', 'develop')

if configuration == 'develop':
    from .develop import *

if configuration == 'prod':
    from .prod import *

else:
    from .base import *