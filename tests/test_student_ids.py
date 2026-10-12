"""Tests for Student_ID allocation without requiring a MySQL server."""

import unittest

from backend.student_ids import get_smallest_available_student_id


class StudentIdAllocationTests(unittest.TestCase):
    def test_reuses_deleted_id(self):
        self.assertEqual(get_smallest_available_student_id([1, 3]), 2)

    def test_reuses_first_gap(self):
        self.assertEqual(get_smallest_available_student_id([1, 2, 5, 7, 8]), 3)

    def test_uses_next_id_when_there_are_no_gaps(self):
        self.assertEqual(get_smallest_available_student_id([1, 2, 3]), 4)


if __name__ == "__main__":
    unittest.main()
