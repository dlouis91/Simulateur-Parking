'''
simulation Parking
thinker + data base sqlite

'''

import tkinter as tk
from tkinter import messagebox

#database
import sqlite3    

#heure
from datetime import datetime

from tkinter import *

#simulation
import simpy

import random

#fonction systeme => sortir d'un code 
import sys

import re  #regular expression

#afficher information_gitba
class Debug:
    '''
        Class Debug - allows to pause the code 
        Debug.ss_pause(" message to be send ")
        
    '''


    def __init__(self):
        self.is_debug = False
        if self._is_debug:
            self.is_debug = True
         
    @classmethod        
    def get_function_name(cls, level = 1 ):
        import sys
        return sys._getframe(level).f_code.co_name
        '''
            Debug.ss_wait()
        '''
        menu_index = input(name)
        matchObj = re.search(r'([0-9]+)(d?)$', menu_index, re.M|re.I)      
        if(matchObj):
            return(True)

    @classmethod
    def ss_pause(self, msg = ""):
        '''
            Debug.ss_pause()
        '''
        method_name = Debug.get_function_name(level = 2)
        menu_index = input(f"pause {method_name} %s:" %(msg))
        matchObj = re.search(r'([0-9]+)(d?)$', menu_index, re.M|re.I)     
        if(matchObj):
            typ  = int(menu_index)
        else:
             typ  = int(1)
        #print(typ)
        return(typ)
        
   

class TimeConverter:
    def __init__(self, minutes):
        self.minutes = minutes

    def to_hours_and_minutes(self):
        hours = self.minutes // 60  # Division entière pour obtenir les heures
        remaining_minutes = self.minutes % 60  # Reste de la division pour les minutes
        return hours, remaining_minutes

    def __str__(self):
        hours, minutes = self.to_hours_and_minutes()
        return f"{self.minutes} minutes = {hours} heures et {minutes} minutes"

class CarApp:
    '''
        CarApp gere va générer aléatoirement le parking (acceptation voiture, refus, payment...)

        Chaque voiture cree possede une identification : car_id [1-1000]
        Chaque voiture va posseder une duree de presence dans le parking [minutes]
    '''
    def __init__(self):
        self.is_print = True
        CarApp.car_id = 0
        self.current_id = 0
        self.arrival_time = 50
        self.parking_duration = 60  # duree du paking 60mn pas defaut
        
        CarApp.nb_car = 0 
        CarApp.refused = 0
        CarApp.accepted = 0
        CarApp.payment = 0
        CarApp.list_accepted = []
        CarApp.is_debug = False
        if CarApp.is_debug:
            print("CarApp created", flush=True)
    def car(self, env, parking_app):
        #print("car", flush = True)
        '''
           à chaque iteration une voiture est creé avec:
            une identification
            une heure d'arrivée en mn
            une fois que la voiture arrive, elle essaye de rentrer dans le parking
            la voiture peut entrer dans le parking s'il y a des places disponibles
            la voiture va rester un certain temps dans le parking et va liberer une place à sa sortie
            
            Si le parking est plein la voiture est refusée
            Le temps d'arrivé d'une voiture est simulé par un yield
            Le temps d'attente est simule par un yielf
        '''
        nb_vehicule_linked  = 1
        while nb_vehicule_linked: 
            nb_vehicule_linked += -1
            CarApp.car_id += 1 
            CarApp.nb_car += 1
            parking_app.parking.total_car += 1  
            self.current_id = CarApp.car_id
            #attente 16 heures 
            self.arrival_time = random.randint(0, 60 * 20)
            #print(f"1: {self.current_id} arrival_time: {self.arrival_time}")
            yield env.timeout(self.arrival_time)
            #print(f"2: {self.current_id} arrival_time: {self.arrival_time}")
            if self.is_print:
                ''' on met-a-jour la database'''
                is_enter = parking_app.enter_car("car " + str(self.current_id))
                if is_enter:
                    if CarApp.is_debug:
                        print(f'Car {self.current_id} is parked at {env.now} mn', flush=True)
                    CarApp.accepted += 1
                    CarApp.list_accepted.append(self)
                    parking_app.parking.accepted += 1 
                    self.parking_duration = random.randint(15, 60 * 20)
                    #print("3 arrival_time: ", self.arrival_time)
                    yield env.timeout(self.parking_duration)
                    if CarApp.is_debug or False:
                        print(f'Car {self.current_id}  leaving at {env.now} mn', flush=True)
                    parking_app.exit_car(self.parking_duration, "car " + str(self.current_id))
                    
                else: #Si le parking est plein la voiture est refusée
                    if CarApp.is_debug:
                        print(f'Car {self.current_id} est repartie - parking plein {env.now}', flush=True)        
                    CarApp.refused += 1 
                    parking_app.parking.refused += 1 
                    
                    
                    #Debug.ss_pause()
        
