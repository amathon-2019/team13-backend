import os
import glob
from split_settings.tools import include

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = [
    '*'
]

COMPONENT_DIR = os.path.join(
    BASE_DIR, 'config', 'settings', 'components',
)
COMPONENTS = [
    'components/{component_name}'.format(
        component_name=os.path.basename(component)
    ) for component
    in glob.glob(os.path.join(COMPONENT_DIR, '*.py'))
]

include(*COMPONENTS)
