import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats

# ------------------------------------------------------------------
# Paramètres généraux
# ------------------------------------------------------------------
DATA_PATH = Path("./data/pib-vs-energie.csv")
ANNEE_DEBUT = 1962
ANNEE_FIN = 2022

# Dossier où ranger les fichiers de sortie
OUTPUT_DIR = Path("sorties_par_annee")
OUTPUT_DIR.mkdir(exist_ok=True)

# ------------------------------------------------------------------
# Chargement des données
# ------------------------------------------------------------------
df = pd.read_csv(DATA_PATH)
df.columns = [c.strip() for c in df.columns]

print("Colonnes :", df.columns.tolist())

# ------------------------------------------------------------------
# Fonction de traitement pour une année donnée
# ------------------------------------------------------------------
def traiter_annee(df: pd.DataFrame, annee: int) -> dict:
    col_pib = f"PIB_{annee}"
    col_energie = f"Utilisation_d_energie_{annee}"

    # Vérifier que les colonnes existent
    if col_pib not in df.columns or col_energie not in df.columns:
        print(f"Année {annee} : colonnes manquantes, ignorée.")
        return None

    # Extraire les deux colonnes + identifiants
    data = df[["Nom_du_territoire", "Code_ISO_du_territoire", col_pib, col_energie]].copy()
    data = data.rename(columns={col_pib: "PIB", col_energie: "Energie"})

    # Nettoyage
    data = data.dropna(subset=["PIB", "Energie"])

    if data.empty:
        print(f"Année {annee} : aucune donnée valide, ignorée.")
        return None

    # Statistiques de base
    cov_xy = data[["PIB", "Energie"]].cov().loc["PIB", "Energie"]
    corr, p_val = stats.pearsonr(data["PIB"], data["Energie"])
    R2 = corr**2

    # Régression linéaire « à la main »
    x = data["PIB"].to_numpy(dtype=float)
    y = data["Energie"].to_numpy(dtype=float)
    x_mean, y_mean = x.mean(), y.mean()
    Sxx = np.sum((x - x_mean)**2)
    Sxy = np.sum((x - x_mean)*(y - y_mean))
    slope = Sxy / Sxx
    intercept = y_mean - slope * x_mean

    # Sauvegarde des données détaillées de l’année
    out_year_path = OUTPUT_DIR / f"pib_energie_{annee}.csv"
    data.to_csv(out_year_path, index=False)

    # Retourner un résumé pour cette année
    return {
        "annee": annee,
        "nb_territoires": len(data),
        "covariance_pib_energie": cov_xy,
        "correlation_pearson": corr,
        "p_value_correlation": p_val,
        "R2": R2,
        "pente_regression": slope,
        "intercept_regression": intercept,
    }

# ------------------------------------------------------------------
# Boucle sur toutes les années + fichier récapitulatif
# ------------------------------------------------------------------
resultats = []

for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
    res = traiter_annee(df, annee)
    if res is not None:
        resultats.append(res)

# Créer un CSV de synthèse pour toutes les années
df_resume = pd.DataFrame(resultats)
df_resume.to_csv("resume_par_annee.csv", index=False)

print("\nFichiers créés :")
print(" - Détail par année dans le dossier 'sorties_par_annee/'")
print(" - Synthèse globale : resume_par_annee.csv")
