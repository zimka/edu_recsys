from django.db import models
from jsonfield import JSONField

from apps.context.models import Student, IsleContext
from .task import build_profile_async


class UserDiagnosticsResults(models.Model):
    user = models.ForeignKey(Student, on_delete=models.PROTECT)
    context = models.ForeignKey(IsleContext, on_delete=models.PROTECT)
    data = JSONField()

    class Meta:
        unique_together = ("user", "context")

    def build_profile(self):
        build_profile_async.delay(self)

    def __str__(self):
        return "{}({})".format(self.user, self.context)


class DigitalProfile(models.Model):
    user = models.OneToOneField(Student, on_delete=models.PROTECT, related_name="digital_profile")
    archetypes = JSONField()
    motivalis = JSONField()
    levels = JSONField()

    def get_serial(self):
        return {
            "user": self.user.uid,
            "archetypes": self.archetypes,
            "motivalis": self.motivalis,
            "levels": self.levels
        }

    def __str__(self):
        return str(self.user)

