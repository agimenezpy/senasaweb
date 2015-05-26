# -*- coding: iso-8859-1 -*-
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

CONFIG_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CONFIG_DIR)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Alberto Gimenez', 'alberto.gimenez@pykoder.com'),
    ('Hugo Astigarra', 'hugo.astigarraga@senasa.gov.py'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'senasaweb',
        'USER': 'senasaweb',
        'PASSWORD': 'sen4dmin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Asuncion'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-py'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(ROOT_DIR, "public")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(CONFIG_DIR, "static"),
    ('dojo-media', os.path.join(ROOT_DIR, "dojango", "dojo-media")),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '6st8r-lf=fv0i6t&amp;!ihwoy_0-25&amp;zuf=ygb%i0m61ro38jetsl'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'dojango.middleware.DojoCollector',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'senasaweb.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'senasaweb.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(ROOT_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.gis',
    'dojango',
    'grappelli',
    'parametros',
    'seguridad',
    'producto',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'fileerr': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filters': ['require_debug_false'],
            'filename': '/var/log/httpd/senasaweb_error.log',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['fileerr'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
LIST_PER_PAGE = 15

if os.name == "nt":
    # SPATIALITE_LIBRARY_PATH = ?
    OSGEO_DIR = os.path.join(os.environ["USERPROFILE"], "Applications", "OSGeo4W", "bin")
    os.putenv("PATH", os.environ["PATH"] + ";" + OSGEO_DIR)
    GDAL_LIBRARY_PATH = os.path.join(OSGEO_DIR, "gdal18.dll")
    GEOS_LIBRARY_PATH = os.path.join(OSGEO_DIR, "geos_c.dll")
    WMS_SERVICE = "http://www.senasa.gov.py/gisobras/wms"
    CONTEXT = ""
    CACHE_DIR = os.path.join(ROOT_DIR, "cache")
    CACHE_TIMEOUT = 5
    LOGGING["handlers"]["fileerr"]["filename"] = "error.log"
else:
    SESSION_ENGINE = "django.contrib.sessions.backends.file"
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
    CONTEXT = "/gisobras"
    WMS_SERVICE = "/wms"
    CACHE_DIR = '/var/tmp/django_cache'
    CACHE_TIMEOUT = 3600

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': CACHE_DIR,
        'TIMEOUT': CACHE_TIMEOUT
        }
}

# DOJANGO
DOJANGO_DOJO_PROFILE = "local_release"
DOJANGO_DOJO_VERSION = "1.7.3"
DOJANGO_DOJO_THEME = "claro"
DOJANGO_DOJO_MEDIA_URL = 'dojo-media'
STATIC_URL = CONTEXT + STATIC_URL
DOJANGO_BASE_MEDIA_URL = STATIC_URL + DOJANGO_DOJO_MEDIA_URL

ADMIN_REORDER = (
    ("Producto", ("Obras", "Contactos")),
    ("Parametros", ("Departamentos", "Distritos", "Localidades", u"Proyectos de inversión", "Grupos de obras")),
    ("Auth", ("Usuarios", "Grupos"))
)

HITOS = (
    (u"Promoción Social y Diseño", 30),
    (u"Perforación del Pozo y Prueba de Bombeo", 40),
    (u"Sistema de Tanque con Caseta y Red Domiciliaria", 30)
)

DOWNLOAD_DIR = os.path.join(STATIC_ROOT, "descargas")
TILE_MAP = "agimenez.map-eb2q2546"  # mapbox.mapbox-light
UI_THEME = 'smoothness'