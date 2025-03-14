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

# Django
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.management.base import (
    BaseCommand,
    CommandError,
)
from django.core.validators import URLValidator

# wger
from wger.nutrition.sync import sync_ingredients
from wger.utils.validators import validate_language_code


class Command(BaseCommand):
    """
    Synchronizes ingredient data from a wger instance to the local database
    """

    remote_url = settings.WGER_SETTINGS['WGER_INSTANCE']

    help = """Synchronizes ingredient data from a wger instance to the local database"""

    def add_arguments(self, parser):
        parser.add_argument(
            '--remote-url',
            action='store',
            dest='remote_url',
            default=settings.WGER_SETTINGS['WGER_INSTANCE'],
            help=f'Remote URL to fetch the ingredients from (default: WGER_SETTINGS'
            f'["WGER_INSTANCE"] - {settings.WGER_SETTINGS["WGER_INSTANCE"]})',
        )
        parser.add_argument(
            '-l',
            '--languages',
            action='store',
            dest='languages',
            default=None,
            help='Specify a comma-separated subset of languages to sync. Example: en,fr,es',
        )

    def handle(self, **options):
        remote_url = options['remote_url']
        languages = options['languages']

        try:
            val = URLValidator()
            val(remote_url)
            self.remote_url = remote_url
        except ValidationError:
            raise CommandError('Please enter a valid URL')
        try:
            self.languages = languages
            if self.languages is not None:
                for language in self.languages.split(','):
                    validate_language_code(language)
        except ValidationError as e:
            raise CommandError('\n'.join([str(arg) for arg in e.args if arg is not None]))

        sync_ingredients(self.stdout.write, self.remote_url, self.languages, self.style.SUCCESS)
