"""Prépare les données NBA et permet d'explorer le fichier CSV obtenu."""

import pandas as pd
import os
import matplotlib.pyplot as plt


class JeuDeDonnees :
    """Conserve les données chargées pour les préparer et les examiner."""

    def __init__ (self) -> None:
        """Crée un jeu de données vide ; aucun fichier n'est encore chargé."""
        self.df = None 

    def preparer(self) -> pd.DataFrame:
        """Prépare le CSV à partir du fichier Excel brut et renvoie le tableau.

        Garde les saisons NBA à partir de 2005 avec au moins 20 matchs,
        sélectionne les colonnes utiles et enregistre le résultat dans donnees.
        Échoue si le fichier Excel est absent, si une colonne manque ou si
        le CSV ne peut pas être écrit.
        """
        dossier_script = os.path.dirname(__file__)
        racine_projet = os.path.dirname(dossier_script)
        chemin_brut = os.path.join(racine_projet, "donnees", "brut", "1946 - Present - NBA Player Stats.xlsx")
        chemin_final = os.path.join(racine_projet, "donnees", "nba_joueur_saison_2005_2024.csv")

        df = pd.read_excel(chemin_brut)
        df = df[(df["league"] == "NBA") & (df["season_year"] >= 2005) & (df["games"] >= 20)]
        df = df.rename(columns={"Minutes Played": "minutes_per_game"})
        df = df[["season_year", "pos", "age", "games", "minutes_per_game", "2pa", "3pa", "trb", "ast", "stl", "tov", "pts"]]
        df.to_csv(chemin_final, index=False)
        self.df = df
        return df

    def charger_csv(self, nom_fichier: str) -> pd.DataFrame:
        """Charge le CSV NBA du projet, le garde dans self.df et le renvoie.

        Le paramètre nom_fichier n'est pas encore utilisé : le chemin est fixe.
        Lève FileNotFoundError si le fichier est absent. La lecture peut aussi
        échouer si son contenu n'est pas un CSV valide.
        """
        dossier_script = os.path.dirname(__file__)
        racine_projet = os.path.dirname(dossier_script)
        chemin = os.path.join(racine_projet, "donnees", "nba_joueur_saison_2005_2024.csv")

        if not os.path.exists(chemin):
            raise FileNotFoundError(f"Fichier introuvable : {chemin}")
        self.df = pd.read_csv(chemin) 
        return self.df

    def afficher_infos(self) -> None:
        """Affiche les dimensions, types, valeurs manquantes et postes du jeu.

        Ne renvoie rien. Appeler preparer ou charger_csv avant cette méthode,
        sinon self.df ne contient pas de tableau et l'affichage échoue.
        """
        print(self.df.shape)
        print(self.df.columns)
        print(self.df.dtypes)
        print(self.df.head())
        print(self.df.isna().sum())
        print(self.df["pos"].unique())

    def __str__(self) -> str:
        """Renvoie un court message indiquant si les données sont chargées."""
        if self.df is None:
            return "Dataset pas encore chargé"
        return "Dataset chargé"

if __name__ == "__main__":
    jeu = JeuDeDonnees()
    jeu.preparer()
    jeu.charger_csv("nba_joueur_saison_2005_2024.csv")
    print(jeu)
    jeu.afficher_infos()


    plt.hist(jeu.df["pts"], bins=100)
    plt.title("Distribution des points par match")
    plt.xlabel("Points par match")  #selon l'axe x
    plt.ylabel("Nombre de joueurs-saisons") #selon l'axe y
    dossier_script = os.path.dirname(__file__)
    racine_projet = os.path.dirname(dossier_script)
    chemin_graphique = os.path.join(racine_projet, "histogramme_pts.png")
    plt.savefig(chemin_graphique)  # on le save sous ce nom
    plt.show()  # on l'affiche 


# import pandas as pd 
# import matplotlib.pyplot as plt
# import os 


# class JeuDeDonnees():
#     def __init__(self):
#         self.df=None
#         dossier = os.path.dirname(__file__)
#         self.racine = os.path.dirname(dossier)
        
    
    
#     def preparer(self):

#         chemin=os.path.join(self.racine,"donnees","brut","1946 - Present - NBA Player Stats.xlsx")

#         if not os.path.exists(chemin):
#             raise FileNotFoundError("Fichier donnees brut introvable")


#         donnes = pd.read_excel(chemin)

#         estnba=donnes['league'] == 'NBA'

#         sup_2005=donnes['season_year']>=int(2005)

#         au_moins_20_matchs= donnes['games']>=20

#         jouees= donnes[estnba & sup_2005 & au_moins_20_matchs]
#         donnees_finales=jouees[['season_year', 'pos', 'age', 'games', 'Minutes Played', '2pa', '3pa', 'trb', 'ast', 'stl', 'tov', 'pts']]

#         self.df = donnees_finales.rename(columns={'Minutes Played': 'minutes_per_game'})

#         chemin_final = os.path.join(self.racine, "donnees", "nba_nettoye.csv")

#         with open(chemin_final, "w", encoding="utf-8", newline="") as fichier:
#             self.df.to_csv(fichier, index=False)
            
#         return self.df



# # print(donnees_finales.isna().sum()) 0 

# if __name__ == "__main__":
#     jeu = JeuDeDonnees()
#     jeu.preparer()
#     print(f"Données chargées : {len(jeu.df)} lignes.")
#     plt.hist(jeu.df['pts'],)
#     plt.xlabel('Points par match')
#     plt.ylabel('Nombre de lignes joueur-saison')
#     plt.title('histogramme de la colonne pts')
#     plt.savefig('histogramme_pts.png')
#     plt.show()
