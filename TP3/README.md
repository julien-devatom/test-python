# TP3 LOG3430
Le dépot github est disponnible [ici](https://github.com/korrigans84/test-python), 
dans le dossier TP3. 

## Objectifs du TP
Nous introduisons 4 paramètres d'entrée à notre email analyzer : 
- use_log détermine si le calcul de la probabilité qu'un mot soit spam utilise le log ou non
- log_merge détermine si le calcul de la probabilité qu'un email soit spam utilise le log ou non
- frequency détermine la fréquence minimale d'un mot pour qu'il soit ajouté au dictionnaire (entre 1 et 4)
- cleaning_mode détermione comment on nettoie le texte. On a donc un entier entre 0 et 3 qui correspond aux clean suivant :
  - 0 pour faire stemming et enlever ”stop words”.
  - 1 pour ne pas faire stemming et enlever ”stop words”.
  - 2 pour faire stemming et ne pas enlever les ”stop words”.
  - 3 pour ne pas faire le stemming et pour ne pas enlever les ”stop words”
  
Nous voulons couvrir les plus de cas de tests, en utilisant des interractions plus 
 ou moins grandes, et en utilisant les résultats des jeux de tests générés par ACTS.

## Ou sont les résultats de l'ACTS ?
Pour chaque puissance (2, 3, 4), le dossier ACTS contient les jeux de tests pour chaque puissance : 
- Puissance 2 : ACTS/output_interact_2.csv
- Puissance 3 : ACTS/output_interact_3.csv
- Puissance 4 : ACTS/output_interact_4.csv

Le fichier ACTS/output.csv est celui qui est utilisé lorsque l'on test notre code en lancant le script main.py

## Executer le script
Pour executer le script, lancez la commande suivante à la racine de ce fichier : 
```bash
python3 main.py
```
L'execution peut prendre plus ou moins de temps suivant la taille du jeu de tests.
Dans le cadre du TP, le test avec l'interraction de 3 contient

## Resultats
Les resultats obtenu par l'execution des jeux de tests avec une interraction de 3 sont présent dans le fichier 
src/results.csv