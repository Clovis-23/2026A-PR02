"""Regroupe les erreurs prévues lors de la validation des données du joueur."""

class Erreur_structure_de_donnes(Exception):
        """Signale un profil mal structuré ou une valeur qui n'est pas numérique."""
        pass

class Valeur_hors_norme(Exception):
       """Signale une valeur numérique en dehors de l'intervalle autorisé."""
       pass 
class CategorieInvalide(Exception):
        """Signale une catégorie qui ne figure pas parmi les choix autorisés."""
        pass
