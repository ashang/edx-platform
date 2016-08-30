from lms.djangoapps.grades.admin.models import PersistentGradesEnabledFlag
from lms.djangoapps.grades.admin.tests.utils import set_persistent_grades_feature_flags, set_course_specific_flag
from django.test import TestCase
from opaque_keys.edx.locator import CourseLocator


class PersistentGradesFeatureFlagTests(TestCase):
    def setUp(self):
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
