from django.conf import settings
import django.conf.global_settings as DEFAULT_SETTINGS


CACHE_TIMEOUT = getattr(settings, "HIERMENU_CACHE_TIMEOUT", 500)

CACHE_KEY_PREFIX = getattr(settings, "HIERMENU_CACHE_KEY_PREFIX", 'M')

UPLOAD_IMG_PATH = getattr(settings, "HIERMENU_UPLOAD_IMG_PATH",
    '/media/img/menu/')

LOCATIONS = getattr(settings, "HIERMENU_LOCATIONS", (
        (1, 'None'),
        (2, 'Top'),
        (3, 'Middle'),
        (4, 'Bottom'),
        (5, 'Left'),
        (6, 'Right'),
        (7, 'Other'),
   )
)

settings.TEMPLATE_CONTEXT_PROCESSORS = getattr(settings,
    "TEMPLATE_CONTEXT_PROCESSORS", DEFAULT_SETTINGS)
settings.TEMPLATE_CONTEXT_PROCESSORS += ('hiermenu.context_processors.menu', )
