from config_models.models import ConfigurationModel
from xmodule_django.models import CourseKeyField


class PersistentGradesEnabledFlag(ConfigurationModel):
    """
    Enables persistent grades across the platform.
    When this feature flag is set to true, individual courses
    must also have persistent grades enabled for the
    feature to take effect.
    """

    @classmethod
    def feature_enabled(cls, course_id=None):
        """
        Looks at the currently active configuration model to determine whether the subsection grades feature is
        available.

        If the flag is not enabled, the feature is not available.
        If the flag is enabled and the provided course_id is authorized,
            the feature is available.
        If the flag is enabled and course-specific authorization is not required, the feature is available.
        """
        if not PersistentGradesEnabledFlag.is_enabled():
            return False
        elif course_id:
            try:
                return CoursePersistentGradesFlag.objects.get(course_id=course_id).enabled
            except CoursePersistentGradesFlag.DoesNotExist:
                return False
        return True

    class Meta(object):
        app_label = "grades"

    def __unicode__(self):
        current_model = PersistentGradesEnabledFlag.current()
        return u"SubsectionGradesFlag: enabled {}".format(
            current_model.is_enabled()
        )


class CoursePersistentGradesFlag(ConfigurationModel):
    """
    Authorizes persistent grades for a specific
    course. Only has an effect if the general
    flag above is set to True.
    """
    KEY_FIELDS = ('course_id',)

    class Meta(object):
        app_label = "grades"

    # The course that these features are attached to.
    course_id = CourseKeyField(max_length=255, db_index=True, unique=True)

    def __unicode__(self):
        not_en = "Not "
        if self.enabled:
            not_en = ""
        # pylint: disable=no-member
        return u"Course '{}': Persistent Grades {}Enabled".format(self.course_id.to_deprecated_string(), not_en)
