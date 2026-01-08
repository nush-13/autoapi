import unittest
import pandas as pd
from analysis import analyze_log_file
import os

class TestAnalysis(unittest.TestCase):

    def setUp(self):
        # Create a dummy log file for testing
        log_data = {
            'query': [
                'SELECT * FROM users WHERE id = 1 AND name = "test" AND age = 30',
                'SELECT * FROM products WHERE category = "electronics" AND price > 100.00'
            ]
        }
        self.log_file_path = 'test_log.csv'
        pd.DataFrame(log_data).to_csv(self.log_file_path, index=False)

    def tearDown(self):
        # Clean up the dummy log file
        if os.path.exists(self.log_file_path):
            os.remove(self.log_file_path)

    def test_multiple_filters_are_extracted(self):
        # Analyze the dummy log file
        stats = analyze_log_file(self.log_file_path)

        # Check the results for the 'users' table
        self.assertIn('users', stats)
        self.assertIn('id', stats['users']['filters'])
        self.assertIn('name', stats['users']['filters'])
        self.assertIn('age', stats['users']['filters'])
        self.assertEqual(stats['users']['filters']['id'], 1)
        self.assertEqual(stats['users']['filters']['name'], 1)
        self.assertEqual(stats['users']['filters']['age'], 1)

        # Check the results for the 'products' table
        self.assertIn('products', stats)
        self.assertIn('category', stats['products']['filters'])
        self.assertIn('price', stats['products']['filters'])
        self.assertEqual(stats['products']['filters']['category'], 1)
        self.assertEqual(stats['products']['filters']['price'], 1)


if __name__ == '__main__':
    unittest.main()
