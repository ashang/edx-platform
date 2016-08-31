"""
Grades Application Configuration

Signal handlers are connected here.
"""

from django.apps import AppConfig


class GradesConfig(AppConfig):
    """
    Application Configuration for Grades.
    """
    name = u'lms.djangoapps.grades'

    def ready(self):
        """
        Connect handlers to recalculate grades.

        Redispatch score_set and score_reset signals from submissions API
        to fire SCORE_CHANGED signal.
        """
        # Can't import models at module level in AppConfigs, and models get
        # included from the signal handlers
        from .signals import handlers
        handlers.connect_handlers()
