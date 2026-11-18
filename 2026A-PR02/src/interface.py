import os
import json
import math
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

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