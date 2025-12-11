# fichier : src/bonus_rangs.py


import os
import pandas as pd
from scipy.stats import spearmanr, kendalltau




# ------------------ OUTIL GÉNÉRIQUE D’ANALYSE DE RANGS ----------------------




def analyse_rangs(liste_x, liste_y):
   """
   Reçoit deux listes (classements ou valeurs) de même longueur et renvoie
   les coefficients de corrélation de Spearman et de Kendall.


   Retourne (rs, p_s, tau, p_k).
   """
   rs, p_s = spearmanr(liste_x, liste_y)
   tau, p_k = kendalltau(liste_x, liste_y)
   return rs, p_s, tau, p_k




# ----------------------------- PARTIE ÎLES ----------------------------------




def bonus_iles():
   """
   Compare le classement des îles par surface et par trait de côte
   en utilisant les coefficients de Spearman et de Kendall.
   Fichier utilisé : data/island-index.csv
   """
   base_dir = os.path.dirname(os.path.dirname(__file__))
   chemin_csv = os.path.join(base_dir, "data", "island-index.csv")
   df = pd.read_csv(chemin_csv, low_memory=False)


   # Colonnes réelles utilisées dans le TP sur les îles
   surf_col = "Surface (km²)"
   coast_col = "Trait de côte (km)"


   # On ne garde que les lignes où les deux colonnes sont valides
   df_sub = df[[surf_col, coast_col]].dropna().copy()
   df_sub[surf_col] = df_sub[surf_col].astype(float)
   df_sub[coast_col] = df_sub[coast_col].astype(float)


   # Création des rangs (ordre décroissant pour un classement « du plus grand au plus petit »)
   df_sub["rang_surface"] = df_sub[surf_col].rank(method="average", ascending=False)
   df_sub["rang_trait"] = df_sub[coast_col].rank(method="average", ascending=False)


   rang_surf = df_sub["rang_surface"].tolist()
   rang_trait = df_sub["rang_trait"].tolist()


   rs, p_s, tau, p_k = analyse_rangs(rang_surf, rang_trait)


   print("\n=== ÎLES : comparaison du classement par surface et par trait de côte ===")
   print(f"Nombre d'îles utilisées : {len(df_sub)}")
   print(f"Spearman r_s = {rs:.3f}, p-value = {p_s:.3g}")
   print(f"Kendall  tau = {tau:.3f}, p-value = {p_k:.3g}")
   # À commenter dans le rapport : plus r_s et tau sont proches de 1 (et p petits),
   # plus les deux classements sont concordants (îles grandes en surface aussi grandes en trait de côte).




# ----------------------- PARTIE POPULATION MONDIALE ------------------------




def ouvrir_un_fichier_etats():
   """Ouvre le fichier Le-Monde-HS-Etats-du-monde-2007-2025.csv."""
   base_dir = os.path.dirname(os.path.dirname(__file__))
   chemin_csv = os.path.join(base_dir, "data", "Le-Monde-HS-Etats-du-monde-2007-2025.csv")
   df = pd.read_csv(chemin_csv)
   return df




def ordrePopulation(liste_valeurs, liste_etats):
   """
   Ordonne de manière décroissante la liste 'liste_valeurs'
   en conservant la correspondance avec 'liste_etats'.


   Retourne (valeurs_ordonnee, etats_ordonnes).
   """
   couples = list(zip(liste_valeurs, liste_etats))
   couples_triees = sorted(couples, key=lambda x: x[0], reverse=True)
   valeurs_ord = [v for v, e in couples_triees]
   etats_ord = [e for v, e in couples_triees]
   return valeurs_ord, etats_ord




def classementPays(etats_pop, etats_densite):
   """
   Prépare la comparaison de deux classements :
   - etats_pop : liste d'États classés selon la population (ordre décroissant)
   - etats_densite : liste d'États classés selon la densité (ordre décroissant)


   Retour : liste de tuples (rang_pop, rang_dens) triés par rang_pop.
   """
   rang_pop = {etat: i + 1 for i, etat in enumerate(etats_pop)}
   rang_dens = {etat: i + 1 for i, etat in enumerate(etats_densite)}


   etats_communs = [e for e in etats_pop if e in rang_dens]
   couples_rangs = [(rang_pop[e], rang_dens[e]) for e in etats_communs]
   couples_rangs.sort(key=lambda x: x[0])
   return couples_rangs




def analyse_une_annee(df, annee):
   """
   1) construit les classements par population et densité pour une année donnée,
   2) fabrique les deux listes de rangs,
   3) renvoie (rs, p_s, tau, p_k) pour cette année.
   """
   col_pop = f"Pop {annee}"
   col_dens = f"Densité {annee}"


   etats = df["État"].tolist()
   pop = df[col_pop].astype(float).tolist()
   dens = df[col_dens].astype(float).tolist()


   _, etats_pop = ordrePopulation(pop, etats)
   _, etats_dens = ordrePopulation(dens, etats)


   couples = classementPays(etats_pop, etats_dens)
   rang_pop = [c[0] for c in couples]
   rang_dens = [c[1] for c in couples]


   return analyse_rangs(rang_pop, rang_dens)




def bonus_population_mondiale():
   """
   1. Factorise l’analyse des rangs dans analyse_une_annee().
   2. Analyse la concordance des rangs pour toutes les années 2007–2025.
   """
   df = ouvrir_un_fichier_etats()


   print("\n=== POPULATION MONDIALE : analyse des classements 2007–2025 ===")
   resultats = []


   for annee in range(2007, 2025 + 1):
       rs, p_s, tau, p_k = analyse_une_annee(df, annee)
       resultats.append((annee, rs, p_s, tau, p_k))
       print(f"Année {annee} : Spearman r_s = {rs:.3f} (p={p_s:.3g}), "
             f"Kendall tau = {tau:.3f} (p={p_k:.3g})")


   # Commentaire possible dans le rapport :
   # - repérer les années où rs / tau sont élevés → forte stabilité du lien
   #   entre classement par population et par densité.
   # - repérer les années où rs / tau se rapprochent de 0 ou changent de signe → hiérarchies différentes.




# ----------------------------- LANCEUR --------------------------------------




def main():
   # Partie îles
   bonus_iles()


   # Partie population mondiale
   bonus_population_mondiale()




if __name__ == "__main__":
   main()


