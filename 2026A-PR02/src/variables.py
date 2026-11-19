"""Définit les variables d'un joueur et les règles de validation de leurs valeurs."""

from src.exceptions import Valeur_hors_norme, CategorieInvalide

class Variable():
    """Représente une caractéristique du joueur, identifiée par son nom."""

    def __init__ (self, nom: str) -> None:
        """Crée une variable à partir du nom de sa colonne dans les données."""
        self.nom=nom


class VariableIntervalles(Variable):
    """Représente une valeur numérique comprise entre deux bornes incluses."""

    def __init__(self, nom: str, minimum: float, maximum: float) -> None:
        """Mémorise le nom et les bornes autorisées, sans vérifier leur ordre."""
        super().__init__(nom)
        self.minimum= minimum
        self.maximum=maximum


    def valider(self, valeur: float) -> bool:
        """Renvoie True si le nombre est dans l'intervalle, bornes comprises.

        Lève Valeur_hors_norme si la valeur est trop petite ou trop grande.
        La valeur doit déjà être numérique pour pouvoir comparer les bornes.
        """
        if valeur <self.minimum or valeur>self.maximum:
            raise Valeur_hors_norme("Valeur hors norme")
        return True
        
class VariableCategorielle(Variable):
    """Représente une valeur à choisir dans une liste de catégories."""

    def __init__(self, nom: str, categories: list[str]) -> None:
        """Mémorise le nom de la variable et la liste des catégories permises."""
        super().__init__(nom)
        self.categories=categories
    
    def valider(self, valeur: str) -> bool:
        """Renvoie True si le texte fait partie des catégories autorisées.

        Lève CategorieInvalide si la valeur n'est pas dans la liste.
        """
        if valeur not in  self.categories:
            raise CategorieInvalide(f"Cette valeur '{valeur}' n'appartient  pas à la categorie")
        return True

# vnum= VariableIntervalles("season_year", dictionnaire["intervalles"]["season_year"]["min"],dictionnaire["intervalles"]["season_year"]["max"])
# vnum.valider(joueur["season_year"])


        
