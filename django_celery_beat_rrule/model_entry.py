from celery import schedules
from django_celery_beat.clockedschedule import clocked
from django_celery_beat.models import (
    CrontabSchedule,
    IntervalSchedule,
    SolarSchedule,
    ClockedSchedule,
    PeriodicTask,
)
from .models import RrulePeriodicTask
from .rruleschedule import rruleschedule
from django_celery_beat.schedulers import ModelEntry

from django_celery_beat_rrule.models import RruleSchedule
from django_celery_beat_rrule.rruleschedule import rruleschedule


class RruleModelEntry(ModelEntry):
    model_schedules = (
        (schedules.crontab, CrontabSchedule, "crontab"),
        (schedules.schedule, IntervalSchedule, "interval"),
        (schedules.solar, SolarSchedule, "solar"),
        (clocked, ClockedSchedule, "clocked"),
        (rruleschedule, RruleSchedule, "rrule"),
    )

    @classmethod
    def from_entry(cls, name, app=None, **entry):
        if isinstance(entry.get('schedule', None), rruleschedule):
            obj, created = RrulePeriodicTask._default_manager.update_or_create(
                name=name, defaults=cls._unpack_fields(**entry),
            )
            return cls(obj, app=app)
        return ModelEntry.from_entry(name, app=app, **entry)
