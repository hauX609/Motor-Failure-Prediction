import unittest
from sklearn.ensemble import RandomForestClassifier
from src.model_training import train_model, evaluate_model

class TestModelTraining(unittest.TestCase):

    def setUp(self):
        self.X_train = [[1, 1000, 30, 50, 10, 5.0, 20, 0.1],
                        [2, 1500, 35, 55, 15, 6.0, 25, 0.2],
                        [1, 1200, 32, 52, 12, 5.5, 22, 0.15],
                        [2, 1300, 33, 53, 13, 5.8, 23, 0.18]]
        self.y_train = [0, 1, 0, 1]
        self.X_test = [[1, 1100, 31, 51, 11, 5.2, 21, 0.12]]
        self.y_test = [0]

    def test_train_model(self):
        model = train_model(self.X_train, self.y_train)
        self.assertIsInstance(model, RandomForestClassifier)

    def test_evaluate_model(self):
        model = train_model(self.X_train, self.y_train)
        report = evaluate_model(model, self.X_test, self.y_test)
        self.assertIn('precision', report)

if __name__ == '__main__':
    unittest.main()
