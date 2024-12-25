#  This file is part of wger Workout Manager <https://github.com/wger-project>.
#  Copyright (C) 2013 - 2021 wger Team
#
#  wger Workout Manager is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  wger Workout Manager is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Standard Library
import datetime
from collections import Counter
from decimal import Decimal
from typing import List

# Django
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# wger
from wger.exercises.models import Exercise
from wger.manager.dataclasses import (
    GroupedLogData,
    RoutineLogData,
    WorkoutDayData,
)
from wger.utils.cache import CacheKeyMapper


class Routine(models.Model):
    """
    Model for a routine
    """

    # objects = WorkoutManager()
    # templates = WorkoutTemplateManager()
    # both = WorkoutAndTemplateManager()

    class Meta:
        ordering = [
            '-created',
        ]

    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        verbose_name=_('Name'),
        max_length=50,
        blank=True,
    )

    description = models.TextField(
        verbose_name=_('Description'),
        max_length=1000,
        blank=True,
    )

    # TODO: remove the auto_now_add during migration so we can set this to a custom
    #       value and then set it back to auto_now_add
    created = models.DateTimeField(
        _('Creation date'),
        auto_now_add=True,
    )

    start = models.DateField(
        _('Start date'),
    )

    end = models.DateField(
        _('End date'),
    )

    is_template = models.BooleanField(
        verbose_name=_('Workout template'),
        help_text=_(
            'Marking a workout as a template will freeze it and allow you to make copies of it'
        ),
        default=False,
        null=False,
    )

    is_public = models.BooleanField(
        verbose_name=_('Public template'),
        help_text=_('A public template is available to other users'),
        default=False,
        null=False,
    )

    fit_in_week = models.BooleanField(
        default=False,
    )

    def get_absolute_url(self):
        """
        Returns the canonical URL to view a workout
        """
        return reverse(
            'manager:routine:view',
            kwargs={'pk': self.id},
        )

    def __str__(self):
        """
        Return a more human-readable representation
        """
        if self.name:
            return self.name
        else:
            return f'Routine {self.id} - {self.created}'

    def get_owner_object(self):
        """
        Returns the object that has owner information
        """
        return self

    def clean(self):
        """Validations"""

        if self.end and self.start and self.start > self.end:
            raise ValidationError(_('The start time cannot be after the end time.'))

    @property
    def day_sequence(self):
        """
        Return a sequence of days.
        """
        return list(self.days.all())

    @property
    def label_dict(self) -> dict[datetime.date, str]:
        out = {}
        labels = self.labels.all()

        for label in labels:
            for i in range(label.start_offset, label.end_offset + 1):
                out[self.start + datetime.timedelta(days=i)] = label.label

        return out

    @property
    def date_sequence(self) -> List[WorkoutDayData]:
        """
        Return a list with specific dates and routine days

        If a day needs logs to continue it will be repeated until the user adds one.
        """

        cache_key = CacheKeyMapper.get_routine_date_sequence_key(self.id)
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        labels = self.label_dict
        delta = datetime.timedelta(days=1)
        current_date = self.start
        days = list(self.days.all())
        current_day = self.days.first()
        nr_days = self.days.count()
        counter = Counter()
        skip_til_date = None

        out = []

        if current_day is None:
            return out

        index = 0
        while current_date <= self.end:
            # Fill all days till the end of the week with empty workout days
            if skip_til_date:
                out.append(
                    WorkoutDayData(
                        iteration=counter[current_day],
                        date=current_date,
                        day=None,
                        label=labels.get(current_date),
                    )
                )
                current_date += delta
                if current_date == skip_til_date:
                    skip_til_date = None
                continue

            counter[current_day] += 1
            index = (index + 1) % nr_days

            # If we reach the end of the available days, check whether we want to fill up the
            # week with empty days, unless the routine already consists of 7 training days
            if nr_days % 7 != 0 and index == 0 and self.fit_in_week:
                days_til_monday = 7 - current_date.weekday()
                skip_til_date = current_date + datetime.timedelta(days=days_til_monday)

            out.append(
                WorkoutDayData(
                    iteration=counter[current_day],
                    date=current_date,
                    day=current_day,
                    label=labels.get(current_date),
                )
            )

            if current_day.can_proceed(current_date):
                current_day = days[index]

            current_date += delta

        cache.set(cache_key, out, settings.WGER_SETTINGS['ROUTINE_CACHE_TTL'])
        return out

    def data_for_day(self, date=None) -> WorkoutDayData | None:
        """
        Return the WorkoutDayData for the specified day. If no date is given, return
        the results for "today"
        """
        if date is None:
            date = datetime.date.today()

        for data in self.date_sequence:
            if data.date == date:
                return data

        return None

    def data_for_iteration(self, iteration: int | None = None) -> List[WorkoutDayData]:
        """
        Return the WorkoutDayData entries for the specified iteration. If no iteration
        is given, return the results for the one for "today". If none could be found,
        return the data for the first one
        """

        if iteration is None:
            for data in self.date_sequence:
                if data.date == datetime.date.today():
                    iteration = data.iteration
                    break

        if iteration is None:
            iteration = 1

        out = []

        for data in self.date_sequence:
            if data.iteration == iteration:
                out.append(data)

        return out

    def logs_display(self, date: datetime.date = None):
        """
        Returns all the logs for this routine, grouped by the session
        """
        out = []

        qs = self.sessions.all()
        if date:
            qs = qs.filter(date=date)

        for session in qs:
            out.append({'session': session, 'logs': session.logs.all()})

        return out

    def calculate_log_statistics(self) -> RoutineLogData:
        """
        Calculates various statistics for the routine based on the logged workouts.

        Returns:
            RoutineLogData: An object containing the calculated statistics.
        """
        # wger
        from wger.manager.helpers import brzycki_intensity

        result = RoutineLogData()
        intensity_counter = GroupedLogData()

        def update_grouped_log_data(
            entry: GroupedLogData,
            date: datetime.date,
            week_nr: int,
            iter: int,
            exercise: Exercise,
            value: Decimal | int,
        ):
            """
            Updates grouped log data

            This method just adds the value to the corresponding entries
            """
            muscles = exercise.muscles.all()

            entry.daily[date].exercises[exercise.id] += value
            entry.weekly[week_nr].exercises[exercise.id] += value
            entry.iteration[iter].exercises[exercise.id] += value
            entry.mesocycle.exercises[exercise.id] += value

            entry.daily[date].total += value
            entry.weekly[week_nr].total += value
            entry.iteration[iter].total += value
            entry.mesocycle.total += value

            for muscle in muscles:
                pk = muscle.id

                entry.daily[date].muscle[pk] += value
                entry.weekly[week_number].muscle[pk] += value
                entry.iteration[iter].muscle[pk] += value
                entry.mesocycle.muscle[pk] += value

        def safe_divide(numerator, denominator):
            return numerator / denominator if denominator != 0 else numerator

        def calculate_average_intensity(result: GroupedLogData, counters: GroupedLogData) -> None:
            result.mesocycle.total = safe_divide(
                result.mesocycle.total,
                counters.mesocycle.total,
            )

            for key in result.daily.keys():
                result.daily[key].total = safe_divide(
                    result.daily[key].total,
                    counters.daily[key].total,
                )
                result.daily[key].upper_body = safe_divide(
                    result.daily[key].upper_body,
                    counters.daily[key].upper_body,
                )
                result.daily[key].lower_body = safe_divide(
                    result.daily[key].lower_body,
                    counters.daily[key].lower_body,
                )

                for j in result.daily[key].muscle.keys():
                    result.daily[key].muscle[j] = safe_divide(
                        result.daily[key].muscle[j],
                        counters.daily[key].muscle[j],
                    )

                for j in result.daily[key].exercises.keys():
                    result.daily[key].exercises[j] = safe_divide(
                        result.daily[key].exercises[j],
                        counters.daily[key].exercises[j],
                    )

            for key in result.weekly.keys():
                result.weekly[key].total = safe_divide(
                    result.weekly[key].total,
                    counters.weekly[key].total,
                )
                result.weekly[key].upper_body = safe_divide(
                    result.weekly[key].upper_body,
                    counters.weekly[key].upper_body,
                )
                result.weekly[key].lower_body = safe_divide(
                    result.weekly[key].lower_body,
                    counters.weekly[key].lower_body,
                )

                for j in result.weekly[key].muscle.keys():
                    result.weekly[key].muscle[j] = safe_divide(
                        result.weekly[key].muscle[j],
                        counters.weekly[key].muscle[j],
                    )

                for j in result.weekly[key].exercises.keys():
                    result.weekly[key].exercises[j] = safe_divide(
                        result.weekly[key].exercises[j],
                        counters.weekly[key].exercises[j],
                    )

            for key in result.iteration.keys():
                result.iteration[key].total = safe_divide(
                    result.iteration[key].total,
                    counters.iteration[key].total,
                )
                result.iteration[key].upper_body = safe_divide(
                    result.iteration[key].upper_body,
                    counters.iteration[key].upper_body,
                )
                result.iteration[key].lower_body = safe_divide(
                    result.iteration[key].lower_body,
                    counters.iteration[key].lower_body,
                )

                for j in result.iteration[key].muscle.keys():
                    result.iteration[key].muscle[j] = safe_divide(
                        result.iteration[key].muscle[j],
                        counters.iteration[key].muscle[j],
                    )

                for j in result.iteration[key].exercises.keys():
                    result.iteration[key].exercises[j] = safe_divide(
                        result.iteration[key].exercises[j],
                        counters.iteration[key].exercises[j],
                    )

        # Iterate over each workout session associated with the routine
        for session in self.sessions.all():
            session_date = session.date
            week_number = session_date.isocalendar().week

            # TODO: filter for lb
            for log in session.logs.kg().reps():
                exercise = log.exercise
                weight = log.weight
                reps = log.reps
                iteration = log.iteration
                exercise_volume = weight * reps

                calculate_intensity = reps is not None and weight is not None
                exercise_intensity = brzycki_intensity(weight, reps)

                update_grouped_log_data(
                    entry=result.volume,
                    iter=iteration,
                    week_nr=week_number,
                    date=session_date,
                    exercise=exercise,
                    value=exercise_volume,
                )
                update_grouped_log_data(
                    entry=result.sets,
                    iter=iteration,
                    week_nr=week_number,
                    date=session_date,
                    exercise=exercise,
                    value=1,
                )

                if calculate_intensity:
                    update_grouped_log_data(
                        entry=intensity_counter,
                        iter=iteration,
                        week_nr=week_number,
                        date=session_date,
                        exercise=exercise,
                        value=1,
                    )

                    update_grouped_log_data(
                        entry=result.intensity,
                        iter=iteration,
                        week_nr=week_number,
                        date=session_date,
                        exercise=exercise,
                        value=exercise_intensity,
                    )

        calculate_average_intensity(result.intensity, intensity_counter)

        return result
