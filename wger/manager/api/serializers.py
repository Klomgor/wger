# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Workout Manager.  If not, see <http://www.gnu.org/licenses/>.


# Third Party
from rest_framework import serializers

# wger
from wger.manager.api.consts import (
    BASE_CONFIG_FIELDS,
    BASE_CONFIG_FILTER_FIELDS,
)
from wger.manager.api.validators import validate_requirements
from wger.manager.models import (
    Day,
    MaxRepsConfig,
    MaxRestConfig,
    MaxRiRConfig,
    MaxSetsConfig,
    MaxWeightConfig,
    RepsConfig,
    RestConfig,
    RiRConfig,
    Routine,
    SetsConfig,
    Slot,
    SlotEntry,
    WeightConfig,
    Workout,
    WorkoutLog,
    WorkoutSession,
)


class RoutineSerializer(serializers.ModelSerializer):
    """
    Routine serializer
    """

    class Meta:
        model = Routine
        fields = (
            'id',
            'name',
            'description',
            'created',
            'start',
            'end',
            'fit_in_week',
        )


class DaySerializer(serializers.ModelSerializer):
    """
    Day serializer
    """

    class Meta:
        model = Day
        fields = (
            'id',
            'routine',
            'order',
            'name',
            'description',
            'is_rest',
            'need_logs_to_advance',
            'type',
            'config',
        )


class BaseConfigSerializer(serializers.ModelSerializer):
    """
    Base Config serializer
    """

    requirements = serializers.JSONField(validators=[validate_requirements])


class WeightConfigSerializer(BaseConfigSerializer):
    """
    Weight Config serializer
    """

    class Meta:
        model = WeightConfig
        fields = BASE_CONFIG_FIELDS


class MaxWeightConfigSerializer(BaseConfigSerializer):
    """
    Max Weight Config serializer
    """

    class Meta:
        model = MaxWeightConfig
        fields = BASE_CONFIG_FIELDS


class RepsConfigSerializer(BaseConfigSerializer):
    """
    Repetition Config serializer
    """

    class Meta:
        model = RepsConfig
        fields = BASE_CONFIG_FIELDS


class MaxRepsConfigSerializer(BaseConfigSerializer):
    """
    Max Repetition Config serializer
    """

    class Meta:
        model = MaxRepsConfig
        fields = BASE_CONFIG_FIELDS


class SetNrConfigSerializer(BaseConfigSerializer):
    """
    Set Nr config serializer
    """

    class Meta:
        model = SetsConfig
        fields = BASE_CONFIG_FIELDS


class MaxSetNrConfigSerializer(BaseConfigSerializer):
    """
    Max Set Nr config serializer
    """

    class Meta:
        model = MaxSetsConfig
        fields = BASE_CONFIG_FIELDS


class RiRConfigSerializer(BaseConfigSerializer):
    """
    RiR Config serializer
    """

    class Meta:
        model = RiRConfig
        fields = BASE_CONFIG_FIELDS


class MaxRiRConfigSerializer(BaseConfigSerializer):
    """
    RiR Config serializer
    """

    class Meta:
        model = MaxRiRConfig
        fields = BASE_CONFIG_FIELDS


class RestConfigSerializer(BaseConfigSerializer):
    """
    Rest Config serializer
    """

    class Meta:
        model = RestConfig
        fields = BASE_CONFIG_FIELDS


class MaxRestConfigSerializer(BaseConfigSerializer):
    """
    Rest Config serializer
    """

    class Meta:
        model = MaxRestConfig
        fields = BASE_CONFIG_FIELDS


class SlotEntryStructureSerializer(serializers.ModelSerializer):
    """
    Slot entry
    """

    weight_configs = WeightConfigSerializer(source='weightconfig_set', many=True)
    max_weight_configs = WeightConfigSerializer(source='maxweightconfig_set', many=True)
    reps_configs = RepsConfigSerializer(source='repsconfig_set', many=True)
    max_reps_configs = RepsConfigSerializer(source='maxrepsconfig_set', many=True)
    set_nr_configs = SetNrConfigSerializer(source='setsconfig_set', many=True)
    max_set_nr_configs = MaxSetNrConfigSerializer(source='maxsetsconfig_set', many=True)
    rir_configs = RiRConfigSerializer(source='rirconfig_set', many=True)
    max_rir_configs = MaxRiRConfigSerializer(source='maxrirconfig_set', many=True)
    rest_configs = RestConfigSerializer(source='restconfig_set', many=True)
    max_rest_configs = RestConfigSerializer(source='maxrestconfig_set', many=True)

    class Meta:
        model = SlotEntry
        fields = (
            'id',
            'slot',
            'exercise',
            'order',
            'comment',
            'type',
            'class_name',
            'config',
            'repetition_unit',
            'repetition_rounding',
            'reps_configs',
            'max_reps_configs',
            'weight_unit',
            'weight_rounding',
            'weight_configs',
            'max_weight_configs',
            'set_nr_configs',
            'max_set_nr_configs',
            'rir_configs',
            'max_rir_configs',
            'rest_configs',
            'max_rest_configs',
        )


class SlotStructureSerializer(serializers.ModelSerializer):
    """
    Slot
    """

    entries = SlotEntryStructureSerializer(many=True)

    class Meta:
        model = Slot
        fields = (
            'id',
            'day',
            'order',
            'comment',
            'entries',
            'config',
        )


class SlotSerializer(serializers.ModelSerializer):
    """
    Slot
    """

    class Meta:
        model = Slot
        fields = (
            'id',
            'day',
            'order',
            'comment',
            'config',
        )


