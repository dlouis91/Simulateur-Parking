import unittest
from Simulateur_parking import Parking

class TestParking(unittest.TestCase):
    def setUp(self):
        self.parking = Parking(2, 2)  # Parking avec 2 étages et 2 places par étage

    def test_initialisation(self):
        self.assertEqual(self.parking.places_libres, 4) # vérification 4 places libres a l'init


    def test_ajouter_voiture(self):
        result = self.parking.ajouter_voiture()
        self.assertEqual(result, (1, 1))
        self.assertEqual(self.parking.places_libres, 3) # verif si on ajoute 1 voiture, on a plus que 3 places

    def test_retirer_voiture(self):
        self.parking.ajouter_voiture(1, 1)
        result = self.parking.retirer_voiture(1, 1)
        self.assertTrue(result)
        self.assertEqual(self.parking.places_libres, 4) # verif si on ajoute et retire 1 voiture, on a 4 places

if __name__ == "__main__":
    unittest.main()
