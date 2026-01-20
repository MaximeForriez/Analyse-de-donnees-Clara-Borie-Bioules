# fichier : src/main.py


import os
import math
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr, kendalltau




# --------------------------------------------------------------------
# 2. Fonction locale ouvrirUnFichier()
# --------------------------------------------------------------------
def ouvrirUnFichier(chemin_fichier: str) -> pd.DataFrame:
   """
   Ouvre un fichier CSV et renvoie un DataFrame pandas.
   Le paramètre est une chaîne de caractères (chemin + nom du fichier).
   """
   if not os.path.exists(chemin_fichier):
       raise FileNotFoundError(f"Fichier introuvable : {chemin_fichier}")
   # low_memory=False pour éviter le warning de typage mixte
   df = pd.read_csv(chemin_fichier, low_memory=False)
   return df




# --------------------------------------------------------------------
# 4. Fonction locale ordreDecroissant()
# --------------------------------------------------------------------
def ordreDecroissant(liste):
   """Retourne une nouvelle liste triée en ordre décroissant."""
   return sorted(liste, reverse=True)




# --------------------------------------------------------------------
# 6. Fonction locale conversionLog()
# --------------------------------------------------------------------
def conversionLog(liste):
   """Retourne une nouvelle liste avec log10 des valeurs strictement positives."""
   return [math.log10(x) for x in liste if x > 0]




# --------------------------------------------------------------------
# Fonctions utilitaires pour les tests de rangs (Spearman / Kendall)
# --------------------------------------------------------------------
def test_spearman_kendall(rangs):
   """
   Exemple de test sur les rangs :
   on teste la corrélation entre le rang et 1/rang (simple illustration).
   """
   import numpy as np


   r = np.array(rangs, dtype=float)
   y = 1.0 / r  # relation monotone décroissante


   rs, p_s = spearmanr(r, y)
   tau, p_k = kendalltau(r, y)


   print("\nExemple de test sur les rangs (rang vs 1/rang) :")
   print(f"  Spearman r_s = {rs:.3f}, p-value = {p_s:.3g}")
   print(f"  Kendall tau = {tau:.3f}, p-value = {p_k:.3g}")


   # 7. Réponse (sous forme de commentaire dans le code) :
   # Oui, il est possible de faire un test sur les rangs.
   # On peut utiliser par exemple les tests de Spearman ou de Kendall
   # pour tester l'existence d'une relation monotone entre deux classements
   # ou entre les rangs et une autre variable ordinale ou quantitative.




# --------------------------------------------------------------------
# Programme principal : étapes 2 à 7
# --------------------------------------------------------------------
def main():
   # 2. Ouvrir le fichier avec ouvrirUnFichier()
   base_dir = os.path.dirname(os.path.dirname(__file__))  # remonte à la racine du projet
   chemin_csv = os.path.join(base_dir, "data", "island-index.csv")
   df = ouvrirUnFichier(chemin_csv)


   print("Aperçu des données :")
   print(df.head())
   print("\nColonnes disponibles :")
   print(list(df.columns))


   # 3. Isoler la colonne « Surface (km²) » et ajouter les continents
   surface_col = "Surface (km²)"
   # Forcer le typage en float
   surfaces = df[surface_col].astype(float).tolist()


   # Surfaces continentales (sans unité, en km²)
   surfaces_continents = [
       85545323.0,  # Asie / Afrique / Europe
       37856841.0,  # Amérique
       7768030.0,   # Antarctique
       7605049.0,   # Australie
   ]
   surfaces.extend(surfaces_continents)


   # 4. Ordonner la liste obtenue (ordre décroissant)
   surfaces_ordonnee = ordreDecroissant(surfaces)


   # 5. Visualiser la loi rang-taille (échelle linéaire)
   rangs = list(range(1, len(surfaces_ordonnee) + 1))


   plt.figure(figsize=(6, 4))
   plt.plot(rangs, surfaces_ordonnee, marker="o", linestyle="none", markersize=2)
   plt.xlabel("Rang")
   plt.ylabel("Surface (km²)")
   plt.title("Loi rang-taille (surfaces d'îles + continents)")
   plt.tight_layout()
   plt.savefig(os.path.join(base_dir, "rang_taille_lineaire.png"))
   plt.close()


   # 6. Conversion des axes en logarithme (log10)
   rangs_log = conversionLog(rangs)
   surfaces_log = conversionLog(surfaces_ordonnee)


   plt.figure(figsize=(6, 4))
   plt.plot(rangs_log, surfaces_log, marker="o", linestyle="none", markersize=2)
   plt.xlabel("log10(Rang)")
   plt.ylabel("log10(Surface)")
   plt.title("Loi rang-taille (log-log)")
   plt.tight_layout()
   plt.savefig(os.path.join(base_dir, "rang_taille_loglog.png"))
   plt.close()


   print("\nImages enregistrées à la racine du projet :")
   print("  rang_taille_lineaire.png")
   print("  rang_taille_loglog.png")


   # 7. Exemple de test sur les rangs (commentaire explicatif dans la fonction)
   test_spearman_kendall(rangs)




if __name__ == "__main__":
   main()
# fichier : src/etats_rangs.py


import os
import pandas as pd
from scipy.stats import spearmanr, kendalltau




# --------------------------------------------------------------------
# 9. Fonction locale ouvrirUnFichier()
# --------------------------------------------------------------------
def ouvrirUnFichier(chemin_fichier: str) -> pd.DataFrame:
   """
   Ouvre un fichier CSV et renvoie un DataFrame pandas.
   Le paramètre est une chaîne de caractères (chemin + nom du fichier).
   """
   if not os.path.exists(chemin_fichier):
       raise FileNotFoundError(f"Fichier introuvable : {chemin_fichier}")
   df = pd.read_csv(chemin_fichier)
   return df