class ParkingSimulation:
    '''
        ParkingSimulation represente une simulation de voitures qui arrivent dans un parking
        La durée de simulation est sur 24H
        On calcule le gain pour le parking
    
    '''
    def run_simulation(self, parking_app):
        '''
            Genere la simulation - on a fixer une simulation de 1000 voitures
            la simulation est terminée on affice les resultat
            On calcule le gain pour le parking 20 cts Euros par minutes
        '''
        print("run_simulation", flush=True)
        nb_car_in_simulation = 1000
        # Create the simulation environment
        env = simpy.Environment()
        car_obj = []
        for nb_car in range(nb_car_in_simulation):
            env.process(CarApp().car(env, parking_app))
            #parking_app.dessiner_parking()
        ''' La durée de simulation est sur 24H '''
        simulation_duration_mn = 24 * 60
        env.run(until=simulation_duration_mn)
        '''  la simulation est terminée on affice les resultat'''
        print("============ Simuation Terminated ==========")
        print("car refused:", CarApp.refused, flush=True)
        print("car accepted:", CarApp.accepted, flush=True)
        print("car total:", CarApp.nb_car, flush=True)
        
        ''' On calcule le gain pour le parking 20 cts Euros par minutes'''
        for car in CarApp.list_accepted:
            parking_app.parking.gain_parking += car.parking_duration * 0.02
        
        if False:
            for car in CarApp.list_accepted:
                print("car id :", car.current_id , flush=True)
                print(" car parking_duration:", car.parking_duration , flush=True)
                print(" car arrival_time:", car.arrival_time , flush=True)
                print("   ")

