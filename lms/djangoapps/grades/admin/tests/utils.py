"""
Utilities for tests involving the feature flags
controlling persistent grading.
"""
from lms.djangoapps.grades.admin.models import CoursePersistentGradesFlag, PersistentGradesEnabledFlag


def set_persistent_grades_feature_flags(
        global_flag,
        override_course_settings=False,
        course_id=None,
        course_setting=False
):
    """
    Most test cases will use a single call to this function,
    as they need to set the global setting and the course-specific
    setting for a single course.
    """
    PersistentGradesEnabledFlag.objects.create(enabled=global_flag, enabled_for_all_courses=override_course_settings)
    if course_id:
        CoursePersistentGradesFlag.objects.create(course_id=course_id, enabled=course_setting)
