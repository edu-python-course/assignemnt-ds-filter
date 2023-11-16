import sqlite3
import unittest
from pathlib import Path

from main import filter_by_values

FIXTURES_DIR = Path(__file__).resolve().parent.joinpath("fixtures")
DATASETS_DB = FIXTURES_DIR / "datasets.db"


def get_people_dataset():
    query = ("SELECT first_name, last_name, birth_date, city "
             "FROM people ORDER BY id")
    connection = sqlite3.connect(DATASETS_DB)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(query)
    people = [dict(record) for record in cursor.fetchall()]
    connection.close()

    return people


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(DATASETS_DB)
        self.connection.row_factory = sqlite3.Row
        self.people_dataset = get_people_dataset()

    def tearDown(self):
        self.connection.close()

    def get_filtered_people(self, *keys):
        keys = ",".join(keys)  # partition by clause
        query = f"""
        SELECT first_name,
               last_name,
               birth_date,
               city
        FROM (SELECT *,
                     ROW_NUMBER() OVER (PARTITION BY {keys} ORDER BY id) AS rn
              FROM people) AS sq
        WHERE rn = 1
        ORDER BY id;
        """

        cursor = self.connection.cursor()
        cursor.execute(query)

        return [dict(row) for row in cursor.fetchall()]

    @unittest.expectedFailure
    def test_empty_dataset(self):
        """Empty dataset"""
        msg = "Empty dataset check failed"
        self.assertListEqual(filter_by_values([], []), [], msg)
        self.assertListEqual(filter_by_values([], ["a"]), [], msg)
        self.assertListEqual(filter_by_values([], ["a", "b"]), [], msg)

    @unittest.expectedFailure
    def test_people_ds_single_key(self):
        """Filter people dataset with a single key"""
        msg = "Single key filter check failed: {}"

        keys = ["first_name"]
        filtered_dataset = filter_by_values(self.people_dataset, keys)
        test_dataset = self.get_filtered_people(*keys)
        self.assertListEqual(filtered_dataset, test_dataset, msg.format(keys))

        keys = ["last_name"]
        filtered_dataset = filter_by_values(self.people_dataset, keys)
        test_dataset = self.get_filtered_people(*keys)
        self.assertListEqual(filtered_dataset, test_dataset, msg.format(keys))

        keys = ["birth_date"]
        filtered_dataset = filter_by_values(self.people_dataset, keys)
        test_dataset = self.get_filtered_people(*keys)
        self.assertListEqual(filtered_dataset, test_dataset, msg.format(keys))

        keys = ["city"]
        filtered_dataset = filter_by_values(self.people_dataset, keys)
        test_dataset = self.get_filtered_people(*keys)
        self.assertListEqual(filtered_dataset, test_dataset, msg.format(keys))

    @unittest.expectedFailure
    def test_people_ds_multiple_keys(self):
        """Filter people dataset with multiple keys"""
        msg = "Multiple keys filter check failed: {}"

        keys = ["first_name", "last_name"]
        filtered_dataset = filter_by_values(self.people_dataset, keys)
        test_dataset = self.get_filtered_people(*keys)
        self.assertListEqual(filtered_dataset, test_dataset, msg.format(keys))

        keys = ["first_name", "city"]
        filtered_dataset = filter_by_values(self.people_dataset, keys)
        test_dataset = self.get_filtered_people(*keys)
        self.assertListEqual(filtered_dataset, test_dataset, msg.format(keys))

        keys = ["first_name", "birth_date"]
        filtered_dataset = filter_by_values(self.people_dataset, keys)
        test_dataset = self.get_filtered_people(*keys)
        self.assertListEqual(filtered_dataset, test_dataset, msg.format(keys))

        keys = ["first_name", "last_name", "city"]
        filtered_dataset = filter_by_values(self.people_dataset, keys)
        test_dataset = self.get_filtered_people(*keys)
        self.assertListEqual(filtered_dataset, test_dataset, msg.format(keys))

        keys = ["last_name", "city"]
        filtered_dataset = filter_by_values(self.people_dataset, keys)
        test_dataset = self.get_filtered_people(*keys)
        self.assertListEqual(filtered_dataset, test_dataset, msg.format(keys))

    @unittest.expectedFailure
    def test_people_ds_no_keys(self):
        """Filter people dataset without keys provided"""
        msg = "No keys filter check failed: {}"

        keys = "first_name", "last_name", "birth_date", "city"
        test_dataset = self.get_filtered_people(*keys)

        # noinspection PyArgumentList
        filtered_dataset = filter_by_values(self.people_dataset)
        self.assertListEqual(filtered_dataset, test_dataset, msg.format(None))

        filtered_dataset = filter_by_values(self.people_dataset, [])
        self.assertListEqual(filtered_dataset, test_dataset, msg.format([]))


if __name__ == "__main__":
    unittest.main()