# --------------------------------------------------------------------
# 11. Fonction locale ordrePopulation()
# --------------------------------------------------------------------
def ordrePopulation(liste_valeurs, liste_etats):
   """
   Ordonne de manière décroissante la liste 'liste_valeurs'
   en conservant la correspondance avec 'liste_etats'.


   Retourne :
     - liste des valeurs ordonnées
     - liste des États réordonnés
   """
   couples = list(zip(liste_valeurs, liste_etats))
   couples_triees = sorted(couples, key=lambda x: x[0], reverse=True)
   valeurs_ord = [v for v, e in couples_triees]
   etats_ord = [e for v, e in couples_triees]
   return valeurs_ord, etats_ord




# --------------------------------------------------------------------
# 12. Fonction locale classementPays()
# --------------------------------------------------------------------
def classementPays(etats_pop, etats_densite):
   """
   Prépare la comparaison de deux classements :
   - etats_pop : liste d'États classés selon la population (ordre décroissant)
   - etats_densite : liste d'États classés selon la densité (ordre décroissant)


   Retour :
     - liste de tuples (rang_pop, rang_dens)
       alignés sur les mêmes États, triés par rang_pop.
   """
   rang_pop = {etat: i + 1 for i, etat in enumerate(etats_pop)}
   rang_dens = {etat: i + 1 for i, etat in enumerate(etats_densite)}


   etats_communs = [e for e in etats_pop if e in rang_dens]


   couples_rangs = [(rang_pop[e], rang_dens[e]) for e in etats_communs]
   couples_rangs.sort(key=lambda x: x[0])


   return couples_rangs




# --------------------------------------------------------------------
# 9–14. Programme principal
# --------------------------------------------------------------------
def main():
   base_dir = os.path.dirname(os.path.dirname(__file__))
   chemin_csv = os.path.join(base_dir, "data", "Le-Monde-HS-Etats-du-monde-2007-2025.csv")


   # 9. Ouvrir le fichier
   df = ouvrirUnFichier(chemin_csv)


   print("Aperçu des données :")
   print(df.head())
   print("\nColonnes disponibles :")
   print(list(df.columns))


   # 10. Isoler les colonnes utiles
   colonnes = ["État", "Pop 2007", "Pop 2025", "Densité 2007", "Densité 2025"]
   for col in colonnes:
       if col not in df.columns:
           raise ValueError(f"Colonne manquante dans le CSV : {col}")


   etats = df["État"].tolist()
   pop_2007 = df["Pop 2007"].astype(float).tolist()
   pop_2025 = df["Pop 2025"].astype(float).tolist()
   dens_2007 = df["Densité 2007"].astype(float).tolist()
   dens_2025 = df["Densité 2025"].astype(float).tolist()


   # 11. Ordonner de manière décroissante les listes
   pop2007_ord, etats_pop2007 = ordrePopulation(pop_2007, etats)
   pop2025_ord, etats_pop2025 = ordrePopulation(pop_2025, etats)
   dens2007_ord, etats_dens2007 = ordrePopulation(dens_2007, etats)
   dens2025_ord, etats_dens2025 = ordrePopulation(dens_2025, etats)


   # 12. Préparer la comparaison des classements (population vs densité)
   couples_rangs_2007 = classementPays(etats_pop2007, etats_dens2007)
   couples_rangs_2025 = classementPays(etats_pop2025, etats_dens2025)


   # 13. Isoler les deux colonnes de rangs sous forme de listes
   rang_pop_2007 = [c[0] for c in couples_rangs_2007]
   rang_dens_2007 = [c[1] for c in couples_rangs_2007]


   rang_pop_2025 = [c[0] for c in couples_rangs_2025]
   rang_dens_2025 = [c[1] for c in couples_rangs_2025]


   # 14. Corrélation des rangs (Spearman) et concordance (Kendall)
   # 2007
   rs_2007, p_s_2007 = spearmanr(rang_pop_2007, rang_dens_2007)
   tau_2007, p_k_2007 = kendalltau(rang_pop_2007, rang_dens_2007)


   print("\nAnnée 2007 :")
   print(f"  Spearman r_s = {rs_2007:.3f}, p-value = {p_s_2007:.3g}")
   print(f"  Kendall tau = {tau_2007:.3f}, p-value = {p_k_2007:.3g}")


   # 2025
   rs_2025, p_s_2025 = spearmanr(rang_pop_2025, rang_dens_2025)
   tau_2025, p_k_2025 = kendalltau(rang_pop_2025, rang_dens_2025)


   print("\nAnnée 2025 :")
   print(f"  Spearman r_s = {rs_2025:.3f}, p-value = {p_s_2025:.3g}")
   print(f"  Kendall tau = {tau_2025:.3f}, p-value = {p_k_2025:.3g}")


   # Commentaire à mettre dans le rapport :
   # - Si r_s et tau sont proches de 1 : les États les plus peuplés sont aussi
   #   parmi les plus denses (hiérarchie similaire).
   # - S'ils sont proches de 0 : peu de lien entre le classement par population
   #   et celui par densité.
   # - S'ils sont négatifs : les États très peuplés ne sont pas ceux qui sont
   #   les plus denses, ce qui signale une inversion de hiérarchie.




if __name__ == "__main__":
   main()
