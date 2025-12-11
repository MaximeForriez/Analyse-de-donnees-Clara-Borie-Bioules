import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats

# ------------------------------------------------------------
# Paramètres
# ------------------------------------------------------------
DATA_PATH = Path("Echantillonnage-100-Echantillons.csv")
OUT_ANOVA = Path("resultats_anova_echantillons.csv")
OUT_AFC_COORD = Path("resultats_afc_coordonnees.csv")
OUT_AFC_EIG = Path("resultats_afc_valeurs_propres.csv")

# ------------------------------------------------------------
# Chargement des données
# ------------------------------------------------------------
df = pd.read_csv(DATA_PATH)
df.columns = [c.strip() for c in df.columns]

print("Aperçu des données :")
print(df.head())

# ------------------------------------------------------------
# 1. ANOVA simple : comparaison des moyennes Pour / Contre / Sans opinion
# ------------------------------------------------------------
pour = df["Pour"].to_numpy(dtype=float)
contre = df["Contre"].to_numpy(dtype=float)
sans = df["Sans opinion"].to_numpy(dtype=float)

print("\nStatistiques descriptives par modalité :")
print("Pour :", df["Pour"].describe())
print("Contre :", df["Contre"].describe())
print("Sans opinion :", df["Sans opinion"].describe())

# ANOVA une voie (H0 : mêmes moyennes dans les 3 groupes)
F_stat, p_value = stats.f_oneway(pour, contre, sans)

print("\nANOVA une voie (Pour vs Contre vs Sans opinion) :")
print(f"  F = {F_stat:.4f}")
print(f"  p-value = {p_value:.4e}")

alpha = 0.05
if p_value < alpha:
    conclusion_anova = (
        "On rejette H0 : il existe au moins une différence significative "
        "entre les moyennes des trois positions."
    )
else:
    conclusion_anova = (
        "On ne rejette pas H0 : aucune différence significative détectée "
        "entre les moyennes des trois positions."
    )

print("  Conclusion :", conclusion_anova)

# Sauvegarde d'un résumé ANOVA
df_anova = pd.DataFrame(
    {
        "F_stat": [F_stat],
        "p_value": [p_value],
        "conclusion": [conclusion_anova],
    }
)
df_anova.to_csv(OUT_ANOVA, index=False)

# ------------------------------------------------------------
# 2. Construction du tableau moyen pour AFC
# ------------------------------------------------------------
# On agrège les 100 échantillons pour obtenir un tableau de contingence global
totaux = df[["Pour", "Contre", "Sans opinion"]].sum(axis=0)
tableau = pd.DataFrame(
    totaux.values.reshape(1, -1),
    index=["Total"],
    columns=["Pour", "Contre", "Sans opinion"],
)

print("\nTableau de contingence global (somme des 100 échantillons) :")
print(tableau)

# Pour une vraie AFC, il faut au moins 2 lignes.
# Ici, on simule des "lignes" en considérant chaque échantillon comme un individu
# (100 lignes, 3 colonnes), ce qui revient à faire une AFC sur df lui-même.

# Table de contingence pour AFC : 100 x 3
N = df.values
n_total = N.sum()

# Fréquences relatives
P = N / n_total

# Profils lignes et colonnes
r = P.sum(axis=1, keepdims=True)   # masses lignes
c = P.sum(axis=0, keepdims=True)   # masses colonnes

# Matrice des écarts au produit des marges
expected = r @ c                   # produit externe
S = P - expected                   # écarts

# Matrice centrée et pondérée (méthode du khi-deux)
D_r_inv_sqrt = np.diag(1.0 / np.sqrt(r.flatten()))
D_c_inv_sqrt = np.diag(1.0 / np.sqrt(c.flatten()))
Z = D_r_inv_sqrt @ S @ D_c_inv_sqrt

# Décomposition en valeurs singulières
U, singular_values, Vt = np.linalg.svd(Z, full_matrices=False)

eigenvalues = singular_values**2   # valeurs propres (inerties partielles)

# Coordonnées factorielles des colonnes (positions Pour/Contre/Sans opinion)
# sur les deux premiers axes
F_col = D_c_inv_sqrt @ Vt.T @ np.diag(singular_values)
coord_col = F_col[:, :2]  # 2 premiers axes

df_eig = pd.DataFrame(
    {
        "axe": np.arange(1, len(eigenvalues) + 1),
        "valeur_propre": eigenvalues,
        "pourcentage_inertie": 100 * eigenvalues / eigenvalues.sum(),
    }
)
df_eig.to_csv(OUT_AFC_EIG, index=False)

df_coord = pd.DataFrame(
    coord_col,
    index=["Pour", "Contre", "Sans opinion"],
    columns=["Dim1", "Dim2"],
)
df_coord.to_csv(OUT_AFC_COORD, index=True)

print("\nAnalyse factorielle des correspondances (AFC) :")
print("Valeurs propres (inerties) :")
print(df_eig)

print("\nCoordonnées des modalités (colonnes) sur les deux premiers axes :")
print(df_coord)

print("\nFichiers exportés :")
print(f"  - {OUT_ANOVA}")
print(f"  - {OUT_AFC_EIG}")
print(f"  - {OUT_AFC_COORD}")
