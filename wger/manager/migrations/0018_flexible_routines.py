# Generated by Django 4.2.6 on 2024-03-12 15:17

import datetime

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0016_alter_language_short_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exercises', '0032_rename_exercise'),
        ('manager', '0017_alter_workoutlog_exercise_base'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayNg',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'type',
                    models.CharField(
                        choices=[
                            ('custom', 'Custom'),
                            ('enom', 'Emom'),
                            ('amrap', 'Amrap'),
                            ('hiit', 'Hiit'),
                            ('tabata', 'Tabata'),
                            ('edt', 'Edt'),
                            ('rft', 'Rft'),
                            ('afap', 'Afap'),
                        ],
                        default='custom',
                        max_length=10,
                    ),
                ),
                ('name', models.CharField(max_length=20, verbose_name='Description')),
                ('description', models.CharField(max_length=1000, verbose_name='Description')),
                ('is_rest', models.BooleanField(default=False)),
                ('last_day_in_week', models.BooleanField(default=False)),
                ('need_logs_to_advance', models.BooleanField(default=False)),
                (
                    'next_day',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to='manager.dayng',
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name='workoutlog',
            name='iteration',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='workoutlog',
            name='session',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='manager.workoutsession',
                verbose_name='Session',
            ),
        ),
        migrations.AlterField(
            model_name='workoutlog',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='workoutsession',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='Date'),
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('order', models.IntegerField(default=1, verbose_name='Order')),
                ('comment', models.CharField(blank=True, max_length=200, verbose_name='Comment')),
                (
                    'day',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='slots',
                        to='manager.dayng',
                        verbose_name='Exercise day',
                    ),
                ),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='SlotConfig',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('order', models.PositiveIntegerField(blank=True)),
                (
                    'type',
                    models.CharField(
                        choices=[
                            ('normal', 'Normal'),
                            ('dropset', 'Dropset'),
                            ('myo', 'Myo'),
                            ('partial', 'Partial'),
                            ('forced', 'Forced'),
                            ('tut', 'Tut'),
                            ('iso', 'Iso Hold'),
                            ('jump', 'Jump'),
                        ],
                        default='normal',
                        max_length=10,
                    ),
                ),
                ('comment', models.CharField(blank=True, max_length=100)),
                ('class_name', models.CharField(blank=True, max_length=50, null=True)),
                (
                    'exercise',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='exercises.exercise'
                    ),
                ),
                (
                    'repetition_unit',
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to='core.repetitionunit',
                    ),
                ),
                (
                    'repetition_rounding',
                    models.DecimalField(decimal_places=2, default=1, max_digits=4),
                ),
                (
                    'slot',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='configs',
                        to='manager.Slot',
                    ),
                ),
                (
                    'weight_unit',
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to='core.weightunit',
                        verbose_name='Unit',
                    ),
                ),
                (
                    'weight_rounding',
                    models.DecimalField(
                        decimal_places=2,
                        default=1.25,
                        max_digits=4,
                    ),
                ),
            ],
            options={
                'ordering': ['order', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Routine',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        blank=True,
                        max_length=50,
                        verbose_name='Name',
                    ),
                ),
                (
                    'description',
                    models.TextField(
                        blank=True,
                        max_length=1000,
                        verbose_name='Description',
                    ),
                ),
                (
                    'created',
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name='Creation date',
                    ),
                ),
                ('start', models.DateField(verbose_name='Start date')),
                ('end', models.DateField(verbose_name='End date')),
                (
                    'first_day',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='first_days',
                        to='manager.dayng',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='User',
                    ),
                ),
                (
                    'is_public',
                    models.BooleanField(
                        default=False,
                        help_text='A public template is available to other users',
                        verbose_name='Public template',
                    ),
                ),
                (
                    'is_template',
                    models.BooleanField(
                        default=False,
                        help_text='Marking a workout as a template will freeze it and allow you to make copies of it',
                        verbose_name='Workout template',
                    ),
                ),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.AddField(
            model_name='dayng',
            name='routine',
            field=models.ForeignKey(
                related_name='days',
                on_delete=django.db.models.deletion.CASCADE,
                to='manager.routine',
                verbose_name='Routine',
            ),
        ),
        migrations.AddField(
            model_name='workoutlog',
            name='slot_config',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='manager.slotconfig',
            ),
        ),
        migrations.AddField(
            model_name='workoutlog',
            name='next_log',
            field=models.ForeignKey(
                default=None,
                editable=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='manager.workoutlog',
            ),
        ),
        migrations.AddField(
            model_name='workoutlog',
            name='routine',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='manager.routine',
                verbose_name='Workout',
            ),
        ),
        migrations.AddField(
            model_name='workoutsession',
            name='day',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='manager.dayng',
            ),
        ),
        migrations.AddField(
            model_name='workoutsession',
            name='routine',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='manager.routine',
            ),
        ),
        migrations.CreateModel(
            name='WeightConfig',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('iteration', models.PositiveIntegerField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=6)),
                (
                    'operation',
                    models.CharField(
                        choices=[('+', 'Plus'), ('-', 'Minus')],
                        default='+',
                        max_length=1,
                        null=True,
                    ),
                ),
                (
                    'step',
                    models.CharField(
                        choices=[('abs', 'Absolute'), ('percent', 'Percent')],
                        default='abs',
                        max_length=10,
                        null=True,
                    ),
                ),
                ('replace', models.BooleanField(default=False)),
                ('need_log_to_apply', models.BooleanField(default=False, null=True)),
                (
                    'slot_config',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='manager.slotconfig',
                    ),
                ),
            ],
            options={
                'ordering': ['slot_config', 'iteration'],
                'abstract': False,
                'unique_together': {('slot_config', 'iteration')},
            },
        ),
        migrations.CreateModel(
            name='MaxWeightConfig',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('iteration', models.PositiveIntegerField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=6)),
                (
                    'operation',
                    models.CharField(
                        choices=[('+', 'Plus'), ('-', 'Minus')],
                        default='+',
                        max_length=1,
                        null=True,
                    ),
                ),
                (
                    'step',
                    models.CharField(
                        choices=[('abs', 'Absolute'), ('percent', 'Percent')],
                        default='abs',
                        max_length=10,
                        null=True,
                    ),
                ),
                ('replace', models.BooleanField(default=False)),
                ('need_log_to_apply', models.BooleanField(default=False)),
                (
                    'slot_config',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='manager.slotconfig',
                    ),
                ),
            ],
            options={
                'ordering': ['slot_config', 'iteration'],
                'abstract': False,
                'unique_together': {('slot_config', 'iteration')},
            },
        ),
        migrations.CreateModel(
            name='RiRConfig',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('iteration', models.PositiveIntegerField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=6)),
                (
                    'operation',
                    models.CharField(
                        choices=[('+', 'Plus'), ('-', 'Minus')],
                        default='+',
                        max_length=1,
                        null=True,
                    ),
                ),
                (
                    'step',
                    models.CharField(
                        choices=[('abs', 'Absolute'), ('percent', 'Percent')],
                        default='abs',
                        max_length=10,
                        null=True,
                    ),
                ),
                ('replace', models.BooleanField(default=False)),
                ('need_log_to_apply', models.BooleanField(default=False)),
                (
                    'slot_config',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='manager.slotconfig',
                    ),
                ),
            ],
            options={
                'ordering': ['slot_config', 'iteration'],
                'abstract': False,
                'unique_together': {('slot_config', 'iteration')},
            },
        ),
        migrations.CreateModel(
            name='RestConfig',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('iteration', models.PositiveIntegerField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=6)),
                (
                    'operation',
                    models.CharField(
                        choices=[('+', 'Plus'), ('-', 'Minus')],
                        default='+',
                        max_length=1,
                        null=True,
                    ),
                ),
                (
                    'step',
                    models.CharField(
                        choices=[('abs', 'Absolute'), ('percent', 'Percent')],
                        default='abs',
                        max_length=10,
                        null=True,
                    ),
                ),
                ('replace', models.BooleanField(default=False)),
                ('need_log_to_apply', models.BooleanField(default=False)),
                (
                    'slot_config',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='manager.slotconfig',
                    ),
                ),
            ],
            options={
                'ordering': ['slot_config', 'iteration'],
                'abstract': False,
                'unique_together': {('slot_config', 'iteration')},
            },
        ),
        migrations.CreateModel(
            name='MaxRestConfig',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('iteration', models.PositiveIntegerField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=6)),
                (
                    'operation',
                    models.CharField(
                        choices=[('+', 'Plus'), ('-', 'Minus')],
                        default='+',
                        max_length=1,
                        null=True,
                    ),
                ),
                (
                    'step',
                    models.CharField(
                        choices=[('abs', 'Absolute'), ('percent', 'Percent')],
                        default='abs',
                        max_length=10,
                        null=True,
                    ),
                ),
                ('replace', models.BooleanField(default=False)),
                ('need_log_to_apply', models.BooleanField(default=False)),
                (
                    'slot_config',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='manager.slotconfig',
                    ),
                ),
            ],
            options={
                'ordering': ['slot_config', 'iteration'],
                'abstract': False,
                'unique_together': {('slot_config', 'iteration')},
            },
        ),
        migrations.CreateModel(
            name='RepsConfig',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('iteration', models.PositiveIntegerField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=6)),
                (
                    'operation',
                    models.CharField(
                        choices=[('+', 'Plus'), ('-', 'Minus')],
                        default='+',
                        max_length=1,
                        null=True,
                    ),
                ),
                (
                    'step',
                    models.CharField(
                        choices=[('abs', 'Absolute'), ('percent', 'Percent')],
                        default='abs',
                        max_length=10,
                        null=True,
                    ),
                ),
                ('replace', models.BooleanField(default=False)),
                ('need_log_to_apply', models.BooleanField(default=False)),
                (
                    'slot_config',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='manager.slotconfig'
                    ),
                ),
            ],
            options={
                'ordering': ['slot_config', 'iteration'],
                'abstract': False,
                'unique_together': {('slot_config', 'iteration')},
            },
        ),
        migrations.CreateModel(
            name='MaxRepsConfig',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('iteration', models.PositiveIntegerField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=6)),
                (
                    'operation',
                    models.CharField(
                        choices=[('+', 'Plus'), ('-', 'Minus')],
                        default='+',
                        max_length=1,
                        null=True,
                    ),
                ),
                (
                    'step',
                    models.CharField(
                        choices=[('abs', 'Absolute'), ('percent', 'Percent')],
                        default='abs',
                        max_length=10,
                        null=True,
                    ),
                ),
                ('replace', models.BooleanField(default=False)),
                ('need_log_to_apply', models.BooleanField(default=False)),
                (
                    'slot_config',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='manager.slotconfig'
                    ),
                ),
            ],
            options={
                'ordering': ['slot_config', 'iteration'],
                'abstract': False,
                'unique_together': {('slot_config', 'iteration')},
            },
        ),
        migrations.CreateModel(
            name='SetsConfig',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('iteration', models.PositiveIntegerField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=6)),
                (
                    'operation',
                    models.CharField(
                        choices=[('+', 'Plus'), ('-', 'Minus')],
                        default='+',
                        max_length=1,
                        null=True,
                    ),
                ),
                (
                    'step',
                    models.CharField(
                        choices=[('abs', 'Absolute'), ('percent', 'Percent')],
                        default='abs',
                        max_length=10,
                        null=True,
                    ),
                ),
                ('replace', models.BooleanField(default=False)),
                ('need_log_to_apply', models.BooleanField(default=False)),
                (
                    'slot_config',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='manager.slotconfig',
                    ),
                ),
            ],
            options={
                'ordering': ['slot_config', 'iteration'],
                'abstract': False,
                'unique_together': {('slot_config', 'iteration')},
            },
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'start_offset',
                    models.PositiveIntegerField(default=1, verbose_name='Start'),
                ),
                (
                    'end_offset',
                    models.PositiveIntegerField(default=2, verbose_name='End'),
                ),
                ('label', models.CharField(max_length=35, verbose_name='Label')),
                (
                    'comment',
                    models.CharField(default='', max_length=500, verbose_name='Comment'),
                ),
                (
                    'routine',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='labels',
                        to='manager.routine',
                        verbose_name='Routine',
                    ),
                ),
            ],
            options={
                'ordering': ['start_offset'],
            },
        ),
    ]
