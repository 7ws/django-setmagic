from collections import OrderedDict
import sys

from django.conf import settings
from setmagic.backend import SettingsBackend


class SettingsWrapper(object):

    '''
    A magic wrapper for all registered settings
    '''

    def __init__(self):
        super(SettingsWrapper, self).__setattr__('_backend', None)

    def _initialize(self):
        '''
        Lazily load the backend
        '''
        if self._backend:
            return

        super(SettingsWrapper, self).__setattr__(
            '_backend', SettingsBackend(settings.SETMAGIC_SCHEMA))

        # Cache all setting defs into a single dict
        super(SettingsWrapper, self).__setattr__('defs', OrderedDict())
        for group_label, setting_defs in settings.SETMAGIC_SCHEMA:
            for setting_def in setting_defs:
                setting_def['group_label'] = group_label
                self.defs[setting_def['name']] = setting_def

    def __getattr__(self, name):
        self._initialize()
        return self._backend.get(name)

    def __setattr__(self, name, value):
        self._initialize()
        self._backend.set(name, value)
