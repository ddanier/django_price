from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

DEFAULT_CURRENCY = getattr(settings, 'PRICE_DEFAULT_CURRENCY', None)

