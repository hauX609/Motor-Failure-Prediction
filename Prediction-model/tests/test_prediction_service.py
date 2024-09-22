import unittest
from src.prediction_service import calculate_energy_consumption, provide_recommendations

class TestPredictionService(unittest.TestCase):

    def test_calculate_energy_consumption(self):
        current = 5.5
        voltage = 220
        time = 2
        energy_consumption, power = calculate_energy_consumption(current, voltage, time)
        self.assertEqual(energy_consumption, 2420.0)
        self.assertEqual(power, 1210.0)

    def test_provide_recommendations(self):
        recommendation = provide_recommendations(0)
        self.assertEqual(recommendation, "Check motor bearings and lubrication.")

if __name__ == '__main__':
    unittest.main()
