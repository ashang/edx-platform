"""
Utilities for grades related tests
"""
from contextlib import contextmanager
from lms.djangoapps.grades.models import CoursePersistentGradesFlag, PersistentGradesEnabledFlag
from mock import patch


@contextmanager
def mock_passing_grade(grade_pass='Pass', percent=0.75):
    """
    Mock the grading function to always return a passing grade.
    """
    with patch('lms.djangoapps.grades.course_grades.summary') as mock_grade:
        mock_grade.return_value = {'grade': grade_pass, 'percent': percent}
        yield


@contextmanager
def mock_get_score(earned=0, possible=1):
    """
    Mocks the get_score function to return a valid grade.
    """
    with patch('lms.djangoapps.grades.new.subsection_grade.get_score') as mock_score:
        mock_score.return_value = (earned, possible)
        yield mock_score


def set_persistent_grades_feature_flags(
        global_flag,
        enabled_for_all_courses=False,
        course_id=None,
        enabled_for_course=False
):
    """
    Most test cases will use a single call to this function,
    as they need to set the global setting and the course-specific
    setting for a single course.
    """

    PersistentGradesEnabledFlag.objects.create(enabled=global_flag, enabled_for_all_courses=enabled_for_all_courses)
    if course_id:
        CoursePersistentGradesFlag.objects.create(course_id=course_id, enabled=enabled_for_course)