class DayStructureSerializer(serializers.ModelSerializer):
    """
    Day serializer
    """

    slots = SlotStructureSerializer(many=True)

    class Meta:
        model = Day
        fields = (
            'id',
            'routine',
            'order',
            'name',
            'description',
            'is_rest',
            'need_logs_to_advance',
            'type',
            'config',
            'slots',
        )


class RoutineStructureSerializer(serializers.ModelSerializer):
    """
    Routine structure serializer
    """

    days = DayStructureSerializer(many=True)

    class Meta:
        model = Routine
        fields = (
            'id',
            'name',
            'description',
            'created',
            'start',
            'end',
            'fit_in_week',
            'days',
        )


class SlotEntrySerializer(serializers.ModelSerializer):
    """
    Slot entry serializer
    """

    class Meta:
        model = SlotEntry
        fields = (
            'id',
            'slot',
            'exercise',
            'type',
            'repetition_unit',
            'repetition_rounding',
            'weight_unit',
            'weight_rounding',
            'order',
            'comment',
            'config',
        )


class SetConfigDataSerializer(serializers.Serializer):
    """
    SetConfigData serializer
    """

    slot_entry_id = serializers.IntegerField()
    exercise = serializers.IntegerField()
    sets = serializers.IntegerField()
    max_sets = serializers.IntegerField()
    weight = serializers.DecimalField(max_digits=5, decimal_places=2)
    max_weight = serializers.DecimalField(max_digits=5, decimal_places=2)
    weight_unit = serializers.IntegerField()
    weight_rounding = serializers.DecimalField(max_digits=4, decimal_places=2)
    reps = serializers.DecimalField(max_digits=5, decimal_places=2)
    max_reps = serializers.DecimalField(max_digits=5, decimal_places=2)
    reps_unit = serializers.IntegerField()
    reps_rounding = serializers.DecimalField(max_digits=4, decimal_places=2)
    rir = serializers.DecimalField(max_digits=5, decimal_places=2)
    rpe = serializers.DecimalField(max_digits=5, decimal_places=2)
    rest = serializers.DecimalField(max_digits=5, decimal_places=2)
    max_rest = serializers.DecimalField(max_digits=5, decimal_places=2)
    type = serializers.CharField()
    text_repr = serializers.CharField()
    comment = serializers.CharField()


class SlotDataSerializer(serializers.Serializer):
    """
    Slot Data serializer
    """

    comment = serializers.CharField()
    is_superset = serializers.BooleanField()
    exercises = serializers.ListSerializer(child=serializers.IntegerField())
    sets = SetConfigDataSerializer(many=True)


class WorkoutDayDataDisplayModeSerializer(serializers.Serializer):
    """
    WorkoutDayData serializer - display mode
    """

    iteration = serializers.IntegerField()
    date = serializers.DateField()
    label = serializers.CharField()
    day = DaySerializer()
    slots = SlotDataSerializer(many=True, source='slots_display_mode')


class WorkoutDayDataGymModeSerializer(serializers.Serializer):
    """
    WorkoutDayData serializer - gym mode
    """

    iteration = serializers.IntegerField()
    date = serializers.DateField()
    label = serializers.CharField()
    day = DaySerializer()
    slots = SlotDataSerializer(many=True, source='slots_gym_mode')


class WorkoutSerializer(serializers.ModelSerializer):
    """
    Workout serializer
    """

    class Meta:
        model = Workout
        fields = ('id', 'name', 'creation_date', 'description')


class WorkoutTemplateSerializer(serializers.ModelSerializer):
    """
    Workout template serializer
    """

    class Meta:
        model = Workout
        fields = ('id', 'name', 'creation_date', 'description', 'is_public')


class WorkoutSessionSerializer(serializers.ModelSerializer):
    """
    Workout session serializer
    """

    class Meta:
        model = WorkoutSession
        fields = [
            'id',
            'routine',
            'day',
            'date',
            'notes',
            'impression',
            'time_start',
            'time_end',
        ]


class WorkoutLogSerializer(serializers.ModelSerializer):
    """
    Workout session serializer
    """

    class Meta:
        model = WorkoutLog
        fields = [
            'id',
            'date',
            'session',
            'routine',
            'slot_entry',
            'next_log',
            'exercise',
            'repetition_unit',
            'reps',
            'reps_target',
            'weight_unit',
            'weight',
            'weight_target',
            'rir',
            'rir_target',
            'iteration',
        ]


class LogDisplaySerializer(serializers.Serializer):
    """
    Log Display Data serializer
    """

    session = WorkoutSessionSerializer()
    logs = WorkoutLogSerializer(many=True)


class LogDataSerializer(serializers.Serializer):
    """
    Log Stats Data serializer
    """

    exercises = serializers.DictField()
    muscle = serializers.DictField()
    upper_body = serializers.DecimalField(max_digits=10, decimal_places=2)
    lower_body = serializers.DecimalField(max_digits=10, decimal_places=2)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)


class GroupedLogDataSerializer(serializers.Serializer):
    """
    Log Stats Data serializer
    """

    iteration = serializers.DictField(child=LogDataSerializer())
    weekly = serializers.DictField(child=LogDataSerializer())
    daily = serializers.DictField(child=LogDataSerializer())
    mesocycle = LogDataSerializer()


class LogStatsDataSerializer(serializers.Serializer):
    """
    Log Stats Data serializer
    """

    intensity = GroupedLogDataSerializer()
    sets = GroupedLogDataSerializer()
    volume = GroupedLogDataSerializer()
