# Projet 2 — INF1007 Automne 2026

## Estimation des points NBA 🏀

Notre application estime les **points par match** d'un joueur NBA à partir de son profil statistique : poste, âge, minutes jouées, tirs tentés et autres statistiques.

Elle utilise une **régression linéaire** et une **interface Streamlit** qui fonctionne en local. L'utilisateur saisit un profil, obtient une estimation et peut consulter l'historique de ses prédictions.

**Pour lancer l'application, vous devez exécuter&#32;`python src/main.py`.**

Les données décrivent des joueurs sur une saison. L'application estime donc les points moyens correspondant à un profil ; elle ne prédit pas le score exact du prochain match.

## Installations requises

Ce projet nécessite Python 3.10 ou plus récent. Les tests et les résultats ci-dessous ont été vérifiés avec Python 3.13.3.

Ensuite, installez les dépendances :

```bash
python -m pip install -r requirements.txt
```

Le fichier `requirements.txt` inclut les dépendances de l'application, pytest et coverage.

## Lancement

**Toutes les commandes ci-dessous se lancent dans le dossier contenant&#32;`src`,&#32;`tests`&#32;et&#32;`requirements.txt`.** Depuis la racine Git du dépôt :

```bash
cd 2026A-PR02
```

Lancez l'interface :

```bash
python src/main.py
```

Ouvrez l'adresse locale indiquée dans le terminal, en général `http://localhost:8501`. Pour arrêter le serveur, utilisez `Ctrl+C`.

Il n'est pas nécessaire de réentraîner le modèle pour utiliser l'application : le modèle sauvegardé et ses métadonnées sont déjà présents.

## Utilisation

1. Entrez un nom ou un pseudonyme pour reconnaître le profil dans l'historique.
2. Choisissez le poste et les valeurs numériques. Les bornes des champs viennent des métadonnées enregistrées avec le modèle.
3. Cliquez sur **Prédire**. Le résultat est exprimé en points par match.
4. Le graphique situe cette estimation dans la distribution des points du jeu de données.
5. Activez **Afficher l'historique** pour consulter les prédictions enregistrées. La suppression d'une ligne utilise un numéro qui commence à zéro.

Les profils et résultats sont conservés localement dans `historique_predictions.csv`. Le nom saisi sert uniquement à identifier le profil dans ce fichier : ce n'est pas une caractéristique utilisée par le modèle.

## Informations sur le projet

### Structure du projet

Le projet est organisé de la manière suivante :

```plaintext
2026A-PR02/                  # racine Git
├── .github/workflows/tests.yml  # tests automatiques à chaque push
└── 2026A-PR02/              # dossier de travail des commandes ci-dessus
    ├── README.md
    ├── DECISIONS.md
    ├── JOURNAL_IA.md
    ├── requirements.txt
    ├── pytest.ini
    ├── donnees/             # CSV préparé et métadonnées JSON
    ├── modeles/             # modèle sauvegardé avec joblib
    ├── src/
    │   ├── donnees.py
    │   ├── modele.py
    │   ├── variables.py
    │   ├── exceptions.py
    │   ├── interface.py
    │   └── main.py
    ├── tests/
    │   ├── test_donnees.py
    │   └── test_modele.py
    ├── histogramme_pts.png
    └── historique_predictions.csv
```

### Détails sur les fichiers

| Fichier | Rôle |
| --- | --- |
| `src/donnees.py` | Préparation du CSV à partir du fichier Excel brut, et exploration des données. |
| `src/modele.py` | Entraînement, évaluation et prédiction avec la régression linéaire. |
| `src/variables.py` | Validation des nombres et des catégories saisies. |
| `src/exceptions.py` | Erreurs propres au projet. |
| `src/interface.py` | Interface Streamlit, prédiction et historique. |
| `src/main.py` | Lanceur de l'interface Streamlit. |
| `donnees/metadata.json` | Colonnes, catégories, intervalles et MAE du modèle. |
| `modeles/modele_nba.joblib` | Modèle sauvegardé, chargé par l'interface sans réentraînement. |

Les principales relations entre les classes : `Variable` est la classe parente, redéfinie par `VariableIntervalles` et `VariableCategorielle` pour leurs validations respectives. `Application` contient une instance de `ModeleNBA`.

**Outil du chapitre 7 :** le décorateur `@annoncer` affiche un message avant l'exécution de la méthode d'entraînement.

## Jeu de données et préparation

Le fichier utilisé par le modèle est `donnees/nba_joueur_saison_2005_2024.csv`. Il contient **8 289 observations et 12 colonnes**, dont 11 caractéristiques et la cible `pts`. Il occupe environ 0,39 Mo, donc moins de 25 Mo.

