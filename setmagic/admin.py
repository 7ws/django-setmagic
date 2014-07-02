from django.contrib import admin

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

admin.site.register(Setting, SetMagicAdmin)
