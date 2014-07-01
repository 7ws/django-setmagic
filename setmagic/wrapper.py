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

    def __getattr__(self, name):
        self._initialize()
        return self._backend.get(name)

    def __setattr__(self, name, value):
        self._initialize()
        self._backend.set(name, value)
