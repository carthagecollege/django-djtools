from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter

from djtools.utils.encryption import do_crypt

import urllib2, os.path, base64

register = template.Library()

@register.filter()
@template.defaultfilters.stringfilter
def format_phone(value):
    """
    takes a value with separated by dashes and returns it in the format:
    (415) 963-4949
    """
    phone = value.split("-")
    try:
        phone = "(%s) %s-%s" % (phone[0],phone[1],phone[2])
    except:
        if value:
            phone = "(%s) %s-%s" % (value[:3],value[3:6],value[6:10])
        else:
            phone = value
    return phone
format_phone.is_safe=True
format_phone.needs_autoescape = False

@register.filter()
@template.defaultfilters.stringfilter
def get_novell_username(value):
    novell = value.split("@")
    try:
        novell = novell[0]
    except:
        novell = ''
    return novell

@register.filter()
@template.defaultfilters.stringfilter
def verify_earl(value):
    try:
        resp = urllib2.urlopen(value)
        return True
    except urllib2.URLError, e:
        return False

@register.filter()
@template.defaultfilters.stringfilter
def encrypt(value):
    try:
        encoded = do_crypt(value, "encrypt").replace("/","\/")
    except:
        encoded = ''
    return encoded

