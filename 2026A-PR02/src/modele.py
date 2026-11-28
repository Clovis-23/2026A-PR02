"""Entraînement, sauvegarde et utilisation du modèle de points NBA."""

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib
import json
import pandas as pd 
import numpy as np
import os
from exceptions import Erreur_structure_de_donnes
from variables import VariableCategorielle, VariableIntervalles

def annoncer(fonction):
    """Annonce le début de l'entraînement."""
    def wrapper(self):
        print("Entraînement en cours...")
        return fonction(self)
    return wrapper


class ModeleNBA:
    """Regroupe le modèle de régression et les données utiles à son évaluation."""

    def __init__(self) -> None:
        """Crée une régression non entraînée et repère le dossier du projet."""
        self._modele= LinearRegression()
        dossier_script = os.path.dirname(__file__)
        self.racine_projet = os.path.dirname(dossier_script)


    def getdummies(self, data: pd.DataFrame, colonne: str) -> pd.DataFrame:
        """Transforme la colonne indiquée en colonnes de 0 et de 1.

        Conserve et renvoie le tableau obtenu. Lève KeyError si le nom de
        colonne n'existe pas dans les données reçues.
        """
        self.colonne_int= pd.get_dummies(data[colonne],dtype=int)
        
        return self.colonne_int
    

    def preparer_donnees(self) -> tuple[pd.DataFrame, pd.Series]:
        """Lit le CSV du projet et renvoie les entrées X et les points Y.

        Le poste est converti en colonnes numériques pour la régression.
        Lève FileNotFoundError si le CSV manque et KeyError si une colonne
        attendue est absente. Un CSV mal formé peut aussi empêcher la lecture.
        """
        
        chemin=os.path.join(self.racine_projet,"donnees","nba_joueur_saison_2005_2024.csv")

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
    
    @annoncer
    def entrainer(self) -> tuple[pd.DataFrame, pd.DataFrame]:
            """Entraîne le modèle et garde les ensembles de test et d'entraînement.

            Renvoie les tableaux d'entrées X_train et X_test. Peut échouer si
            le CSV est absent ou si les données ne conviennent pas au modèle.
            """
            X,Y= self.preparer_donnees()
            X_train, X_test, Y_train, Y_test = train_test_split(
            X, Y,
            test_size=0.2,
            random_state=42
            )
            self._modele.fit(X_train, Y_train)
            self.X_train=X_train
            self.X_test=X_test
            self.Y_train=Y_train
            self.Y_test=Y_test
            return X_train, X_test
    
    
    def evaluer(self) -> tuple[float, float, np.bool_]:
        """Renvoie la MAE du modèle, celle de la référence et le contrôle NumPy.

        La référence prédit la moyenne des points de l'ensemble d'entraînement.
        Le dernier résultat indique si les calculs NumPy et scikit-learn
        concordent. Il faut avoir appelé entrainer(), sinon les ensembles
        nécessaires à l'évaluation ne sont pas disponibles.
        """
        
        predictions = self._modele.predict(self.X_test)    
        mae = mean_absolute_error(self.Y_test, predictions)
        moy= self.Y_train.mean()
        predictions_baseline=[moy for joueur in self.Y_test]
        mae_baseline = mean_absolute_error(self.Y_test, predictions_baseline )
        mae_verif=np.abs(self.Y_test - predictions).mean()
        verification= np.isclose(mae,mae_verif)
        
        return mae,mae_baseline, verification
   
        
    def sauvegarder(self) -> None:
            """Écrit le modèle actuel dans modeles/modele_nba.joblib.

            Crée le dossier au besoin et remplace le fichier existant.
            Ne renvoie rien. Une erreur d'accès au disque empêche la sauvegarde.
            """
            chemin= os.path.join(self.racine_projet,"modeles" )
            os.makedirs(chemin, exist_ok=True)

            chemin_sauvegarde = os.path.join(chemin, "modele_nba.joblib")

            joblib.dump(self._modele, chemin_sauvegarde)

    def sauvegarder_metadata(self) -> None:
        """Écrit les colonnes, catégories, intervalles et la MAE dans le JSON.

        Ne renvoie rien. Le modèle doit avoir été entraîné avec entrainer().
        La lecture du CSV, l'évaluation ou l'écriture du fichier peuvent échouer
        si les données ou les fichiers nécessaires ne sont pas accessibles.
        """

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

    def charger(self) -> None:
        """Remplace le modèle actuel par celui du fichier modele_nba.joblib.

        Ne renvoie rien. Lève FileNotFoundError si le fichier manque.
        Le chargement peut aussi échouer si le fichier est illisible ou incompatible.
        """

        chemin=os.path.join(self.racine_projet,'modeles','modele_nba.joblib' )
        if not os.path.exists(chemin):
            raise FileNotFoundError("Le fichier modele_nba est introuvable")
        self._modele= joblib.load(chemin)

    def predire(self, joueur: dict[str, str | int | float]) -> float:
        """Valide les statistiques du joueur et renvoie ses points prédits par match.

        Reçoit un dictionnaire contenant le poste et les valeurs numériques,
        sans le modifier. Il faut avoir chargé ou entraîné le modèle.
        Lève Erreur_structure_de_donnes si la structure ou un type est invalide,
        CategorieInvalide pour un poste inconnu et Valeur_hors_norme pour une
        valeur hors intervalle. Lève ValueError pour une valeur NaN ou une
        prédiction négative. Le fichier de métadonnées doit être lisible.
        """
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
        joueur = joueur.copy()
        for i in joueur:
            if i not in variables:
                raise Erreur_structure_de_donnes(f"La variable {i} est inconnue")

            if i == "pos":
                variable = VariableCategorielle(i, dictionnaire["categories"])
                variable.valider(joueur[i])

            else:
                variable = VariableIntervalles(
                    i,
                    dictionnaire["intervalles"][i]["min"],
                    dictionnaire["intervalles"][i]["max"]
                )

                try:
                    valeur = float(joueur[i])
                except (ValueError, TypeError):
                    raise Erreur_structure_de_donnes(
                        f"La variable {i} doit être numérique"
                    )

                if pd.isna(valeur):
                    raise ValueError(f"La variable {i} est manquante")
                variable.valider(valeur)
                joueur[i] = valeur
        

        joueur= pd.DataFrame([joueur])
        joueur_int=self.getdummies(joueur,'pos')
        joueur=joueur.drop(columns=['pos']) 
        joueur=pd.concat([joueur,joueur_int], axis=1)

        colonne= dictionnaire['colonnes']
        joueur=joueur.reindex(columns=colonne, fill_value=0)
        prediction=self._modele.predict(joueur)
        points =float(prediction[0])

        if points<0:
            raise ValueError(
        "Le modèle a calculé des points négatifs. "
        "Vérifiez les données fournies."
    )
        return points
    
