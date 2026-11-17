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
        