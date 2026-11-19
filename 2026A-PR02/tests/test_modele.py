
"""Teste la structure d'un profil joueur et le calcul de la MAE avec NumPy."""

import pytest
import numpy as np
from sklearn.metrics import mean_absolute_error

from src.modele import ModeleNBA
from src.exceptions import Erreur_structure_de_donnes


# TEST 6 : Mauvaise structure de données
def test_dictionnaire_invalide() -> None:
    """Vérifie qu'une liste est refusée à la place d'un dictionnaire joueur."""
    modele = ModeleNBA()

    with pytest.raises(Erreur_structure_de_donnes):
        modele.predire(["PG", 25, 82])


# TEST 7 : Variable manquante
def test_variable_manquante() -> None:
    """Vérifie qu'un profil sans âge déclenche l'erreur de structure attendue."""
    modele = ModeleNBA()

    joueur = {
        "season_year": 2020,
        "pos": "PG",
        "games": 82,
        "minutes_per_game": 30,
        "2pa": 8,
        "3pa": 5,
        "trb": 4,
        "ast": 7,
        "stl": 1,
        "tov": 2
    }

    # Il manque volontairement "age"
    with pytest.raises(Erreur_structure_de_donnes):
        modele.predire(joueur)


# TEST 8 : Vérification MAE avec NumPy
def test_mae_numpy() -> None:
    """Compare la MAE NumPy à celle de scikit-learn, avec une tolérance numérique."""
    valeurs_reelles = np.array([10, 20, 30])
    predictions = np.array([12, 18, 27])

    mae_sklearn = mean_absolute_error(
        valeurs_reelles, predictions
    )

    mae_numpy = np.abs(valeurs_reelles - predictions).mean()

    assert mae_numpy == pytest.approx(mae_sklearn)

# .venv/bin/python -m pytest tests/test_modele.py -v
