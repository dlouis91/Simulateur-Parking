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
        if self.parking_plein():
            print("Le parking est complet")
            return


        # si un etage et une place sont choisis
        if etage is not None and place is not None:
            if etage < 0 or place < 0 or etage > self.etages or place > self.places_par_etage:
                print("Erreur, cette place n existe pas")
                return

            etage-=1
            place-=1
            if self.places[etage][place] is False:
                self.places[etage][place]= True
                self.places_libres -= 1
                print(f"la voiture est garée à l'étage {etage+1}, place {place+1}")
            else:
                print(f"La place à l'étage {etage+1}, place {place+1} est déjà occupée")

        # si l'utilisateur ne choisis pas de place
        else:
            for e in range(self.etages):
                for p in range(self.places_par_etage):
                    if not self.places[e][p]:
                        self.places[e][p]=True
                        self.places_libres -= 1
                        print(f"la voiture est garée à l'étage {e+1}, place {p+1}")
                        return

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
        if self.places[etage][place]:
            self.places[etage][place]=False
            self.places_libres +=1
            print(f"Voiture retirée de l'étage {etage+1}, place {place+1}")


parking=Parking(2,6)
parking.afficher_parking()
parking.ajouter_voiture(2,1)
parking.afficher_parking()
"""parking.retirer_voiture(2,3)
parking.afficher_parking()"""

"""parking.ajouter_voiture(2,4)
parking.retirer_voiture(2,3)
parking.afficher_parking()
parking.retirer_voiture(4,7)
parking.afficher_parking()
parking.retirer_voiture(1,2)"""



