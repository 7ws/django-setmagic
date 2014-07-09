from collections import OrderedDict

from setmagic.models import Setting


class SettingsBackend(object):

    '''
    A structure to organize the settings scheme and provide a simple API for
    easier access to all registered settings.
    '''

    settings = property(lambda self: self._settings)

    def __init__(self, groups):
        '''
        Sync settings schema to both the backend and database
        '''

        self._settings = OrderedDict()

        for group_label, group_settings in groups:
            # Sync settings
            for setting_line in group_settings:
                try:
                    setting = Setting.objects.get(name=setting_line['name'])
                except Setting.DoesNotExist:
                    setting = Setting(name=setting_line['name'])
                setting.__dict__.update(**setting_line)
                setting.save()
                self._settings[setting.name] = setting

    def get(self, name):
        try:
            return Setting.objects.get(name=name).current_value
        except Setting.DoesNotExist:
            return

    def set(self, name, value):
        Setting.objects.filter(name=name).update(current_value=value)