if __name__ == "__main__":
    nba = ModeleNBA()

    nba.entrainer()

    mae, mae_baseline, verification = nba.evaluer()
    print("MAE :", mae)
    print("MAE baseline :", mae_baseline)
    print("Vérification NumPy :", verification)

    nba.sauvegarder()
    nba.sauvegarder_metadata()

    print("Modèle entraîné et sauvegardé avec succès !")



# Ancien modèle : forêt aléatoire, non utilisé, gardé pour référence

# class Modele :
#     def __init__ (self) :
#         dossier_script = os.path.dirname(__file__)
#         racine_projet = os.path.dirname(dossier_script)
#         self.chemin_modele = os.path.join(racine_projet, "modeles", "modele.pkl")
#         self.modele_foret = None
    
#     def __str__(self) -> str:
#             if self.modele_foret is None:
#                 return "Modele pas encore chargé"
#             return "Modele chargé"

#     def charger_csv (self) :
#          self.modele_foret = joblib.load(self.chemin_modele)

#     def predire_points(self, pos, age, minutes_per_game, deux_pa, trois_pa, trb, ast, stl, tov):
#         profil_invente = pd.DataFrame([{
#             "pos": pos,
#             "age": age,
#             "minutes_per_game": minutes_per_game,
#             "2pa": deux_pa,
#             "3pa": trois_pa,
#             "trb": trb,
#             "ast": ast,
#             "stl": stl,
#             "tov": tov
#         }])

#         profil_encode = pd.get_dummies(profil_invente, columns=["pos"], dtype=float)
#         colonnes_attendues = ["age", "minutes_per_game", "2pa", "3pa", "trb", "ast", "stl", "tov",
#                             "pos_C", "pos_PF", "pos_PG", "pos_SF", "pos_SG"]
#         profil_encode = profil_encode.reindex(columns=colonnes_attendues, fill_value=0)

#         prediction_points = self.modele_foret.predict(profil_encode)
#         return float(prediction_points[0])

#     def entrainer (self, entrees_entrainement_encodees, cible_entrainement):
#         self.modele_foret = RandomForestRegressor(random_state=42)
#         self.modele_foret.fit(entrees_entrainement_encodees, cible_entrainement)

#     def evaluer (self, entrees_test_encodees, cible_test) :
#         predictions_foret = self.modele_foret.predict(entrees_test_encodees)
#         self.erreur_modele = mean_squared_error(cible_test, predictions_foret) ** 0.5
#         self.score_r2_modele = r2_score(cible_test, predictions_foret)
#         return self.erreur_modele, self.score_r2_modele

#     def sauvegarder (self) :
#         dossier_modeles = os.path.dirname(self.chemin_modele)
#         os.makedirs(dossier_modeles, exist_ok=True)
#         joblib.dump(self.modele_foret, self.chemin_modele)
 

# if __name__ == "__main__":
#     jeu = JeuDeDonnees()
#     donnees = jeu.charger_csv("nba_joueur_saison_2005_2024.csv")

#     entrees = donnees[["pos", "age", "minutes_per_game", "2pa", "3pa", "trb", "ast", "stl", "tov"]]
#     cible_points = donnees["pts"]

#     entrees_entrainement, entrees_test, cible_entrainement, cible_test = train_test_split(
#         entrees, cible_points, test_size=0.2, random_state=42)

#     moyenne_points_entrainement = cible_entrainement.mean()
#     predictions_moyenne = [moyenne_points_entrainement] * len(cible_test)
#     erreur = mean_squared_error(cible_test, predictions_moyenne) ** 0.5

#     #Transformer pos en nombres
#     entrees_entrainement_encodees = pd.get_dummies(entrees_entrainement, columns=["pos"], dtype=float)
#     entrees_test_encodees = pd.get_dummies(entrees_test, columns=["pos"], dtype=float)
#     entrees_test_encodees = entrees_test_encodees.reindex(
#         columns=entrees_entrainement_encodees.columns, fill_value=0)


#     modele = Modele()
#     modele.entrainer(entrees_entrainement_encodees, cible_entrainement)
#     erreur_modele, score_r2_modele = modele.evaluer(entrees_test_encodees, cible_test)

#     print("Moyenne train :", moyenne_points_entrainement)
#     print("RMSE baseline :", erreur)
#     print("RMSE modele :", erreur_modele)
#     print("R2 modele :", score_r2_modele)

#     modele.sauvegarder()