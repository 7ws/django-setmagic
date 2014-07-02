from setmagic.models import Group, Setting


class SettingsBackend(object):

    '''
    A structure to organize the settings scheme and provide a simple API for
    easier access to all registered settings.
    '''

    groups = property(lambda self: self._groups)
    settings = property(lambda self: self._settings)

    def __init__(self, groups):
        '''
        Sync settings schema to both the backend and database
        '''

        self._groups = []
        self._settings = {}

        for group_label, group_settings in groups:
            # Sync groups
            group, new = Group.objects.get_or_create(label=group_label)
            self._groups.append(group)

            # Sync settings
            for setting_line in group_settings:
                try:
                    setting = Setting.objects.get(name=setting_line['name'])
                except Setting.DoesNotExist:
                    setting = Setting(name=setting_line['name'])
                setting.__dict__.update(**setting_line)
                setting.group = group
                setting.save()
                self._settings[setting.name] = setting

    def get(self, name):
        try:
            return Setting.objects.get(name=name).current_value
        except Setting.DoesNotExist:
            return

    def set(self, name, value):
        Setting.objects.filter(name=name).update(current_value=value)
