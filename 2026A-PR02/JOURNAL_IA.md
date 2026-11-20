# Journal d'utilisation de l'IA

Les vérifications attribuées à Codex ont été réalisées par l'outil. La relecture par l'équipe reste nécessaire.

| Outil | Notre demande | Aide reçue | Vérification faite | Décision |
| --- | --- | --- | --- | --- |
| IA à préciser | Préparer le squelette du projet. | Aide à la structure de départ. | Utilisation déclarée par l'équipe ; échange initial à retrouver. | Préciser les éléments conservés après relecture. |
| ChatGPT / Codex | Lancer l'interface Streamlit. | Commande à exécuter depuis le dossier du projet. | Codex a vérifié le chemin après l'erreur « fichier introuvable ». | Garder la commande avec le bon dossier. |
| ChatGPT / Codex | Lancer les tests manuellement. | Utiliser le Python de l'environnement Conda. | Le terminal indiquait que `.venv/bin/python` n'existait pas. | **Changer la commande** pour utiliser `python -m pytest tests/ -v`. |
| ChatGPT / Codex | Corriger les imports. | Imports explicites depuis `src`, sans `if __package__`. | Les 8 tests passent lors de l'exécution par Codex. | Garder les imports simples dans le modèle et les variables. |
| ChatGPT / Codex | Créer un workflow GitHub Actions. | Fichier YAML lançant pytest à chaque push. | Tests locaux réussis, mais aucune exécution GitHub confirmée. | Annuler cette première version ; CI à terminer. |
| ChatGPT / Codex | Ajouter les docstrings et les types. | Documentation de 38 fonctions et méthodes. | Codex a comparé la logique avant/après : inchangée ; 8 tests réussis. | Garder les ajouts, à relire par l'équipe. |
| ChatGPT / Codex | Vérifier les exigences du mandat. | Liste des éléments manquants. | Codex a comparé le PDF aux fichiers du projet. | Utiliser la liste pour préparer la remise. |
| ChatGPT / Codex | Rédiger le README et les décisions. | Textes explicatifs et schémas du projet. | Codex a consulté la documentation et recalculé les MAE : 0,7481 et 4,8483. | Garder une base à relire ; compléter source, licence et validations. |
| ChatGPT / Codex | Résoudre l’erreur `No module named 'src'` lors du lancement direct de `modele.py`, avec des imports que nous comprenons. | Remplacement des imports `src.…` par les noms simples des modules dans le code et les tests ; ajout de `pytest.ini` avec `pythonpath = src` pour que pytest trouve les modules. | Codex a exécuté les 8 tests avec succès et vérifié l’entraînement et l’évaluation depuis le dossier `src`, sans remplacer le modèle sauvegardé. | Garder cette correction, qui remplace le choix précédent d’imports avec `src.` et permet le lancement direct du modèle. |
| ChatGPT / Codex | Mettre en place GitHub Actions pour lancer les tests à chaque push. | L’IA a rédigé le workflow approuvé et déplacé le fichier tests.yml à la racine Git, dans .github/workflows. Le workflow installe Python 3.13 et les dépendances, puis lance pytest dans le sous-dossier 2026A-PR02. | Documentation officielle GitHub consultée ; les 8 tests passent localement avec Python 3.13.3. L’exécution sur GitHub reste à vérifier après le push. | Garder cette version, qui remplace la première tentative annulée ; vérifier la CI verte sur GitHub après publication. |

## Une vérification qui a changé notre décision

Nous utilisions une commande avec `.venv/bin/python`. L'erreur du terminal a montré
que ce chemin n'existait pas. Nous avons donc choisi d'utiliser le Python de notre
environnement Conda : `python -m pytest tests/ -v`.
