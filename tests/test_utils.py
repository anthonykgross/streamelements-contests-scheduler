import unittest

from utils import CSVReader


class TestCSVReader(unittest.TestCase):
    def test_default(self):
        CSV_FORMAT = {
            'START_ROW_INDEX': 1,
            'QUESTION_COL_INDEX': 0,
            'RESPONSE_COL_INDEX': 1,
            'CHOICES_COL_INDEXES': [1, 2, 3]
        }
        reader = CSVReader('contests.csv', CSV_FORMAT)
        contests = reader.get_contests()
        self.assertEqual(len(contests), 2)

        contest = contests[0]
        self.assertEqual(contest.title, '1+1=?')
        self.assertEqual(len(contest.choices), 3)
        self.assertEqual(contest.choices[1].title, '3')

    def test_2_choices(self):
        CSV_FORMAT = {
            'START_ROW_INDEX': 1,
            'QUESTION_COL_INDEX': 0,
            'RESPONSE_COL_INDEX': 1,
            'CHOICES_COL_INDEXES': [1, 3]
        }
        reader = CSVReader('contests.csv', CSV_FORMAT)
        contests = reader.get_contests()
        self.assertEqual(len(contests), 2)

        contest = contests[0]
        self.assertEqual(contest.title, '1+1=?')
        self.assertEqual(len(contest.choices), 2)
        self.assertEqual(contest.choices[1].title, '4')

    def test_other_question(self):
        CSV_FORMAT = {
            'START_ROW_INDEX': 1,
            'QUESTION_COL_INDEX': 1,
            'RESPONSE_COL_INDEX': 1,
            'CHOICES_COL_INDEXES': [1, 3]
        }
        reader = CSVReader('contests.csv', CSV_FORMAT)
        contests = reader.get_contests()
        self.assertEqual(len(contests), 2)

        contest = contests[0]
        self.assertEqual(contest.title, '2')
        self.assertEqual(len(contest.choices), 2)
        self.assertEqual(contest.choices[1].title, '4')

    def test_start_index_too_far(self):
        CSV_FORMAT = {
            'START_ROW_INDEX': 10,
            'QUESTION_COL_INDEX': 0,
            'RESPONSE_COL_INDEX': 1,
            'CHOICES_COL_INDEXES': [1, 2, 3]
        }
        reader = CSVReader('contests.csv', CSV_FORMAT)
        contests = reader.get_contests()
        self.assertEqual(len(contests), 0)

    def test_include_headers(self):
        CSV_FORMAT = {
            'START_ROW_INDEX': 0,
            'QUESTION_COL_INDEX': 0,
            'RESPONSE_COL_INDEX': 1,
            'CHOICES_COL_INDEXES': [1, 2, 3]
        }
        reader = CSVReader('contests.csv', CSV_FORMAT)
        contests = reader.get_contests()
        self.assertEqual(len(contests), 3)

        contest = contests[0]
        self.assertEqual(contest.title, 'Question')
        self.assertEqual(len(contest.choices), 3)
        self.assertEqual(contest.choices[1].title, 'choice_1')

    def test_response_not_in_choice(self):
        CSV_FORMAT = {
            'START_ROW_INDEX': 1,
            'QUESTION_COL_INDEX': 0,
            'RESPONSE_COL_INDEX': 1,
            'CHOICES_COL_INDEXES': [2, 3]
        }
        reader = CSVReader('contests.csv', CSV_FORMAT)

        with self.assertRaises(Exception):
            contests = reader.get_contests()
            self.assertEqual(len(contests), 2)

    def test_out_of_range(self):
        CSV_FORMAT = {
            'START_ROW_INDEX': 1,
            'QUESTION_COL_INDEX': 0,
            'RESPONSE_COL_INDEX': 1,
            'CHOICES_COL_INDEXES': [1, 8]
        }
        reader = CSVReader('contests.csv', CSV_FORMAT)

        with self.assertRaises(Exception):
            contests = reader.get_contests()
            self.assertEqual(len(contests), 2)
