# -*- coding: utf-8 -*-
from django import template
from django.conf import settings

from django_cackle.utils import get_sso_auth

register = template.Library()


@register.inclusion_tag('cackle/widget.html', takes_context=True)
def cackle_widget(context, channel=None):
    if 'user' in context:
        user = context['user']
    elif 'request' in context:
        user = context['request'].user
    else:
        user = None

    if getattr(settings, 'CACKLE_SSO_AUTH', False) and user:
        sso_auth = get_sso_auth(user)
    else:
        sso_auth = None

    return {
        'cackle_site': settings.CACKLE_SITE,
        'cackle_channel': channel,
        'cackle_jquery_off': getattr(settings, 'CACKLE_JQUERY_OFF', False),
        'cackle_no_style': getattr(settings, 'CACKLE_NO_STYLE', False),
        'cackle_locale': getattr(settings, 'CACKLE_LOCALE', None),
        'cackle_providers': getattr(settings, 'CACKLE_PROVIDERS', None),
        'cackle_size': getattr(settings, 'CACKLE_SIZE', None),
        'cackle_avatar_size': getattr(settings, 'CACKLE_AVATAR_SIZE', None),
        'cackle_text_size': getattr(settings, 'CACKLE_TEXT_SIZE', None),
        'cackle_sso_auth': sso_auth,
    }


@register.inclusion_tag('cackle/last_reply_widget.html')
def cackle_last_reply_widget():
    return {
        'cackle_site': settings.CACKLE_SITE,
        'cackle_jquery_off': getattr(settings, 'CACKLE_JQUERY_OFF', False),
        'cackle_size': getattr(settings, 'CACKLE_SIZE', None),
        'cackle_avatar_size': getattr(settings, 'CACKLE_AVATAR_SIZE', None),
        'cackle_text_size': getattr(settings, 'CACKLE_TEXT_SIZE', None),
    }


@register.inclusion_tag('cackle/reply_count_widget.html')
def cackle_reply_count_widget():
    return {
        'cackle_site': settings.CACKLE_SITE,
        'cackle_jquery_off': getattr(settings, 'CACKLE_JQUERY_OFF', False),
    }
