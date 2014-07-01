from setmagic.models import Group, Setting


class GroupProxy(object):

    def __init__(self, label, *lines):
        self.label = label


class SettingProxy(object):

    def __init__(self, group, name, label, help_text):
        self.group = group
        self.name = name
        self.label = label
        self.help_text = help_text


class SettingsBackend(object):

    '''
    A structure to organize the settings scheme and provide a simple API for
    easier access to all registered settings.
    '''

    groups = property(lambda self: self._groups)
    settings = property(lambda self: self._settings)

    def __init__(self, groups):

        self._groups = []
        self._settings = {}

        for group_label, group_settings in groups:
            group = GroupProxy(group_label, group_settings)

            # Build the scheme groups
            self._groups.append(group)

            # Append all settings to the main scheme object
            self._settings.update({
                line['name']: SettingProxy(group, **line)
                for line in group_settings
            })

    def get(self, name):
        try:
            return Setting.objects.get(name=name).current_value
        except Setting.DoesNotExist:
            return

    def set(self, name, value):
        try:
            # The setting already exists, retrieve it
            setting = Setting.objects.get(name=name)

        except Setting.DoesNotExist:
            # Create the group and setting for the first time
            group, new = Group.objects.get_or_create(
                label=self.settings[name].group.label)

            setting, new = Setting.objects.get_or_create(
                group=group,
                name=self.settings[name].name,
                label=self.settings[name].label,
                help_text=self.settings[name].help_text)

        setting.current_value = value
        setting.save()


def setting_line(name, label, help_text=None):
    '''
    A simple helper function make adding optional values to settings tuple
    possible.
    '''
    return locals()