| Colonne | Type | Description |
| --- | --- | --- |
| `pts` | cible | Points moyens par match. |
| `pos` | catégorielle | Poste : `C`, `PF`, `PG`, `SF`, `SG`. |
| `season_year`, `age`, `games` | numérique | Année de la saison, âge, nombre de matchs. |
| `minutes_per_game`, `2pa`, `3pa` | numérique | Minutes par match, tirs à 2 et à 3 points tentés par match. |
| `trb`, `ast`, `stl`, `tov` | numérique | Rebonds, passes décisives, interceptions et balles perdues par match. |

`JeuDeDonnees.preparer()` garde les lignes NBA à partir de 2005 avec au moins 20 matchs, sélectionne les colonnes utiles et renomme `Minutes Played` en `minutes_per_game`. Le seuil de matchs limite les moyennes établies sur très peu de rencontres. Le CSV actuel ne contient aucune valeur manquante. Un histogramme des points est enregistré dans `histogramme_pts.png`.

**Source :** [1946 - Present - NBA Player Stats (regular season)](https://www.kaggle.com/datasets/teteuvinicius/1946-present-nba-player-stats-regular-season), publié sur Kaggle par le compte `teteuvinicius`.

## Modèle, évaluation et limites

Nous utilisons `LinearRegression` de scikit-learn : la cible est une valeur numérique, et ce modèle fournit une solution simple à expliquer et rapide à entraîner. Le poste est transformé en colonnes de 0 et de 1 avec `get_dummies`, sans imposer un ordre entre les catégories.

La séparation utilise **80 % des observations pour l'entraînement** et **20 % pour le test**, avec `random_state=42` : 6 631 lignes d'entraînement et 1 658 de test. La métrique est la **MAE**, l'erreur absolue moyenne, exprimée en points par match. La référence prédit toujours la moyenne des points de l'ensemble d'entraînement.

| Modèle | MAE |
| --- | --- |
| Régression linéaire | **0,7481 point par match** |
| Référence (moyenne de l'entraînement) | **4,8483 points par match** |

Résultats recalculés le 19 novembre 2026. Le calcul vectorisé NumPy donne le même résultat que scikit-learn, à la tolérance numérique près. Cela ne signifie pas que chaque prédiction a une erreur inférieure à 0,75 point.

Quelques limites importantes :

- Les entrées décrivent la même saison que les points. Le bon score ne démontre pas une capacité à prévoir une saison future.
- La séparation aléatoire peut placer différentes saisons d'un même joueur dans les deux ensembles.
- Les joueurs avec moins de 20 matchs sont exclus. Les résultats ne représentent donc pas tous les profils possibles.
- Une régression linéaire peut produire une estimation négative pour certains profils ; le code refuse alors ce résultat.
- Aucun intervalle de confiance n'est calculé et aucune comparaison expérimentale avec un second modèle n'a été réalisée dans ce projet.

Pour réentraîner le modèle et remplacer sa sauvegarde et ses métadonnées :

```bash
python src/modele.py
```

Pour reconstruire le CSV depuis le fichier Excel et produire le graphique d'exploration :

```bash
python src/donnees.py
```

## Tests et couverture

Depuis le même dossier de travail :

```bash
python -m pytest tests/ -v
```

Les **8 tests passent** lors de la vérification locale. Les cinq tests de `test_donnees.py` vérifient les variables : poste valide ou invalide, âge usuel, bornes et âge hors intervalle. Les trois tests de `test_modele.py` vérifient une structure incorrecte, une variable manquante et la concordance du calcul de MAE. Ils utilisent `pytest.raises` pour les erreurs et `pytest.approx` pour les flottants.

## Intégration continue

Le workflow `.github/workflows/tests.yml`, placé à la racine Git, installe Python 3.13 et les dépendances, puis lance `python -m pytest tests/ -v` dans le sous-dossier `2026A-PR02` à chaque push. Les exécutions des commits `07dadf0` et `6be731b` ont réussi sur GitHub. Chaque nouveau push produit un nouveau résultat à consulter dans l'onglet Actions.

## Documentation officielle

Pages consultées lors de la rédaction de cette documentation :

- [pandas — 10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
- [scikit-learn — LinearRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)
- [Streamlit — st.pyplot](https://docs.streamlit.io/develop/api-reference/charts/st.pyplot)
- [Coverage.py — exécuter une mesure](https://coverage.readthedocs.io/en/latest/commands/cmd_run.html)

La fiche de [décisions](DECISIONS.md) explique les choix techniques. Le [journal d'IA](JOURNAL_IA.md) décrit l'aide reçue, les vérifications et les changements de décision.