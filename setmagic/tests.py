from itertools import groupby
import random

from django.core.urlresolvers import reverse
from django.test import SimpleTestCase, TransactionTestCase, override_settings
from lxml import html

from setmagic import settings
from setmagic.models import Setting


test_schema = [
    ('Test group 1', [
        dict(
            name='SETTING1',
            label='Setting 1',
            help_text='Help text for setting 1'),
        dict(
            name='SETTING2',
            label='Setting 2',
            help_text='Help text for setting 2'),
    ]),
    ('Test group 2', [
        dict(
            name='SETTING3',
            label='Setting 3',
            help_text='Help text for setting 3'),
        dict(
            name='SETTING4',
            label='Setting 4',
            help_text='Help text for setting 4'),
        dict(
            name='SETTING5',
            label='Setting 5',
            help_text='Help text for setting 5'),
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


class SettingsAdminTestCase(TransactionTestCase):

    fixtures = ['setmagic_test_users']

    def test_changelist_order(self):
        self.client.login(username='root', password='123')
        url = reverse('admin:setmagic_setting_changelist')

        # Check a randomized the settings order many times
        for i in range(10):
            new_schema = test_schema[:]
            random.shuffle(new_schema)
            for g, settings_lines in new_schema:
                random.shuffle(settings_lines)

            with override_settings(SETMAGIC_SCHEMA=new_schema):
                expected = [
                    (group.label, [setting.name for setting in settings_],)
                    for group, settings_ in groupby(
                        settings._backend.settings.values(),
                        lambda s: s.group)]

                dom = html.fromstring(self.client.get(url).content)
                rendered = [
                    (
                        section.xpath('h2/text()')[0],
                        section.xpath('*//*[@data-setting-name]/text()'),
                    )
                    for section in dom.xpath('//*[@data-settings-formset]')]

                self.assertEqual(expected, rendered)