class Parking:
    '''        print("car refused:", CarApp.refused, flush=True)
        Class Parking controle le parking avec:
        Le nombre place occupées
        authorise une voiture a entrer
        met a jour la database
    
    '''
    def __init__(self, capacity, db_):
        """Initialisation du parking avec une capacité donnée."""
        self.capacity = capacity
        self.db = db_
        self.refused = 0
        self.accepted = 0
        self.total_car = 0
        self.money = 0
        self.gain_parking = 0
        self.places_occupees = self.get_places_occupees()
        
    def reset(self):
        '''
         intialise les valeurs des variables
        
        '''
        self.refused = 0
        self.accepted = 0
        self.total_car = 0
        self.gain_parking =0

    def get_places_occupees(self):
        """Récupère le nombre de places occupées dans la base de données."""
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM voitures")
        return cursor.fetchone()[0]
    
    def get_all_cars():
        cursor = db.cursor()
        cursor.execute('SELECT * FROM voitures')
        cars = cursor.fetchall()
        for car in cars:
            print(car)

    def entrer(self, voiture):
        """
    
        Ajoute une voiture dans le parking si des places sont disponibles
        mise a jour de la base de donnees.
        
        """
        #print(type(voiture))
        #Debug.ss_pause()
        if self.places_occupees < self.capacity:
            heure_entree = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor = db.cursor()
            ''' insere une ligne dans la data base'''
            cursor.execute("INSERT INTO voitures (nom_voiture, heure_entree) VALUES (?, ?)", (voiture, heure_entree))
            self.db.commit()
            self.places_occupees += 1
            return True
        else:
            return False

    def sortir(self, voiture):
        """
        Retire une voiture du parking  
        de la base de données si elle est présente. """
        cursor = self.db.cursor()
        ''' efface une ligne dans la data base'''
        cursor.execute("DELETE FROM voitures WHERE nom_voiture = ?", (voiture,))
        #print("===========> car  removed")
        if cursor.rowcount > 0:
            db.commit()
            #print("===========> removed")
            self.places_occupees += -1
            return True
        else:
            return False
        

    def get_voitures(self):
        """Récupère la liste des voitures présentes dans le parking. """
        cursor = self.db.cursor()
        cursor.execute("SELECT nom_voiture FROM voitures")
        return [row[0] for row in cursor.fetchall()]

    def empty_database(self):
        """ vide la base de données"""
        cursor = self.db.cursor()
        cursor.execute('DELETE FROM voitures')
        self.places_occupees = self.get_places_occupees()
        self.refused = 0
        self.accepted = 0
        self.total_car = 0
        self.gain_parking = 0
        db.commit()

