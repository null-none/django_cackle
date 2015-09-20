# -*- coding: utf-8 -*-
import simplejson
import hashlib
from base64 import b64encode
import time

from django.conf import settings
from django.contrib.auth.models import SiteProfileNotAvailable
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


def _get_user_name(user):
    if user.first_name and user.last_name:
        name = u'{first} {last}'.format(first=user.first_name,
                                        last=user.last_name)
    elif user.first_name:
        name = user.first_name
    elif user.last_name:
        name = user.last_name
    else:
        name = user.email.split(u'@')[0]

    return name


def _get_profile(user):
    if user.is_anonymous():
        return None

    try:
        return user.get_profile()
    except (SiteProfileNotAvailable, ObjectDoesNotExist):
        return None


def get_sso_auth(user):
    profile = _get_profile(user)
    user_info = {
        'id': user.pk,
        'email': user.email,
    }

    if hasattr(profile, 'cackle_avatar'):
        user_info['avatar'] = profile.cackle_avatar

    if hasattr(profile, 'cackle_www'):
        user_info['www'] = profile.cackle_www

    if hasattr(profile, 'cackle_name'):
        user_info['name'] = profile.cackle_name
    else:
        user_info['name'] = _get_user_name(user)

    site_api_key = settings.CACKLE_SITE_API_KEY
    user_data = b64encode(simplejson.dumps(user_info))
    timestamp = int(time.mktime(timezone.now().timetuple()))
    sign = hashlib.md5(u'{user_data}{site_api_key}{timestamp}'.format(
        user_data=user_data, site_api_key=site_api_key, timestamp=timestamp)) \
        .hexdigest()

    return u'{user_data} {md5_sign} {timestamp}'.format(
        user_data=user_data, md5_sign=sign, timestamp=timestamp)


def get_sso_logout():
    user_info = {}

    site_api_key = settings.CACKLE_SITE_API_KEY
    user_data = b64encode(simplejson.dumps(user_info))
    timestamp = int(time.mktime(timezone.now().timetuple()))
    sign = hashlib.md5(u'{user_data}{site_api_key}{timestamp}'.format(
        user_data=user_data, site_api_key=site_api_key, timestamp=timestamp)) \
        .hexdigest()

    return u'{user_data} {md5_sign} {timestamp}'.format(
        user_data=user_data, md5_sign=sign, timestamp=timestamp)
