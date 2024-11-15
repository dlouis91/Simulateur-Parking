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


