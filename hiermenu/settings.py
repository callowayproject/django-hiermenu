from django.conf import settings

CACHE_TIMEOUT = getattr(settings, "HIERMENU_CACHE_TIMEOUT", 500)

CACHE_KEY_PREFIX = getattr(settings, "HIERMENU_CACHE_KEY_PREFIX", 'M')

UPLOAD_IMG_PATH = getattr(settings, "HIERMENU_UPLOAD_IMG_PATH", '/media/img/menu/')

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