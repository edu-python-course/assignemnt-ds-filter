import unittest
from copy import deepcopy

from main import filter_by_values


class TestReplit(unittest.TestCase):
    def setUp(self):
        self.dataset = [
            {"A": 1, "B": 3, "C": 2},
            {"A": 1, "B": 3, "C": 1},
            {"A": 3, "B": 2, "C": 2},
            {"A": 3, "B": 1, "C": 1},
            {"A": 2, "B": 3, "C": 1},
            {"A": 2, "B": 1, "C": 1},
            {"A": 3, "B": 2, "C": 2},
            {"A": 2, "B": 2, "C": 3},
            {"A": 3, "B": 3, "C": 3},
        ]

    @unittest.expectedFailure
    def test_training_a_ds(self):
        """Filter example dataset with A key"""
        msg = "Training dataset filter failed: {}"
        keys = ["A"]
        test_dataset = [
            {"A": 1, "B": 3, "C": 2},
            {"A": 3, "B": 2, "C": 2},
            {"A": 2, "B": 3, "C": 1},
        ]
        filtered_dataset = filter_by_values(self.dataset, keys)
        self.assertListEqual(filtered_dataset, test_dataset, msg.format(keys))

    @unittest.expectedFailure
    def test_training_b_ds(self):
        """Filter example dataset with B key"""
        msg = "Training dataset filter failed: {}"
        keys = ["B"]
        test_dataset = [
            {"A": 1, "B": 3, "C": 2},
            {"A": 3, "B": 2, "C": 2},
            {"A": 3, "B": 1, "C": 1},
        ]
        filtered_dataset = filter_by_values(self.dataset, keys)
        self.assertListEqual(filtered_dataset, test_dataset, msg.format(keys))

    @unittest.expectedFailure
    def test_training_ac_ds(self):
        """Filter example dataset with A, C keys"""
        msg = "Training dataset filter failed: {}"
        keys = ["A", "C"]
        test_dataset = [
            {"A": 1, "B": 3, "C": 2},
            {"A": 1, "B": 3, "C": 1},
            {"A": 3, "B": 2, "C": 2},
            {"A": 3, "B": 1, "C": 1},
            {"A": 2, "B": 3, "C": 1},
            {"A": 2, "B": 2, "C": 3},
            {"A": 3, "B": 3, "C": 3},
        ]
        filtered_dataset = filter_by_values(self.dataset, keys)
        self.assertListEqual(filtered_dataset, test_dataset, msg.format(keys))

    @unittest.expectedFailure
    def test_training_bc_ds(self):
        """Filter example dataset with B, C keys"""
        msg = "Training dataset filter failed: {}"
        keys = ["B", "C"]
        test_dataset = [
            {"A": 1, "B": 3, "C": 2},
            {"A": 1, "B": 3, "C": 1},
            {"A": 3, "B": 2, "C": 2},
            {"A": 3, "B": 1, "C": 1},
            {"A": 2, "B": 2, "C": 3},
            {"A": 3, "B": 3, "C": 3},
        ]
        filtered_dataset = filter_by_values(self.dataset, keys)
        self.assertListEqual(filtered_dataset, test_dataset, msg.format(keys))

    @unittest.expectedFailure
    def test_training_abc_ds(self):
        """Filter example dataset with all keys"""
        msg = "Training dataset filter failed: {}"
        keys = ["A", "B", "C"]
        test_dataset = [
            {"A": 1, "B": 3, "C": 2},
            {"A": 1, "B": 3, "C": 1},
            {"A": 3, "B": 2, "C": 2},
            {"A": 3, "B": 1, "C": 1},
            {"A": 2, "B": 3, "C": 1},
            {"A": 2, "B": 1, "C": 1},
            {"A": 2, "B": 2, "C": 3},
            {"A": 3, "B": 3, "C": 3},
        ]
        # noinspection PyArgumentList
        filtered_dataset = filter_by_values(self.dataset)
        self.assertListEqual(filtered_dataset, test_dataset, msg.format(None))
        filtered_dataset = filter_by_values(self.dataset, keys)
        self.assertListEqual(filtered_dataset, test_dataset, msg.format(keys))

    @unittest.expectedFailure
    def test_data_modification(self):
        original_copy = deepcopy(self.dataset)
        result = filter_by_values(self.dataset, ["x", "y"])
        self.assertIsNotNone(result)
        self.assertListEqual(self.dataset, original_copy)

    @unittest.expectedFailure
    def test_new_object_return(self):
        result = filter_by_values(self.dataset, ["x", "y"])
        self.assertIsNotNone(result)
        self.assertIsNot(self.dataset, result)
