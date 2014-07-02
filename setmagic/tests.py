from django.test import SimpleTestCase, override_settings

from setmagic import settings
from setmagic.models import Setting


test_schema = [
    ('Test group', [
        dict(
            name='SETTING1',
            label='Setting 1',
            help_text='Help text for setting 1'),
    ]),
]


@override_settings(SETMAGIC_SCHEMA=test_schema)
class GetSetSettingsTestCase(SimpleTestCase):

    def test_set_setting(self):
        new_value = 'value1'
        settings.SETTING1 = new_value

        # Check from the settings wrapper
        self.assertEqual(settings.SETTING1, new_value)

        # Check directly from database
        self.assertTrue(Setting.objects.exists())
        db_object = Setting.objects.get(name='SETTING1')
        self.assertEqual(db_object.current_value, new_value)
