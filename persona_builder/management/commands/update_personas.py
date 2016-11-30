from optparse import make_option

import datetime

from persona_builder.models import Persona
from persona_builder.views import get_active_configuration

__author__ = 'dimitris'

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Update all personas. Use the `-p` property to update a specific persona'
    option_list = BaseCommand.option_list + (
        make_option(
            "-p",
            "--persona",
            dest="persona",
            help="The ID of a specific persona to update",
            metavar="PERSONA"
        ),
    )

    def handle(self, *args, **options):
        if 'persona' in options and options['persona']:
            try:
                persona_id = int(options['persona'])
            except ValueError:
                print 'The persona ID must be an integer'
                return

            personas = Persona.objects.filter(pk=persona_id)
            if not personas:
                print 'Persona with ID #%d was not found' % persona_id
        else:
            personas = Persona.objects.all()

        # get anonymizer configuration
        config = get_active_configuration()

        # update all personas
        for persona in personas:
            t = datetime.datetime.now()
            # get a user manager
            user_manager = config.get_user_manager(token=persona.uuid)

            # update & save persona
            try:
                persona.update_users(user_manager)
                persona.save()

                # log
                t2 = datetime.datetime.now()
                print 'Persona #%d updated in %s' % (persona.pk, str(t2 - t))
            except:
                print 'Persona #%d could not be updated' % persona.pk
                
        print '%d personas updated successfully' % len(personas)
