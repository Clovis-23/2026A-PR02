"""Affiche le formulaire NBA, les prédictions et leur historique avec Streamlit."""

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
    """Relie le modèle sauvegardé aux profils saisis et à l'historique CSV."""

    def __init__ (self) -> None:
        """Charge le modèle et ses métadonnées pour préparer l'application.

        Échoue si un fichier nécessaire est absent, illisible ou invalide.
        """
        # Ici, on charge le modèle déjà entraîné.
        from modele import ModeleNBA

        self.modele = ModeleNBA()
        self.modele.charger()
        self.chemin_historique = os.path.join(racine_projet, "historique_predictions.csv")

        chemin_metadata = os.path.join(racine_projet, "donnees", "metadata.json")
        with open(chemin_metadata, "r", encoding="utf-8") as fichier:
            self.metadata = json.load(fichier)

    def __str__ (self) -> str:
        """Renvoie un court message sur la présence du modèle dans l'application."""
        if self.modele is None:
            return "Modele pas encore chargé"
        return "Modele chargé"

    def predire_profil (self, joueur: dict) -> float:
        """Renvoie les points par match estimés à partir du dictionnaire du joueur.

        Laisse remonter les erreurs du modèle si le profil est invalide ou si
        les fichiers nécessaires à la prédiction ne peuvent pas être lus.
        """
        prediction = self.modele.predire(joueur)
        return float(prediction)
    
    def consulter_historique(self) -> pd.DataFrame | None:
        """Renvoie les prédictions enregistrées, ou None si le fichier est absent.

        Échoue si le fichier existe mais ne peut pas être lu comme un CSV.
        """
        if not os.path.exists(self.chemin_historique):
            return None
        return pd.read_csv(self.chemin_historique)

    def enregistrer_prediction(self, nom_joueur: str, joueur: dict, prediction: float) -> None:
            """Ajoute le nom, le profil et les points prédits au fichier d'historique.

            Ne renvoie rien. Échoue si le fichier ne peut pas être écrit.
            """
            nouvelle_ligne = joueur.copy()
            nouvelle_ligne["nom_joueur"] = nom_joueur
            nouvelle_ligne["points_predits"] = prediction
            pd.DataFrame([nouvelle_ligne]).to_csv(self.chemin_historique, mode="a",
                    header=not os.path.exists(self.chemin_historique), index=False)

    def retirer_ligne_histo(self, numero_ligne: int) -> bool:
        """Supprime la ligne demandée, en comptant à partir de zéro.

        Renvoie True si la suppression a réussi, False si le fichier est absent
        ou le numéro invalide. Échoue si la lecture ou l'écriture du CSV échoue.
        """
        historique = self.consulter_historique()
        if historique is None:
            return False
        if numero_ligne < 0 or numero_ligne >= len(historique):
            return False

        historique = historique.drop(index=numero_ligne).reset_index(drop=True)
        historique.to_csv(self.chemin_historique, index=False)
        return True

#on passe a l'interface pur avec streamlit

def effacer_resultat() -> None:
    """Retire la dernière prédiction de la session si elle existe, sans rien renvoyer."""
    if "derniere_prediction" in st.session_state:
        del st.session_state["derniere_prediction"]

def saisir_un_nombre (application: Application, colonne: str, texte: str) -> int | float:
    """Affiche un champ numérique et renvoie sa valeur entière ou décimale.

    Utilise les bornes de la colonne dans les métadonnées de l'application et
    le texte reçu comme libellé. Échoue si ces bornes sont absentes ou invalides.
    """
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

def valider_joueur(joueur: dict, metadata: dict) -> dict:
    """Vérifie les valeurs numériques du joueur et renvoie une copie du profil.

    Les champs doivent être présents et numériques. Lève ValueError si une
    valeur sort de l'intervalle indiqué dans les métadonnées.
    """
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
    """Renvoie l'histogramme des points avec un repère pour la prédiction du joueur.

    Le nom sert à la légende et la prédiction place le repère sur l'axe des
    points. Échoue si le CSV est absent, illisible ou sans colonne « pts ».
    """
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

def main() -> None:
    """Affiche l'interface et traite les actions de l'utilisateur, sans rien renvoyer.

    À lancer avec Streamlit. Affiche les erreurs de chargement et les ValueError
    de prédiction ; les autres erreurs de fichier ou de validation peuvent remonter.
    """
    st.set_page_config(page_title="Prédiction de points NBA", page_icon="🏀", layout="centered")
    st.title("Prédiction des points NBA")
    st.write("Entrez les valeurs d'un joueur type pour calculer ses points par match.")

    if st.button("Générer un joueur aléatoire") :
          
        pass

    try:
        application = Application()
    except Exception as e:
        st.error(f"Impossible de charger le modèle : {e}")
        st.stop()

    nom_joueur = st.text_input("Nom du joueur").strip()
    pos = st.radio("Poste", application.metadata["categories"])
    joueur = {"pos": pos}
    for colonne, texte in CHAMPS_NUMERIQUES.items():
        if colonne == "age" :
            intervalle = application.metadata["intervalles"]["age"]
            joueur[colonne] = st.slider(texte, int(intervalle["min"]), int(intervalle["max"]))
        else :
            joueur[colonne] = saisir_un_nombre(application, colonne, texte)

    if st.button("Prédire"):
        if nom_joueur == "":
            st.warning("Entrez le nom du joueur avant de prédire.")
        else:
            try:
                joueur_valide = valider_joueur(joueur, application.metadata)
                prediction = application.predire_profil(joueur_valide)
                st.success(f"{nom_joueur} devrait marquer {prediction:.2f} points par match.")
                application.enregistrer_prediction(nom_joueur, joueur_valide, prediction)
                fig = graphique(nom_joueur, prediction)
                st.pyplot(fig)
                plt.close(fig)
            except ValueError as e:
                st.error(str(e))

    historique = application.consulter_historique()
    num_ligne = st.number_input("Saisir le numéro de la ligne a retirer, 0 = première ligne", min_value=0, step=1, value=0)
    if st.button("Retirer une ligne de l'historique") :
        if historique is None :
            st.warning("Impossible de retirer une ligne car l'historique est vierge")
        else :
            if application.retirer_ligne_histo(int(num_ligne)) :
                st.success("Ligne retirée")
            else :
                st.warning("Numéro invalide !")

    historique = application.consulter_historique()
    if st.toggle("Afficher l'historique"):
        if historique is None:
            st.info("Aucune prédiction pour l'instant. Veuillez d'abord faire une prédiction")
        else:
            st.dataframe(historique)
    
    
if __name__ == "__main__":
    main()

# commande a mettre dans le terminal :
# streamlit run src/interface.py
# streamlit run 2026A-PR02/src/interface.py
