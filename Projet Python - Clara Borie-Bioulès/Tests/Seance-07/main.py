import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------------------------------------------
# Paramètres généraux
# ------------------------------------------------------------------
DATA_PATH = Path("./data/pib-vs-energie.csv")
TERRITOIRE_CIBLE = "France"    # à adapter si besoin
ANNEE_DEBUT = 1990
ANNEE_FIN = 2020

# ------------------------------------------------------------------
# Étape 1 – Chargement et nettoyage de base
# ------------------------------------------------------------------
def charger_donnees(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Standardisation minimale des noms de colonnes
    df.columns = [c.strip() for c in df.columns]
    return df

df = charger_donnees(DATA_PATH)

# Vérification rapide
print("Dimensions du fichier :", df.shape)
print("Colonnes disponibles :")
print(df.columns.tolist())

# ------------------------------------------------------------------
# Étape 2 – Mise en forme pour une analyse bivariée (PIB vs énergie)
# ------------------------------------------------------------------
# Hypothèse : colonnes de type 'PIBYYYY' et 'UtilisationdenergieYYYY'
colonnes_pib = [c for c in df.columns if c.startswith("PIB")]
colonnes_energie = [c for c in df.columns if c.startswith("Utilisationdenergie")]

# Extraire le territoire étudié
df_territoire = df[df["Nomduterritoire"] == TERRITOIRE_CIBLE].copy()

# Mise au format long
pib_long = df_territoire.melt(
    id_vars=["Nomduterritoire", "CodeISOduterritoire"],
    value_vars=colonnes_pib,
    var_name="Annee",
    value_name="PIB"
)
pib_long["Annee"] = pib_long["Annee"].str.replace("PIB", "").astype(int)

energie_long = df_territoire.melt(
    id_vars=["Nomduterritoire", "CodeISOduterritoire"],
    value_vars=colonnes_energie,
    var_name="Annee",
    value_name="Energie"
)
energie_long["Annee"] = energie_long["Annee"].str.replace("Utilisationdenergie", "").astype(int)

# Fusion PIB + énergie
df_long = pd.merge(
    pib_long[["Nomduterritoire", "CodeISOduterritoire", "Annee", "PIB"]],
    energie_long[["Annee", "Energie"]],
    on="Annee",
    how="inner"
)

# Filtrer sur une période
df_long = df_long[(df_long["Annee"] >= ANNEE_DEBUT) & (df_long["Annee"] <= ANNEE_FIN)].copy()

# Suppression des lignes manquantes
df_long = df_long.dropna(subset=["PIB", "Energie"])

print("\nAperçu des données longues :")
print(df_long.head())

# ------------------------------------------------------------------
# Étape 3 – Statistiques descriptives (univariées et bivariées)
# ------------------------------------------------------------------
print("\nStatistiques descriptives PIB :")
print(df_long["PIB"].describe())

print("\nStatistiques descriptives Utilisation d'énergie :")
print(df_long["Energie"].describe())

# Tableau croisé simple par année (optionnel)
table_annee = df_long[["Annee", "PIB", "Energie"]].set_index("Annee")
print("\nAperçu série temporelle (PIB/Energie par année) :")
print(table_annee.head())

# ------------------------------------------------------------------
# Étape 4 – Corrélation, covariance, régression linéaire
# ------------------------------------------------------------------
x = df_long["PIB"].values
y = df_long["Energie"].values

# Covariance et corrélation
cov_xy = np.cov(x, y, ddof=1)[0, 1]
corr_pearson, p_value = stats.pearsonr(x, y)
coeff_determination = corr_pearson**2

print(f"\nCovariance PIB–Energie : {cov_xy:.4e}")
print(f"Corrélation de Pearson r : {corr_pearson:.4f} (p = {p_value:.4g})")
print(f"Coefficient de détermination R² : {coeff_determination:.4f}")

# Régression linéaire (méthode des moindres carrés)
slope, intercept, r_value, p_val_reg, stderr = stats.linregress(x, y)
print("\nRégression linéaire Energie = a + b * PIB")
print(f"  a (intercept) = {intercept:.4e}")
print(f"  b (pente)     = {slope:.4e}")
print(f"  r             = {r_value:.4f}")
print(f"  R²            = {r_value**2:.4f}")
print(f"  p-value       = {p_val_reg:.4g}")

# ------------------------------------------------------------------
# Étape 5 – Visualisations (nuage de points, droite de régression)
# ------------------------------------------------------------------
sns.set(style="whitegrid")

plt.figure(figsize=(8, 6))
sns.scatterplot(data=df_long, x="PIB", y="Energie")
# Droite de régression
x_vals = np.linspace(df_long["PIB"].min(), df_long["PIB"].max(), 100)
y_hat = intercept + slope * x_vals
plt.plot(x_vals, y_hat, color="red", label="Régression linéaire")
plt.xlabel("PIB (niveau ou log, selon le fichier)")
plt.ylabel("Utilisation d'énergie")
plt.title(f"{TERRITOIRE_CIBLE} – PIB vs Utilisation d'énergie ({ANNEE_DEBUT}-{ANNEE_FIN})")
plt.legend()
plt.tight_layout()
plt.show()

# ------------------------------------------------------------------
# Étape 6 – Sauvegarde des résultats (CSV)
# ------------------------------------------------------------------
# Sauvegarder les données utilisées pour les analyses
df_long.to_csv("resultats_pib_energie_long.csv", index=False)

# Sauvegarder un petit résumé statistique
resume = {
    "covariance_pib_energie": [cov_xy],
    "correlation_pearson": [corr_pearson],
    "p_value_correlation": [p_value],
    "R2": [coeff_determination],
    "pente_regression": [slope],
    "intercept_regression": [intercept],
    "p_value_regression": [p_val_reg]
}
df_resume = pd.DataFrame(resume)
df_resume.to_csv("resume_stats_pib_energie.csv", index=False)

print("\nFichiers exportés :")
print(" - resultats_pib_energie_long.csv")
print(" - resume_stats_pib_energie.csv")
