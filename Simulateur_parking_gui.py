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

