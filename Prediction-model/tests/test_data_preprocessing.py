import unittest
import pandas as pd
from src.data_preprocessing import load_data, preprocess_data, split_data

class TestDataPreprocessing(unittest.TestCase):

    def setUp(self):
        self.data_path = '/home/user/motor_failure_prediction/data/motor_data.csv'
        self.data = load_data(self.data_path)

    def test_load_data(self):
        self.assertIsInstance(self.data, pd.DataFrame)

    def test_preprocess_data(self):
        preprocessed_data = preprocess_data(self.data)
        self.assertFalse(preprocessed_data.isnull().values.any())

    def test_split_data(self):
        preprocessed_data = preprocess_data(self.data)
        X_train, X_test, y_train, y_test = split_data(preprocessed_data, 'failure_type')
        self.assertEqual(len(X_train), len(y_train))
        self.assertEqual(len(X_test), len(y_test))

if __name__ == '__main__':
    unittest.main()
