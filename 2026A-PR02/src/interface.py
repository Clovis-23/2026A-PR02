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

    
    