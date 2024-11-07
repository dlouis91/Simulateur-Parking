class Parking:
    def __init__(self, etages, places_par_etage):
        self.etages = etages
        self.places_par_etage = places_par_etage
        # Initialiser le parking avec toutes les places libres (False = Libre, True = Occupée)
        self.places = [[False for _ in range(places_par_etage)] for _ in range(etages)]
        self.total_places = etages * places_par_etage
        self.places_libres = self.total_places

    def afficher_parking(self):
        """affiche l'etat actuel du parking, les places libres et occupées par étage"""
        print(f"Places libres : {self.places_libres}/{self.total_places}")
        for etage in range(self.etages):
            print(f"Étage {etage+1} : ", end="")
            for place in range(self.places_par_etage):
                etat = "Libre" if not self.places[etage][place] else "Occupée"
                print(f"[{etat}]", end=" ")
            print()  # Pour passer à la ligne suivante après un étage
        print()

    def parking_plein(self):
        if self.places_libres==0:
            print("Le parking est complet")

    def ajouter_voiture(self, etage=None, place=None):
        # Vérifie si le parking est complet
        if self.parking_plein():
            return False  # Indique que le parking est plein

        # Si un étage et une place sont spécifiés
        if etage is not None and place is not None:
            if etage < 0 or place < 0 or etage > self.etages or place > self.places_par_etage:
                print("Erreur, cette place n existe pas")
                return None

            # Ajustement des indices pour correspondre aux listes (qui commencent à 0)
            etage -= 1
            place -= 1

            # Vérifie si la place est libre
            if not self.places[etage][place]:
                self.places[etage][place] = True
                self.places_libres -= 1
                return (etage + 1, place + 1)  # Retourne le résultat en format humain (commençant à 1)
            else:
                return None  # Indique que la place est déjà occupée

        # Si l'utilisateur ne spécifie pas de place, recherche la première place libre
        for e in range(self.etages):
            for p in range(self.places_par_etage):
                if not self.places[e][p]:  # Trouve la première place libre
                    self.places[e][p] = True
                    self.places_libres -= 1
                    return (e + 1, p + 1)

        return False  # Cas ou aucune place libre n'est trouvée

    def retirer_voiture(self, etage, place):
        """retire la voiture à l'emplacement indiqué"""
        #pour ajuster les indices
        etage-=1
        place-=1
        if etage < 0 or etage >= self.etages or place < 0 or place >= self.places_par_etage:
            print("Erreur, la place indiquée n'existe pas")
            return
        if self.places[etage][place] is False:
            print("Attention, aucune voiture n'est garée a cette place")
            return False
        if self.places[etage][place]:
            self.places[etage][place]=False
            self.places_libres +=1
            print(f"Voiture retirée de l'étage {etage+1}, place {place+1}")
            return True

    def get_status(self):
        """Retourne l'état actuel des places du parking"""
        return self.places

if __name__ == "__main__":
    while True:
        try:
            etages = int(input("Entrez le nombre d'étages : "))
            places_par_etage = int(input("Entrez le nombre de places par étage : "))
            break
        except ValueError:
            print("Veuillez entrer des nombres valides.")

    parking = Parking(etages, places_par_etage)
    while True:
        print("\nOptions: 1) Afficher parking 2) Ajouter voiture 3) Retirer voiture 4) Quitter")
        choix = input("Choisissez une option: ")
        if choix == '1':
            parking.afficher_parking()
        elif choix == '2':
            etage = input("Étage (ou vide pour automatique) : ")
            place = input("Place (ou vide pour automatique) : ")
            etage = int(etage) if etage else None
            place = int(place) if place else None
            parking.ajouter_voiture(etage, place)
        elif choix == '3':
            try:
                etage = int(input("Étage : "))
                place = int(input("Place : "))
                parking.retirer_voiture(etage, place)
            except ValueError:
                print("Veuillez entrer des nombres valides.")
        elif choix == '4':
            break
        else:
            print("Option invalide.")

"""parking=Parking(2,6)
parking.afficher_parking()
parking.ajouter_voiture(2,1)
parking.afficher_parking()
parking.retirer_voiture(2,1)
parking.afficher_parking()"""