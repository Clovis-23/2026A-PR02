import os
import json
import math
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

dossier_script = os.path.dirname(__file__)
racine_projet = os.path.dirname(dossier_script)


CHAMPS_NUMERIQUES = {
    "season_year": "Année de la saison",
    "age": "Âge du joueur",
    "games": "Nombre de matchs dans la saison",
    "minutes_per_game": "Minutes par match",
    "2pa": "Tirs à 2 points tentés par match",
    "3pa": "Tirs à 3 points tentés par match",
    "trb": "Rebonds par match",
    "ast": "Passes décisives par match",
    "stl": "Interceptions par match",
    "tov": "Balles perdues par match",
}
CHAMPS_ENTIERS = {"season_year", "age", "games"}

class Application :
    def __init__ (self) :
        # Ici, on charge le modèle déjà entraîné.
        from modele import ModeleNBA

        self.modele = ModeleNBA()
        self.modele.charger()

        chemin_metadata = os.path.join(racine_projet, "donnees", "metadata.json")
        with open(chemin_metadata, "r", encoding="utf-8") as fichier:
            self.metadata = json.load(fichier)

    def __str__ (self) :
        if self.modele is None:
            return "Modele pas encore chargé"
        return "Modele chargé"

    def predire_profil (self, joueur) :
        prediction = self.modele.predire(joueur)
        pass
    
    def consulter_historique(self) :
        """Renvoie l'historique, ou None s'il n'y en a pas encore."""
        if not os.path.exists(self.chemin_historique):
            return None
        return pd.read_csv(self.chemin_historique)

    def enregistrer_prediction(self, nom_joueur, joueur, prediction) :
            nouvelle_ligne = joueur.copy()
            nouvelle_ligne["nom_joueur"] = nom_joueur
            nouvelle_ligne["points prédits"] = prediction
            ligne_final = pd.DataFrame([nouvelle_ligne])
    
            historique = self.consulter_historique()
            if historique is None :
                historique = ligne_final
            else :
                historique.append(nouvelle_ligne)
            return historique

    def retirer_ligne_histo(self, numero_ligne):
        historique = self.consulter_historique()
        if historique is None:
            return False
        if numero_ligne < 0 or numero_ligne >= len(historique):
            return False

        historique = historique.drop(index=numero_ligne).reset_index(drop=True)
        historique.to_csv(self.chemin_historique, index=False)
        return True

#on passe a l'interface pur avec streamlit

def effacer_resultat():
    if "derniere_prediction" in st.session_state:
        del st.session_state["derniere_prediction"]

def saisir_un_nombre (application, colonne, texte) :
    intervalle = application.metadata["intervalles"][colonne]
    minimum = intervalle["min"]
    maximum = intervalle["max"]
    entier = colonne in CHAMPS_ENTIERS
    return st.number_input(
        texte,
        min_value=int(minimum) if entier else float(minimum),
        max_value=int(maximum) if entier else float(maximum),
        value=int(minimum) if entier else float(minimum),
        step=1 if entier else 0.1,
        key=colonne,
        help=f"Valeur attendue entre {minimum} et {maximum}.",
        on_change=effacer_resultat)

def valider_joueur(joueur: dict, metadata: dict) :
    profil = joueur.copy()
    for colonne, nom in CHAMPS_NUMERIQUES.items():
        valeur = joueur[colonne]
        minimum = metadata["intervalles"][colonne]["min"]
        maximum = metadata["intervalles"][colonne]["max"]
        if valeur < minimum or valeur > maximum:
            raise ValueError(f"{nom} : entrez une valeur entre {minimum} et {maximum}.")
        profil[colonne] = valeur
    return profil


def graphique(nom_joueur: str, prediction: float) -> plt.Figure:
    """Renvoie le graphique. Échoue si le CSV est absent ou invalide."""
    chemin = os.path.join(racine_projet, "donnees", "nba_joueur_saison_2005_2024.csv")
    if not os.path.exists(chemin):
        raise FileNotFoundError("Le fichier nba_joueur_saison_2005_2024.csv est introuvable.")
    df = pd.read_csv(chemin)
    figure, ax = plt.subplots()
    ax.hist(df["pts"], bins=20)
    ax.axvline(prediction, color="red", linestyle="--", label=f"{nom_joueur} : {prediction:.2f} points")
    ax.set_title("Distribution des points par match")
    ax.set_xlabel("Points par match")
    ax.set_ylabel("Nombre de joueurs-saisons")
    ax.legend() 
    return figure 