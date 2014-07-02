from itertools import groupby

from django import template

from setmagic import settings


register = template.Library()


@register.assignment_tag
def organize_settings_formset(formset, *args):
    '''
    Group the settings form into groups and re-order them according to what is
    defined at SETMAGIC_SCHEMA.
    '''
    order = [setting.id for setting in settings._backend.settings.values()]
    formset = sorted(formset.forms, key=lambda f: order.index(f.instance.id))
    return [
        (group, list(forms),)
        for group, forms in groupby(formset, lambda f: f.instance.group)]
