import pandas as pd
import os
import matplotlib.pyplot as plt


class JeuDeDonnees :
    def __init__ (self) :
        self.df = None 

    def preparer(self) -> pd.DataFrame:
        """Crée le jeu final 2005-2024 à partir du fichier Excel brut."""
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
        """Charge un CSV du dossier donnees, en vérifiant qu'il existe."""
        dossier_script = os.path.dirname(__file__)
        racine_projet = os.path.dirname(dossier_script)
        chemin = os.path.join(racine_projet, "donnees", "nba_joueur_saison_2005_2024.csv")

        if not os.path.exists(chemin):
            raise FileNotFoundError(f"Fichier introuvable : {chemin}")
        self.df = pd.read_csv(chemin) 
        return self.df

    def afficher_infos(self) -> None:
        """Affiche les infos d'exploration du jeu chargé."""
        print(self.df.shape)
        print(self.df.columns)
        print(self.df.dtypes)
        print(self.df.head())
        print(self.df.isna().sum())
        print(self.df["pos"].unique())

    def __str__(self) -> str:
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