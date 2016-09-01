"""
Tests for the models that control the
persistent grading feature.
"""
from django.test import TestCase
from opaque_keys.edx.locator import CourseLocator
from lms.djangoapps.grades.config.models import PersistentGradesEnabledFlag
from lms.djangoapps.grades.config.tests.utils import set_persistent_grades_feature_flags


class PersistentGradesFeatureFlagTests(TestCase):
    """
    Tests the behavior of the feature flags for persistent grading.
    These are set via Django admin settings.
    """
    def setUp(self):
        super(PersistentGradesFeatureFlagTests, self).setUp()
        self.course_id_1 = CourseLocator(org="edx", course="course", run="run")
        self.course_id_2 = CourseLocator(org="edx", course="course2", run="run")

    def test_global_and_course_enabled(self):
        set_persistent_grades_feature_flags(
            global_flag=True,
            enabled_for_all_courses=False,
            course_id=self.course_id_1,
            enabled_for_course=True
        )
        self.assertTrue(PersistentGradesEnabledFlag.feature_enabled())
        self.assertTrue(PersistentGradesEnabledFlag.feature_enabled(self.course_id_1))
        self.assertFalse(PersistentGradesEnabledFlag.feature_enabled(self.course_id_2))

    def test_global_enabled_only(self):
        set_persistent_grades_feature_flags(
            global_flag=True,
            enabled_for_all_courses=False,
            course_id=self.course_id_1,
            enabled_for_course=False
        )
        self.assertTrue(PersistentGradesEnabledFlag.feature_enabled())
        self.assertFalse(PersistentGradesEnabledFlag.feature_enabled(self.course_id_1))
        self.assertFalse(PersistentGradesEnabledFlag.feature_enabled(self.course_id_2))

    def test_global_disabled_with_course_enabled(self):
        set_persistent_grades_feature_flags(
            global_flag=False,
            enabled_for_all_courses=False,
            course_id=self.course_id_1,
            enabled_for_course=True
        )
        self.assertFalse(PersistentGradesEnabledFlag.feature_enabled())
        self.assertFalse(PersistentGradesEnabledFlag.feature_enabled(self.course_id_1))
        self.assertFalse(PersistentGradesEnabledFlag.feature_enabled(self.course_id_2))

    def test_global_enabled_with_override(self):
        set_persistent_grades_feature_flags(
            global_flag=True,
            enabled_for_all_courses=True,
            course_id=self.course_id_1,
            enabled_for_course=True
        )
        self.assertTrue(PersistentGradesEnabledFlag.feature_enabled())
        self.assertTrue(PersistentGradesEnabledFlag.feature_enabled(self.course_id_1))
        self.assertTrue(PersistentGradesEnabledFlag.feature_enabled(self.course_id_2))
