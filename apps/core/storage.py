from django.conf import settings
from django.core.cache import cache


class ComputeStorage:
    """
    Хранилище промежуточных результатов вычислений рекоммендаторов для
    последующего переиспользования.
    """
    # TODO: использовать базу?

    def __init__(self):
        self.timeout = getattr(settings, "STORAGE_COMPUTATION_TIMEOUT", 6*60*60)

    def set(self, key, value):
        return cache.set(key, value, self.timeout)

    def get(self, key):
        return cache.get(key)
