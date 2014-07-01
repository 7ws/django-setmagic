from django.db import models


class Group(models.Model):
    label = models.CharField(max_length=40)

    def __str__(self):
        return self.label


class Setting(models.Model):
    group = models.ForeignKey('Group')
    name = models.CharField(max_length=20, unique=True)
    label = models.CharField(max_length=40)
    help_text = models.CharField(max_length=140)
    current_value = models.TextField()

    def __str__(self):
        return '{name} ({label} - {group})'.format(
            name=self.name,
            label=self.label,
            group=self.group.label,
        )
