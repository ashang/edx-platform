from lms.djangoapps.grades.admin.models import PersistentGradesEnabledFlag, CoursePersistentGradesFlag
from django.test import TestCase
from opaque_keys.edx.locator import CourseLocator


class PersistentGradesFeatureFlagTests(TestCase):
    def setUp(self):
        self.course_id_1 = CourseLocator(org="edx", course="course", run="run")
        self.course_id_2 = CourseLocator(org="edx", course="course2", run="run")

    def test_global_and_course_enabled(self):
        PersistentGradesEnabledFlag.objects.create(enabled=True)
        CoursePersistentGradesFlag.objects.create(course_id=self.course_id_1, enabled=True)
        self.assertTrue(PersistentGradesEnabledFlag.feature_enabled())
        self.assertTrue(PersistentGradesEnabledFlag.feature_enabled(self.course_id_1))
        self.assertFalse(PersistentGradesEnabledFlag.feature_enabled(self.course_id_2))

    def test_global_enabled_only(self):
        PersistentGradesEnabledFlag.objects.create(enabled=True)
        CoursePersistentGradesFlag.objects.create(course_id=self.course_id_1, enabled=False)
        self.assertTrue(PersistentGradesEnabledFlag.feature_enabled())
        self.assertFalse(PersistentGradesEnabledFlag.feature_enabled(self.course_id_1))
        self.assertFalse(PersistentGradesEnabledFlag.feature_enabled(self.course_id_2))

    def test_global_disabled_with_courses_enabled(self):
        PersistentGradesEnabledFlag.objects.create(enabled=False)
        CoursePersistentGradesFlag.objects.create(course_id=self.course_id_1, enabled=True)
        CoursePersistentGradesFlag.objects.create(course_id=self.course_id_2, enabled=True)
        self.assertFalse(PersistentGradesEnabledFlag.feature_enabled())
        self.assertFalse(PersistentGradesEnabledFlag.feature_enabled(self.course_id_1))
        self.assertFalse(PersistentGradesEnabledFlag.feature_enabled(self.course_id_2))
