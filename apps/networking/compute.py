from django.conf import settings
from apps.context.models import Student
import random


def get_sample(iterable, size):
    pool = tuple(iterable)
    n = len(pool)
    try:
        indices = sorted(random.sample(range(n), size))
    except ValueError:
        indices = range(n)
    t = tuple(pool[i] for i in indices)
    if len(t) == 1:
        return t[0]
    else:
        return t


def get_networking_json(user):
    # Round robin!
    size = getattr(settings,"NETWORKING_RECOMMENDATION_SIZE", 2)
    students = Student.objects.all().exclude(uid=user.uid)
    coffee = {"type": "coffee", "target_ids":list(str(x.uid) for x in get_sample(students, size))}
    discuss = {"type": "discuss", "target_ids":list(str(x.uid) for x in get_sample(students, size))}
    learn = {"type": "learn", "users": [
            {"target_id": str(get_sample(students, 1).uid), "competence": ""}
    ]}
    look = {"type": "look", "target_ids":list(str(x.uid) for x in get_sample(students, size))}
    return {"communication": [coffee, discuss, learn, look]}

