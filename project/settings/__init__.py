import os

if os.getenv('develop'):
    from .develop import *

else:
    from .base import *