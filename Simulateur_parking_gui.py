import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import time


class ParkingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Simulateur de Parking Amélioré")

        # Initialiser un style moderne avec ttk
        style = ttk.Style()
        style.theme_use("clam")
        self.master.configure(bg="#f7f7f7")

        # Variables de stationnement
        self.entry_times = {}  # Pour stocker les heures d'arrivée
        self.vehicle_type = tk.StringVar(value="Voiture")

        # Demander la taille du parking
        self.etages = simpledialog.askinteger("Configuration", "Entrez le nombre d'étages :", minvalue=1)
        self.places_par_etage = simpledialog.askinteger("Configuration", "Entrez le nombre de places par étage :",
                                                        minvalue=1)
        if self.etages is None or self.places_par_etage is None:
            messagebox.showerror("Erreur", "Configuration annulée. L'application va se fermer.")
            master.destroy()
            return

        # Initialiser le parking
        self.parking = [[False] * self.places_par_etage for _ in range(self.etages)]

        # Dimensions et espacement des cases
        self.case_width = 40
        self.case_height = 30
        self.etage_spacing = 10

        # Configurer le canvas avec un cadre
        canvas_width = self.places_par_etage * self.case_width
        canvas_height = self.etages * (self.case_height + self.etage_spacing)
        self.canvas_frame = tk.Frame(self.master, bg="gray", bd=2, relief="sunken")
        self.canvas = tk.Canvas(self.canvas_frame, width=canvas_width, height=canvas_height, bg="lightgrey")
        self.canvas.pack(padx=10, pady=10)
        self.canvas_frame.pack(pady=10)

        # Créer le label pour les informations de tarif et de durée
        self.info_label = ttk.Label(self.master, text="Tarif: 2€/h | 1 heure = 10 secondes",
                                    font=("Helvetica", 10, "italic"))
        self.info_label.pack(pady=5)

        # Créer les contrôles
        self.create_controls()
        self.update_places_disponibles()
        self.draw_parking()
    def create_controls(self):
        # Contrôles d'ajout de véhicule
        self.controls_frame = ttk.Frame(self.master)
        self.controls_frame.pack(pady=10)

        self.add_label = ttk.Label(self.controls_frame, text="Ajouter (Étage, Place) :")
        self.add_label.grid(row=0, column=0, padx=5)

        self.add_etage = ttk.Entry(self.controls_frame, width=3)
        self.add_etage.grid(row=0, column=1, padx=5)

        self.add_place = ttk.Entry(self.controls_frame, width=3)
        self.add_place.grid(row=0, column=2, padx=5)

        self.vehicle_menu = ttk.OptionMenu(self.controls_frame, self.vehicle_type, "Voiture", "Voiture", "Moto",
                                           "Camion")
        self.vehicle_menu.grid(row=0, column=3, padx=5)

        self.add_button = ttk.Button(self.controls_frame, text="Ajouter", command=self.add_car)
        self.add_button.grid(row=0, column=4, padx=5)

        # Contrôle pour retirer le véhicule
        self.remove_label = ttk.Label(self.controls_frame, text="Retirer (Étage, Place) :")
        self.remove_label.grid(row=1, column=0, padx=5)

        self.remove_etage = ttk.Entry(self.controls_frame, width=3)
        self.remove_etage.grid(row=1, column=1, padx=5)

        self.remove_place = ttk.Entry(self.controls_frame, width=3)
        self.remove_place.grid(row=1, column=2, padx=5)

        self.remove_button = ttk.Button(self.controls_frame, text="Retirer", command=self.remove_car)
        self.remove_button.grid(row=1, column=4, padx=5)

        # Label d'affichage des places disponibles
        self.places_disponibles_label = ttk.Label(self.master, text="", font=("Helvetica", 12, "bold"))
        self.places_disponibles_label.pack(pady=5)

    def draw_parking(self):
        self.canvas.delete("all")

        for etage in range(self.etages):
            for place in range(self.places_par_etage):
                x1 = place * self.case_width
                y1 = etage * (self.case_height + self.etage_spacing)
                x2 = x1 + self.case_width
                y2 = y1 + self.case_height

                occupied = self.parking[etage][place]
                color = "green" if not occupied else "red"
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

                # Associer le clic pour ajouter/retirer
                self.canvas.tag_bind(rect, "<Button-1>",
                                     lambda event, e=etage + 1, p=place + 1: self.toggle_place(e, p))

                # Afficher le numéro de la place
                self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=f"{etage + 1}-{place + 1}", fill="white")

    def add_car(self):
        try:
            etage = int(self.add_etage.get())
            place = int(self.add_place.get())
            vehicle = self.vehicle_type.get()

            if not (1 <= etage <= self.etages) or not (1 <= place <= self.places_par_etage):
                messagebox.showerror("Erreur", "Place inexistante.")
                return

            if self.parking[etage - 1][place - 1]:
                messagebox.showerror("Erreur", "Place déjà occupée.")
                return

            self.parking[etage - 1][place - 1] = True
            self.entry_times[(etage, place)] = time.time()
            self.update_places_disponibles()

        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des numéros valides pour l'étage et la place.")

    def remove_car(self):
        try:
            etage = int(self.remove_etage.get())
            place = int(self.remove_place.get())
            if not (1 <= etage <= self.etages) or not (1 <= place <= self.places_par_etage):
                messagebox.showerror("Erreur", "Place inexistante.")
                return

            if not self.parking[etage - 1][place - 1]:
                messagebox.showerror("Erreur", "Aucun véhicule à retirer ici.")
                return

            self.parking[etage - 1][place - 1] = False
            entry_time = self.entry_times.pop((etage, place), None)
            if entry_time:
                # Calculer la durée de stationnement avec 1 heure = 10 secondes
                duration = time.time() - entry_time
                hours = duration // 10  # Chaque "heure" est de 10 secondes
                cost = hours * 2  # Tarif de 2€ par heure
                messagebox.showinfo("Coût", f"Durée : {int(hours)} h. Coût : {cost} €")
            self.update_places_disponibles()

        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des numéros valides pour l'étage et la place.")

    def toggle_place(self, etage, place):
        if self.parking[etage - 1][place - 1]:
            self.remove_car()
        else:
            self.add_car()

    def update_places_disponibles(self):
        places_libres = sum(row.count(False) for row in self.parking) #calcul des places libres
        total_places = self.etages * self.places_par_etage
        self.places_disponibles_label.config(text=f"Places disponibles : {places_libres}/{total_places}") #maj du label
        self.draw_parking()


if __name__ == "__main__":
    root = tk.Tk()
    app = ParkingApp(root)
    root.mainloop()