class ParkingApp:
    '''
        Application User Interface du Parking
    
    '''
    def __init__(self, tk_app, parking):
        self.tk_app = tk_app
        self.parking = parking
        self.tk_app.title("Parking lot simulation")
        self.is_simulation_mode = False
        self.blick = False
        # Créer le menu
        menu_bar = Menu(self.tk_app)
        self.tk_app.config(menu=menu_bar)
       
        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Menu", menu=file_menu)
        file_menu.add_command(label="Static Mode", command = self.static_mode)
        file_menu.add_command(label="Empty Database", command = self.empty_database)
        file_menu.add_command(label="Quit", command = ParkingApp.quit)
        file_menu.add_command(label="Set Parking Capacity", command=self.set_parking_capacity)
        
        simu_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Simulation", menu=simu_menu)
        
        simu_menu.add_command(label="Simulation Mode", command = self.simulation_mode)

        menu_bar.add_command(label="Help", command=ParkingApp.help)
        
        spacer_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label=" " * 70, menu=spacer_menu)  # Espace pour décaler pour avoir About a droite
        
        about_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_command(label="About", command=ParkingApp.about)
       
        # Dimensions du parking graphique
        self.place_width = 80
        self.place_height = 40
        self.padding = 10  # Espace entre les places de parking
        self.places_per_row = 5  # Nombre de places par ligne pour une disposition améliorée

        # Draw parking lot
        canvas_width = self.places_per_row * (self.place_width + self.padding)
        canvas_height = ((self.parking.capacity // self.places_per_row) + 1) * (self.place_height + self.padding)
        self.canvas = tk.Canvas(tk_app, width=canvas_width, height=canvas_height, bg='white')
        self.canvas.pack(pady=20)

        # Étiquette du titre
        self.title_label = tk.Label(tk_app, text="Parking Simulation", font=("Arial", 14, "bold"))
        self.title_label.pack(pady=5)
        

        if False:
            # Champ pour l'entrée de la voiture
            self.voiture_label = tk.Label(tk_app, text="Entrez le nom de la voiture :", font=("Arial", 12))
            self.voiture_label.pack()

        if False:
            self.voiture_entry = tk.Entry(tk_app, font=("Arial", 12))
            self.voiture_entry.pack(pady=5)

        if False:
            # Bouton pour faire entrer une voiture
            self.entrer_button = tk.Button(tk_app, text="Entrer Voiture", font=("Arial", 12), command=self.entrer_voiture)
            self.entrer_button.pack(pady=5)

        if False:
            # Bouton pour faire sortir une voiture
            self.sortir_button = tk.Button(tk_app, text="Sortir Voiture", font=("Arial", 12), command=self.sortir_voiture)
            self.sortir_button.pack(pady=5)
        if True:
            # Étiquette pour afficher l'état du parking
            self.etat_label = tk.Label(tk_app, text="", font=("Arial", 10))
            self.etat_label.pack( pady=3)

           
            
        if True:


            frame_labels = tk.Frame(tk_app)
            frame_labels.pack(side="left", padx=10, pady=5)  # Ajoute un cadre pour les marges

            # Étiquette pour afficher le nombre total de voitures
            self.label_total_car = tk.Label(frame_labels, text="", font=("Arial", 10))
            self.label_total_car.pack(side="top", anchor="w", pady=0)
            # Étiquette pour afficher le nombre de voitures refusées
            self.label_refused_car = tk.Label(frame_labels, text="", font=("Arial", 10))
            self.label_refused_car.pack(side="top", anchor="w", pady=0)  # 'anchor="w"' pour aligner à gauche dans le cadre

            # Étiquette pour afficher le nombre de voitures acceptées
            self.label_accepted_car = tk.Label(frame_labels, text="", font=("Arial", 10))
            self.label_accepted_car.pack(side="top", anchor="w", pady=0)
            
            # Étiquette pour afficher le nombre de voitures acceptées
            self.label_gain_parking = tk.Label(frame_labels, text="", font=("Arial", 10))
            self.label_gain_parking.pack(side="top", anchor="w", pady=0)           
            
        # Dessin initial du parking
        
        self.dessiner_parking()


    def set_parking_capacity(self):
        # Créer une nouvelle fenêtre
        capacity_window = Toplevel(self.tk_app)
        capacity_window.title("Set Parking Capacity")
        
        # Créer l'interface dans la fenêtre
        Label(capacity_window, text="Enter parking capacity:").pack(pady=10)
        capacity_entry = Entry(capacity_window)
        capacity_entry.pack(pady=5)
        
        def save_capacity():
            try:
                # Essayer de convertir l'entrée en entier
                capacity = int(capacity_entry.get())
                if capacity < 0:
                    raise ValueError("Capacity cannot be negative")
                # Stocker la capacité (par exemple, dans un attribut de l'objet)
                self.parking.capacity = capacity
                messagebox.showinfo("Success", f"Parking capacity set to {capacity}")
                capacity_window.destroy()
            except ValueError as e:
                messagebox.showerror("Invalid Input", f"Please enter a valid positive integer.\n{e}")
        
        # Bouton pour sauvegarder la capacité
        Button(capacity_window, text="Save", command=save_capacity).pack(pady=10)

    def help():
        aide_window = Toplevel(tk_app)
        aide_window.title("Help")
        
    
        texte_aide = '''
        Bienvenue dans le simulateur de parking !
        
        - Appuyez sur "Simulation" pour générer une simulation de voitures dans un parking sur 24h.
        - La simulation représente des voitures arrivant dans un parking de manière aléatoire 
        et restant pour une durée aléatoire.
        - Si le parking est plein, la voiture est refusée.
        - Le prix est proportionnel à la durée de présence dans le parking.
        - Les voitures résidant dans le parking sont représentées en bleu.
        
        - La capacité du parking peut etre changé
        '''


        label_aide = tk.Label(aide_window, text=texte_aide, font=("Arial", 10), justify="left", padx=10, pady=10)
        label_aide.pack(fill="both", expand=True)


    def display_simulation_result(self):
        aide_window = Toplevel(tk_app)
        aide_window.title("Simulation Result")
        texte_aide = '''
        Display simulation result

    '''
    
        label_aide = Label(aide_window, text=texte_aide)
        label_aide.pack(padx=20, pady=20)



    def simulation_mode(self):
        '''
            On active la simulation
            On vide la la database
            tant que ce sous menu ne fini pas le parking ne sera pas mis a jour
        '''
        print("simulation_mode", flush = True)
        self.is_simulation_mode = True
        parking_app_obj = self
        self.parking.empty_database()
        self.parking.reset()
        app.blick = True
        self.dessiner_parking()
        #Debug.ss_pause()
        #new_simulation = ParkingSimulation()
        #new_simulation.run_simulation(parking_app_obj)
        #self.is_simulation_mode = False
        
    def static_mode(self):
        '''
        Pour tester l'entrée des vehicules dans le parking
        Pour du debug 
        
        '''
        duration = 60
        self.exit_car("car 3", duration)
        self.exit_car("car 2", duration)
        self.exit_car("car 1", duration)

        self.enter_car("car 1")
        self.enter_car("car 2")
        self.enter_car("car 3")
        Parking.get_all_cars()

    def empty_database(self):
        '''
            vide la database
        '''
        self.parking.empty_database()
        self.dessiner_parking()

    def quit():
        '''
            methode pour quitter le programme
        '''
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            tk_app.destroy()       
            
    def about():
        '''
            method pour afficher les informations sur le createur
        '''
        about_window = Toplevel(tk_app)
        about_window.title("About")
        about_txt = '''
        Author: Alexandre Sintes
        Code Simulation Parking disponible sur Github
        version 1.0 2024


    '''
    
        label_about = Label(about_window, text=about_txt)
        label_about.pack(padx=20, pady=20)   
            
    def dessiner_parking(self):
        """
        Dessine les places de parking sur le canvas 
        Chaque place de parking est representé par un rectangle
        Sur les place de parking on dessine les voitures (en bleue) qui sont actuelement dans le parking
        On les dessines dans l'ordre en prenant l'hypothese que les vehicules se gare dans l'order
        """
        self.canvas.delete("all")  # Efface le dessin précédent
        voitures = self.parking.get_voitures()  # de l'object parking on recupere la liste des voitures présentes dans le parking 
        
        delta_x_y = 5
        for i in range(self.parking.capacity):
            row = i // self.places_per_row
            col = i % self.places_per_row
            x1 = col * (self.place_width + self.padding)
            y1 = row * (self.place_height + self.padding)
            x2 = x1 + self.place_width
            y2 = y1 + self.place_height
            self.canvas.create_rectangle(x1+delta_x_y, y1+delta_x_y, x2+delta_x_y, y2+delta_x_y, outline="black", fill="lightgray")
            
            if i < len(voitures):
                # Dessine une voiture sous forme de rectangle en bleu
                self.canvas.create_rectangle(x1 + 10 + delta_x_y, y1 + 5 +delta_x_y , x2 - 10+ delta_x_y, y2 - 5+ delta_x_y, outline="black", fill="blue")
                self.canvas.create_text(x1 + delta_x_y + self.place_width // 2, y1 +delta_x_y + self.place_height // 2, text=voitures[i], fill="white")

        # Mise à jour de l'indicateur visuel des places occupées
        self.update_etat()

    def entrer_voiture(self):
        voiture = self.voiture_entry.get()
        if voiture:
            if self.parking.entrer(voiture):
                self.dessiner_parking()
                messagebox.showinfo("Succès", f"La voiture {voiture} est entrée dans le parking.")
            else:
                messagebox.showwarning("Erreur", "Le parking est plein. Aucune place disponible.")
        else:
            messagebox.showwarning("Erreur", "Veuillez entrer un nom de voiture.")
            
    def enter_car(self, car_name):
        '''
            car_name string
        
        '''
        is_enter = self.parking.entrer(car_name)
        self.dessiner_parking()
        #Debug.ss_pause()
        return(is_enter)
        #messagebox.showinfo("Succès", f"La voiture  est entrée dans le parking.")

    def exit_car(self, duration, car_name):
        #print("exit_v", flush=True)
        self.parking.sortir(car_name)
        

        #self.parking.to_pay(car_name, duration)
        self.dessiner_parking()
        
    def sortir_voiture(self):
        voiture = self.voiture_entry.get()
        if voiture:
            if self.parking.sortir(voiture):
                self.dessiner_parking()
                messagebox.showinfo("Succès", f"La voiture {voiture} est sortie du parking.")
            else:
                messagebox.showwarning("Erreur", f"La voiture {voiture} n'est pas dans le parking.")
        else:
            messagebox.showwarning("Erreur", "Veuillez entrer un nom de voiture.")

    def update_etat(self):
        """Met à jour l'indicateur visuel de l'état du parking."""
        places_libres = self.parking.capacity - self.parking.places_occupees
        etat = f"Places occupées : {self.parking.places_occupees}/{self.parking.capacity}"
        etat_couleur = "green" if places_libres > 5 else "orange" if places_libres > 2 else "red"
        self.etat_label.config(text=etat, fg=etat_couleur)
        
        etat_refused = f"Refused Cars {self.parking.refused}"
        self.label_refused_car.config(text=etat_refused)
        
        etat_accepted = f"Accepted Cars {self.parking.accepted}"
        self.label_accepted_car.config(text=etat_accepted)       
        
        etat_total_car = f"Total Cars {self.parking.total_car}"
        self.label_total_car.config(text=etat_total_car)
        
        etat_gain_parking = f"Gain Parking {self.parking.gain_parking:.2f} €"
        self.label_gain_parking.config(text=etat_gain_parking)    
        
        
        
        if self.is_simulation_mode:
            if self.blick:
                state_simulation_mode =  f"Simulation Mode in progress"
                self.title_label.config (text=state_simulation_mode)
                self.blick = False
            else:
                state_simulation_mode =  f""
                self.title_label.config (text=state_simulation_mode)
                self.blick = True
        else:
            self.blick = False
            state_simulation_mode =  f"Simulation Mode"
            self.title_label.config (text=state_simulation_mode)
            self.blick = False    
        
class DataBase:
    '''   DataBase  sqlite3'''
    def connect(database_name):
        # Connexion à la base de données SQLite (ou création si elle n'existe pas)
        db = sqlite3.connect(database_name)
        cursor = db.cursor()

        # Création de la table pour les voitures si elle n'existe pas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS voitures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_voiture TEXT,
                heure_entree TEXT
            )
        ''')
        db.commit()
        return(db)

def update_timer():
    '''
            fontion appelée chqaue seconde
            met à jour l' affichage chaque seconde dans l'application Tkinter sans bloquer l’interface.
            Toute les secondes on redessine le parking
    '''
     #print("1 seconde", flush=True)
     
    ''' on verifie si on a demandé une simulation '''
    if app.is_simulation_mode:
        app.blick = True
        ''' on execute une simulation'''
        new_simulation = ParkingSimulation()
        new_simulation.run_simulation(app)
        #app.display_simulation_result()
        app.is_simulation_mode = False
    '''  on redessine le parking '''
    app.dessiner_parking()
    ''' on rapelle la fonction dans une seconde '''
    tk_app.after(1000, update_timer)  # Met à jour toutes les secondes 



############################   
if __name__ == "__main__":
    ''' Connection à la  base de données'''
    db  = DataBase.connect('parking2.db')

    # Simulation avec une capacité de 25 places
    parking = Parking(25, db)

    # Création de l'application Tkinter pour visuliser le parking
    tk_app = tk.Tk()

    app = ParkingApp(tk_app, parking)  #instance of parking
    
    # on utilise un timer qui va m.a.j le parking
    update_timer()
    
    # application est exectuter il faut faire quit a partir du menu pour sortir ou utiliser la croix dla fenetre 
    tk_app.mainloop()

    # Fermeture de la connexion à la base de données lorsque l'application est terminée
    db.close()

