"""Teste les valeurs usuelles, les limites et les erreurs des variables."""

import pytest
from variables import VariableIntervalles, VariableCategorielle
from exceptions import Valeur_hors_norme, CategorieInvalide

# TEST 1 : Position valide
def test_position_valide() -> None:
    """Vérifie qu'un poste présent dans la liste est accepté."""
    position = VariableCategorielle("pos", ["PG", "SG", "C"])
    assert position.valider("PG") == True


# TEST 2 : Position invalide
def test_position_invalide() -> None:
    """Vérifie qu'un poste inconnu déclenche CategorieInvalide."""
    position = VariableCategorielle("pos", ["PG", "SG", "C"])

    with pytest.raises(CategorieInvalide):
        position.valider("XYZ")


# TEST 3 : Age valide
def test_age_valide() -> None:
    """Vérifie qu'un âge à l'intérieur de l'intervalle est accepté."""
    age = VariableIntervalles("age", 18, 40)
    assert age.valider(25) == True


# TEST 4 : Age aux limites
def test_age_limite() -> None:
    """Vérifie que les deux bornes de l'intervalle sont acceptées."""
    age = VariableIntervalles("age", 18, 40)

    assert age.valider(18) == True
    assert age.valider(40) == True


# TEST 5 : Age hors intervalle
def test_age_invalide() -> None:
    """Vérifie qu'un âge trop élevé déclenche Valeur_hors_norme."""
    age = VariableIntervalles("age", 18, 40)

    with pytest.raises(Valeur_hors_norme):
        age.valider(50)


# python -m pytest tests/test_donnees.py -v
