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

            for setting_line in group_settings:
                setting, new = Setting.objects.get_or_create(
                    group=group,
                    name=setting_line['name'],
                    label=setting_line['label'],
                    help_text=setting_line['help_text'])
                self._settings[setting.name] = setting

    def get(self, name):
        try:
            return Setting.objects.get(name=name).current_value
        except Setting.DoesNotExist:
            return

    def set(self, name, value):
        Setting.objects.filter(name=name).update(current_value=value)


def setting_line(name, label, help_text=None):
    '''
    A simple helper function make adding optional values to settings tuple
    possible.
    '''
    return locals()
