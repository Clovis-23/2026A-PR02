import pytest
from src.variables import VariableIntervalles, VariableCategorielle
from src.exceptions import Valeur_hors_norme, CategorieInvalide

# TEST 1 : Position valide
def test_position_valide():
    position = VariableCategorielle("pos", ["PG", "SG", "C"])
    assert position.valider("PG") == True


# TEST 2 : Position invalide
def test_position_invalide():
    position = VariableCategorielle("pos", ["PG", "SG", "C"])

    with pytest.raises(CategorieInvalide):
        position.valider("XYZ")


# TEST 3 : Age valide
def test_age_valide():
    age = VariableIntervalles("age", 18, 40)
    assert age.valider(25) == True


# TEST 4 : Age aux limites
def test_age_limite():
    age = VariableIntervalles("age", 18, 40)

    assert age.valider(18) == True
    assert age.valider(40) == True


# TEST 5 : Age hors intervalle
def test_age_invalide():
    age = VariableIntervalles("age", 18, 40)

    with pytest.raises(Valeur_hors_norme):
        age.valider(50)


# tester .venv/bin/python -m pytest tests/test_donnees.py -v