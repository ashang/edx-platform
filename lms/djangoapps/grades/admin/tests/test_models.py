"""
Tests for the models within the admin section
of the grades app. Currently this consists
of Django admin settings for persistent grades.
"""
from lms.djangoapps.grades.admin.models import PersistentGradesEnabledFlag
from lms.djangoapps.grades.admin.tests.utils import set_persistent_grades_feature_flags
from django.test import TestCase
from opaque_keys.edx.locator import CourseLocator


class PersistentGradesFeatureFlagTests(TestCase):
    """
    Tests the behavior of the feature flags for persistent grading.
    These are set via Django admin settings.
    """
    def setUp(self):
        super(PersistentGradesFeatureFlagTests)
        self.course_id_1 = CourseLocator(org="edx", course="course", run="run")
        self.course_id_2 = CourseLocator(org="edx", course="course2", run="run")

    def test_global_and_course_enabled(self):
        set_persistent_grades_feature_flags(
            global_flag=True,
            override_course_settings=False,
            course_id=self.course_id_1,
            course_setting=True
        )
        self.assertTrue(PersistentGradesEnabledFlag.feature_enabled())
        self.assertTrue(PersistentGradesEnabledFlag.feature_enabled(self.course_id_1))
        self.assertFalse(PersistentGradesEnabledFlag.feature_enabled(self.course_id_2))

    def test_global_enabled_only(self):
        set_persistent_grades_feature_flags(
            global_flag=True,
            override_course_settings=False,
            course_id=self.course_id_1,
            course_setting=False
        )
        self.assertTrue(PersistentGradesEnabledFlag.feature_enabled())
        self.assertFalse(PersistentGradesEnabledFlag.feature_enabled(self.course_id_1))
        self.assertFalse(PersistentGradesEnabledFlag.feature_enabled(self.course_id_2))

    def test_global_disabled_with_course_enabled(self):
        set_persistent_grades_feature_flags(
            global_flag=False,
            override_course_settings=False,
            course_id=self.course_id_1,
            course_setting=True
        )
        self.assertFalse(PersistentGradesEnabledFlag.feature_enabled())
        self.assertFalse(PersistentGradesEnabledFlag.feature_enabled(self.course_id_1))
        self.assertFalse(PersistentGradesEnabledFlag.feature_enabled(self.course_id_2))

    def test_global_enabled_with_override(self):
        set_persistent_grades_feature_flags(
            global_flag=True,
            override_course_settings=True,
            course_id=self.course_id_1,
            course_setting=True
        )
        self.assertTrue(PersistentGradesEnabledFlag.feature_enabled())
        self.assertTrue(PersistentGradesEnabledFlag.feature_enabled(self.course_id_1))
        self.assertTrue(PersistentGradesEnabledFlag.feature_enabled(self.course_id_2))
