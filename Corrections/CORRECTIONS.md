# Élements de corrections

## Séance 4.

### Questions

- **Question 1.** On sent que vous avez compris, mais il manque quelques éléménts.

### Code

- Pourquoi ne pas avoir enregistré les images produites ?

## Séance 5.

### Questions

- **Question 5.** Point de détail : on parle de statistique exhaustive, et non d'enquête exhaustive. L'enquête renvoie à la méthode de la collecte des données.

### Code

- Excellent !

## Séance 6

### Questions

- Excellent !

### Code

- Je n'arrive pas à exécuter votre code sur ma machine. Pourquoi avoir modifié `def ouvrirUnFichier():` ?

- **Question 7.** Il n'est pas possible d'effectuer un test sur un seul classement. Il en faux au moins deux.

- Vous avez mal comparé les classements. Vous avez écrit :

```
       # 14. Corrélation des rangs (Spearman) et concordance (Kendall)
        # 2007
        rs_2007, p_s_2007 = spearmanr(rang_pop_2007, rang_dens_2007)
        tau_2007, p_k_2007 = kendalltau(rang_pop_2007, rang_dens_2007)

        # 2025
        rs_2025, p_s_2025 = spearmanr(rang_pop_2025, rang_dens_2025)
        tau_2025, p_k_2025 = kendalltau(rang_pop_2025, rang_dens_2025)
```

Il fallait écrire :

```
       # 14. Corrélation des rangs (Spearman) et concordance (Kendall)
        # Population
        rs_pop, p_s_pop = spearmanr(rang_pop_2007, rang_pop_2025)
        tau_pop, p_k_pop = kendalltau(rang_pop_2007, rang_pop_2025)

        # 2025
        rs_dens, p_s_dens = spearmanr(rang_dens_2007, rang_dens_2025)
        tau_dens, p_k_dens = kendalltau(rang_dens_2007, rang_dens_2025)
```

- **Question bonus.** La généralisation est bonne, mais ce ne sont pas les bonnes listes comparées.

## Séance 7

### Questions

- **Question 2.** La corrélation concerne les variables qualitatives, tandis que la corrélation concerne les variables quantitatives. Le rapport de corrélation étudie le rapport entre une variable qualitative et une variable quantitatitve.

### Code

- Je n'arrive pas à exécuter votre code sur ma machine. Pourquoi avoir modifié `def ouvrirUnFichier():` ?

- Il y a un problème dans le calcul de votre régression linéaire. La corrélation est beaucoup plus forte. Il semble que votre algorithme triant les données à censurer en exclut trop.

## Séance 8

### Questions

- **Question 1.** La corrélation entre deux variables qualitatives n'a aucun sens et est rarement calculable.

### Code

- Impressionnant algorithmique pour le bonus sur l'ANOVA et l'A.F.C., mais il existe déjà des [bibliothèques](https://github.com/MaximeForriez/Sorbonne-M1-Analyse-de-donnees/blob/main/Python/PYTHON-STATISTIQUES-MULTIVARIEES.md) pour faire les calculs. Cela prouve votre compréhension du cours. Bravo !

## Humanités numériques

- Aucun rendu.

## Remarques générales

- Aucun dépôt régulier sur `GitHub`.

- Je suis navré que vous ayez eu autant de problèmes techniques. Je vous félicite pour votre acharnement et vos solutions ingénieuses. La solution `venv` mise en place est une solution acceptable et largement utilisée à la place de `Docker`.

- Point de détail. Il fallait laisser par dossier le fichier `main.py`. C'est une convention de nommage que vous comprendrez si vous faites du `Python` avancé.
