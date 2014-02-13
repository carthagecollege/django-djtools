from django import template
from django.conf import settings
from django.core.cache import cache

import urllib2, json, sys

register = template.Library()

class GetContent(template.Node):

    def __init__(self, bits):
        self.varname = bits[2]
        self.ctype=bits[3]
        self.cid=bits[4]

    def __repr__(self):
        return "<LiveWhaleContent>"

    def render(self, context):
        key = "livewhale_%s_%s" % (self.ctype,self.cid)
        if cache.get(key):
            content = cache.get(key)
        else:
            earl = "http://www.carthage.edu/live/%s/%s@JSON" % (self.ctype,self.cid)
            response =  urllib2.urlopen(earl)
            data = response.read()
            content = json.loads(data)
            cache.set(key, content)

        context[self.varname] = content
        return ''

class DoGetLiveWhaleContent:
    """
    {% get_lw_content as variable_name content_type ID %}
    """

    def __init__(self, tag_name):
        self.tag_name = tag_name

    def __call__(self, parser, token):
        bits = token.contents.split()
        if len(bits) < 4:
            raise template.TemplateSyntaxError, "'%s' tag takes three arguments" % bits[0]
        if bits[1] != "as":
            raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'as'" % bits[0]
        return GetContent(bits)

register.tag('get_lw_content', DoGetLiveWhaleContent('get_lw_content'))
