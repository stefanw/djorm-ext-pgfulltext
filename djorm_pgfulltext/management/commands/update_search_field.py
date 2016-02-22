"""
Update search fields.
"""
from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ImproperlyConfigured
from django.apps import apps


class Command(BaseCommand):
    help = 'Update search fields'
    args = "appname [model]"

    def handle(self, app=None, model=None, **options):
        if not app:
            raise CommandError("You must provide an app to update search fields.")

        # check application

        try:
            app_module = apps.get_app_config(app)
        except ImproperlyConfigured:
            raise CommandError("There is no enabled application matching '%s'." % app)

        app_models = []

        # get models

        if model:
            m = app_module.get_model(model)
            if not m:
                raise CommandError("There is no model '%s'." % model)

            app_models.append(app_module.get_model(model))
        else:
            app_models += app_module.get_models()

        # get models only with search managers

        app_models_for_process = [x for x in app_models if getattr(x, '_fts_manager', None)]

        if not app_models_for_process:
            raise CommandError("There is no models for processing.")

        # processing

        for m in app_models_for_process:
            print("Processing model %s..." % m, end='')
            m._fts_manager.update_search_field()
            print("Done")
