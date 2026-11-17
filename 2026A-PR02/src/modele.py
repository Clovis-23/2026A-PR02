from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib
import json
import pandas as pd 
import numpy as np
import os

class ModeleNBA:

    def __init__(self):
        self.modele= LinearRegression()
        dossier_script = os.path.dirname(__file__)
        self.racine_projet = os.path.dirname(dossier_script)


    def getdummies(self,data,colonne ):
        self.colonne_int= pd.get_dummies(data[colonne],dtype=int)
        
        return self.colonne_int
    

    def preparer_donnees(self):

        chemin=os.path.join(self.racine_projet,"donnees","nba_nettoye.csv")

        if not os.path.exists(chemin):
            raise FileNotFoundError("Le fichier NBA est introuvable")
        with open(chemin, "r", encoding="utf-8") as f:
            self.donnes = pd.read_csv(f)
        X=self.donnes[['season_year', 'pos', 'age', 'games', 'minutes_per_game', '2pa', '3pa', 'trb', 'ast', 'stl', 'tov']]
        Y= self.donnes['pts']    
        pos_int=self.getdummies(self.donnes,'pos')  
        X=X.drop(columns=['pos']) 
        X=pd.concat([X,pos_int], axis=1)
         
        return X, Y