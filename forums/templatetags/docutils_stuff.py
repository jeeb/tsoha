from django import template
from django.template.defaultfilters import stringfilter

from docutils.core import publish_parts

register = template.Library()

# Defaults for any docutils_conversion
docutils_defaults = {
    'file_insertion_enabled': 0,
    'raw_enabled': 0,
    '_disable_config': 1,
}

# Our local thingy for calling docutils
@register.filter
@stringfilter
def rst_to_html(string):
    return publish_parts(string, writer_name='html', settings_overrides=docutils_defaults)['fragment']
