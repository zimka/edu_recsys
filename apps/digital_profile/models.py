from django.db import models
from jsonfield import JSONField

from apps.context.models import Student, IsleContext


class UserDiagnosticsResults(models.Model):
    user = models.ForeignKey(Student, on_delete=models.PROTECT)
    context = models.ForeignKey(IsleContext, on_delete=models.PROTECT)
    data = JSONField()

    class Meta:
        unique_together = ("user", "context")

    def build_profile(self):
        pass

    def __str__(self):
        return "{}({})".format(self.user, self.context)

class DigitalProfile(models.Model):
    user = models.OneToOneField(Student, on_delete=models.PROTECT)
    archetypes = JSONField()
    motivalis = JSONField()
    levels = JSONField()

    def __str__(self):
        return str(self.user)


