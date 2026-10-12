"""Small helpers for allocating Student_ID values."""


def get_smallest_available_student_id(student_ids):
    """Return the first positive Student_ID not present in ``student_ids``."""
    next_id = 1

    for student_id in sorted(student_ids):
        if student_id == next_id:
            next_id += 1
        elif student_id > next_id:
            break

    return next_id
