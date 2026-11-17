from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib
import json
import pandas as pd 
import numpy as np
import os
from exceptions import Erreur_structure_de_donnes, Valeur_hors_norme, CategorieInvalide

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
    
    def evaluer(self):
        
        predictions = self.modele.predict(self.X_test)    
        mae = mean_absolute_error(self.Y_test, predictions)
        moy= self.Y_train.mean()
        predictions_baseline=[moy for joueur in self.Y_test]
        mae_baseline = mean_absolute_error(self.Y_test, predictions_baseline )
        mae_verif=np.abs(self.Y_test - predictions).mean()
        verification= np.isclose(mae,mae_verif)
        
        return mae,mae_baseline, verification
    def entrainer(self):
            X,Y= self.preparer_donnees()
            X_train, X_test, Y_train, Y_test = train_test_split(
            X, Y,
            test_size=0.2,
            random_state=42
            )
            self.modele.fit(X_train, Y_train)
            self.X_train=X_train
            self.X_test=X_test
            self.Y_train=Y_train
            self.Y_test=Y_test
            return X_train, X_test
        
    def sauvegarder(self):
            chemin= os.path.join(self.racine_projet,"modeles" )
            os.makedirs(chemin, exist_ok=True)

            chemin_sauvegarde = os.path.join(chemin, "modele_nba.joblib")

            joblib.dump(self.modele, chemin_sauvegarde)

    def sauvegarder_metadata(self):

        mae,mae_baseline, verification=self.evaluer()
        X,Y= self.preparer_donnees()
        colonnes = X.columns.tolist()
        intervalles={}
        for colonne in X:
            intervalles[colonne]={
            'min':float(X[colonne].min()),
            'max':float(X[colonne].max())
            }
        positions = self.donnes['pos'].unique().tolist()
        metadata={"colonnes": colonnes, "mae": float(mae) ,   "intervalles": intervalles
        , "categories":positions
            }
        chemin_racine= os.path.join(self.racine_projet, 'donnees')
        os.makedirs(chemin_racine, exist_ok=True)
        chemin= os.path.join(chemin_racine, 'metadata.json')
        with open(chemin, "w") as f:
            json.dump(metadata, f, indent=4)        

    def charger(self):

        chemin=os.path.join(self.racine_projet,'modeles','modele_nba.joblib' )
        if not os.path.exists(chemin):
            raise FileNotFoundError("Le fichier modele_nba est introuvable")
        self.modele= joblib.load(chemin)

    def predire(self, joueur):
        variables = [ 'season_year', 'pos', 'age', 'games', 'minutes_per_game', '2pa', '3pa','trb', 'ast', 'stl', 'tov' ]
        chemin= os.path.join(self.racine_projet,'donnees','metadata.json')

        if not os.path.exists(chemin):
            raise FileNotFoundError(f"Le fichier metadata.json n'existe pas")
        with open(chemin, "r") as f:
            dictionnaire=json.load(f)


        if not isinstance(joueur, dict):
            raise Erreur_structure_de_donnes("Vous n'avez pas rentrer un dictionnaire")
        
        for variable in variables:
            if variable not in joueur:
                raise Erreur_structure_de_donnes(f"La variable {variable} est manquante")