# Journal d'utilisation de l'IA

Ce journal décrit l'aide reçue et les vérifications réellement effectuées.

| Date | Outil | Ce que nous avons demandé | Réponse reçue | Vérification faite | Décision |
| --- | --- | --- | --- | --- | --- |
| 19 novembre 2026 | ChatGPT / Codex | Ajouter des docstrings en français naturel et des annotations de type dans le code et les tests, puis noter cette aide dans le journal. | Ajout ou précision des docstrings et des types pour les 38 fonctions et méthodes. Les descriptions expliquent les paramètres, les résultats et les principales erreurs possibles, sans modifier la logique. | Codex a vérifié que chaque fonction possède une docstring et des annotations pour ses paramètres (sauf self) et son retour. La comparaison du code avant et après, en retirant ces ajouts, confirme que la logique est identique. Les 8 tests passent avec `python3 -B -m pytest tests/ -v -p no:cacheprovider`. | Changements conservés dans le projet après ces vérifications. La relecture par les deux membres de l'équipe reste à faire pour confirmer qu'ils comprennent et approuvent les descriptions. |
