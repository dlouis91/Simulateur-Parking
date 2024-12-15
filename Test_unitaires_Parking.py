import unittest
from Simulateur_parking import Parking

class TestParking(unittest.TestCase):
    def setUp(self):
        self.parking = Parking(2, 2)  # Parking avec 2 étages et 2 places par étage

    def test_initialisation(self):
        self.assertEqual(self.parking.places_libres, 4)

    def test_ajouter_voiture(self):
        result = self.parking.ajouter_voiture()
        self.assertEqual(result, (1, 1))
        self.assertEqual(self.parking.places_libres, 3)

    def test_retirer_voiture(self):
        self.parking.ajouter_voiture(1, 1)
        result = self.parking.retirer_voiture(1, 1)
        self.assertTrue(result)
        self.assertEqual(self.parking.places_libres, 4)

if __name__ == "__main__":
    unittest.main()
