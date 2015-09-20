# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext as _

try:
    settings.CACKLE_SITE
except AttributeError:
    raise ImproperlyConfigured(_('You need to specify CACKLE_SITE '
                                 'in you Django settings file.'))
