from django.db import models


class Setting(models.Model):
    name = models.CharField(max_length=40, unique=True)
    label = models.CharField(max_length=60)
    help_text = models.TextField()
    current_value = models.CharField(max_length=100, null=True)

    class Meta:
        app_label = 'setmagic'

    def __str__(self):
        return '{name} ({label})'.format(
            name=self.name,
            label=self.label,
        )
