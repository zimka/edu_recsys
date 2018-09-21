SCORE_LIMITS = (0, 1)


def in_score_limits(score):
    return SCORE_LIMITS[0] <= score <= SCORE_LIMITS[1]


class RawRecommendation:
    """
    "Сырая" рекомендация, которую можно положить в хранилище/сериализовать.
    Любая даваемая рекомендация должна быть представимы в "сыром" виде.
    """
    _SLOTS = ["user", "item", "score", "source", "created"]
    _OPTIONAL_SLOTS = ["created"]

    @classmethod
    def from_kwargs(cls, *, user, item, score, source, created=None):
        if not in_score_limits(score):
            raise ValueError("Score {} not in score limits".format(score))
        instance = cls()
        instance._partial_update(non_update_fields=[], user=user, item=item, score=score, source=source,
                                 created=created)
        return instance

    def to_kwargs(self, item_name=None, drop_none=True):
        if item_name is None:
            mapping = lambda x: x
        else:
            mapping = lambda x: x if x != "item" else item_name
        serial = dict((mapping(k), getattr(self, k)) for k in self._SLOTS)
        if drop_none:
            serial = dict((k, v) for k, v in serial.items() if v is not None)
        return serial

    def _partial_update(self, non_update_fields=_OPTIONAL_SLOTS, **kwargs):
        if non_update_fields is None:
            non_update_fields = tuple()

        for field in self._SLOTS:
            if field in non_update_fields:
                continue
            value = kwargs.get(field)
            setattr(self, field, value)

    def __eq__(self, other):
        if not isinstance(other, RawRecommendation):
            return False
        return self.user == other.user and self.item == other.item

    def __repr__(self):
        return "{}/{}({}): {}".format(self.user, self.item, self.score, self.created)
