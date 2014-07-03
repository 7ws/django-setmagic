from django import forms
from django.contrib import admin

from setmagic import settings
from setmagic.models import Setting


_denied = lambda *args: False


class SetMagicAdmin(admin.ModelAdmin):
    list_display = 'label', 'current_value',
    list_editable = 'current_value',
    list_display_links = None

    has_add_permission = _denied
    has_delete_permission = _denied

    # Make all fields read-only at the change form
    def get_readonly_fields(self, *args, **kwargs):
        return self.opts.get_all_field_names()

    def changelist_view(self, *args, **kwargs):
        settings._initialize()
        return super(SetMagicAdmin, self).changelist_view(*args, **kwargs)

    def get_changelist_formset(self, request, **kwargs):
        class Form(forms.ModelForm):

            class Meta:
                fields = self.list_display

            def __init__(self, *args, **kwargs):
                super(Form, self).__init__(*args, **kwargs)

                # Do nothing for empty forms
                if not self.instance.pk:
                    return

                # Set a custom field
                custom_field = settings.defs[self.instance.name].get('field')
                if custom_field:
                    self.fields['current_value'] = custom_field

        return forms.modelformset_factory(Setting, form=Form, extra=0)

admin.site.register(Setting, SetMagicAdmin)
