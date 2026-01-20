
import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import chi2_contingency

# ------------------------------------------------------------
# Paramètres
# ------------------------------------------------------------
DATA_PATH = Path("./data/Socioprofessionnelle-vs-sexe.csv")
OUTPUT_RESUME = Path("./data/resultats_chi2_socioprofessionnelle_sexe.csv")

# ------------------------------------------------------------
# Fonctions locales pour les marges
# ------------------------------------------------------------
def sommeDesLignes(tableau: np.ndarray) -> np.ndarray:
    """Retourne la somme de chaque ligne (marges de lignes)."""
    return tableau.sum(axis=1)

def sommeDesColonnes(tableau: np.ndarray) -> np.ndarray:
    """Retourne la somme de chaque colonne (marges de colonnes)."""
    return tableau.sum(axis=0)

# ------------------------------------------------------------
# 1. Chargement des données
# ------------------------------------------------------------
df = pd.read_csv(DATA_PATH)

# On garde seulement les effectifs du tableau de contingence
# (ici colonnes 'Femmes' et 'Hommes')
contingence = df[["Femmes", "Hommes"]].to_numpy(dtype=float)

categories = df["Catégorie"].tolist()
modalites_sexe = ["Femmes", "Hommes"]

print("Tableau de contingence (effectifs) :")
print(pd.DataFrame(contingence, index=categories, columns=modalites_sexe))

# ------------------------------------------------------------
# 1. Marges des lignes et des colonnes
# ------------------------------------------------------------
marges_lignes = sommeDesLignes(contingence)
marges_colonnes = sommeDesColonnes(contingence)

print("\nMarges de lignes :")
for cat, m in zip(categories, marges_lignes):
    print(f"{cat} : {int(m)}")

print("\nMarges de colonnes :")
for sex, m in zip(modalites_sexe, marges_colonnes):
    print(f"{sex} : {int(m)}")

total_lignes = marges_lignes.sum()
total_colonnes = marges_colonnes.sum()

print(f"\nTotal des marges de lignes : {int(total_lignes)}")
print(f"Total des marges de colonnes : {int(total_colonnes)}")

# ------------------------------------------------------------
# 2. Vérification égalité des totaux des marges
# ------------------------------------------------------------
if np.isclose(total_lignes, total_colonnes):
    print("\nVérification : le total des marges de lignes est égal au total des marges de colonnes.")
else:
    print("\nAttention : les totaux des marges de lignes et de colonnes diffèrent !")

# ------------------------------------------------------------
# 3. Test d'indépendance du chi2
# ------------------------------------------------------------
chi2, p_value, dof, expected = chi2_contingency(contingence)

print("\nTest du chi2 d'indépendance :")
print(f"  Chi2 = {chi2:.4f}")
print(f"  ddl  = {dof}")
print(f"  p-value = {p_value:.4e}")

alpha = 0.05
if p_value < alpha:
    conclusion = "On rejette l'hypothèse d'indépendance : il existe une liaison entre catégorie socioprofessionnelle et sexe."
else:
    conclusion = "On ne rejette pas l'hypothèse d'indépendance : aucune liaison significative détectée au seuil de 5%."

print("  Conclusion :", conclusion)

# ------------------------------------------------------------
# 4. Intensité de liaison phi2 de Pearson
# ------------------------------------------------------------
n = contingence.sum()
phi2 = chi2 / n

print(f"\nIntensité de liaison phi^2 de Pearson : {phi2:.4f}")

# Quelques repères (optionnels) :
# - phi2 proche de 0 : liaison très faible
# - plus phi2 est élevé, plus la liaison est forte (bornes dépendent du tableau)

# ------------------------------------------------------------
# 5. Sauvegarde d'un résumé des résultats
# ------------------------------------------------------------
resume = {
    "n_total": [int(n)],
    "chi2": [chi2],
    "ddl": [dof],
    "p_value": [p_value],
    "phi2": [phi2],
    "conclusion": [conclusion],
}

df_resume = pd.DataFrame(resume)
df_resume.to_csv(OUTPUT_RESUME, index=False)

print(f"\nRésumé des résultats sauvegardé dans : {OUTPUT_RESUME}")
