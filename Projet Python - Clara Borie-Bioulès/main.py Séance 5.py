import csv
from math import sqrt


def ouvrirUnFichier(chemin):
   with open(chemin, "r", encoding="utf-8") as f:
       lecteur = csv.reader(f)
       next(lecteur)  # saute la première ligne (en-tête)
       return [row for row in lecteur]


def moyenne_colonnes(donnees):
   nb_colonnes = len(donnees[0])
   colonnes = [[] for _ in range(nb_colonnes)]
   for row in donnees:
       for i, val in enumerate(row):
           # enlever les espaces et les éventuelles virgules dans les grands nombres
           colonnes[i].append(int(val.replace(" ", "").replace(",", "")))
   moyennes = [round(sum(col) / len(col)) for col in colonnes]
   return moyennes


def frequences(valeurs):
   total = sum(valeurs)
   return [round(v / total, 2) for v in valeurs]


def intervalle_fluctuation(freq, n, z=1.96):
   intervalles = []
   for f in freq:
       delta = z * sqrt(f * (1 - f) / n)
       intervalles.append((round(f - delta, 2), round(f + delta, 2)))
   return intervalles


# --- Main ---
donnees = ouvrirUnFichier("data/Echantillonnage-100-Echantillons.csv")
moyennes = moyenne_colonnes(donnees)
freq_echantillon = frequences(moyennes)


# Population mère (à adapter selon ton exercice)
freq_population = [0.3, 0.5, 0.2]
n = sum(moyennes)


intervalles = intervalle_fluctuation(freq_population, n)


print("Moyennes par opinion :", moyennes)
print("Fréquences de l'échantillon :", freq_echantillon)
print("Fréquences de la population mère :", freq_population)
print("Intervalles de fluctuation à 95% :", intervalles)


print("\nConclusion : Les fréquences de l'échantillon doivent se situer dans l'intervalle de fluctuation des fréquences de la population mère. Des écarts sont possibles à cause de la variabilité des échantillons.")

import pandas as pd
import math


# Charger le fichier CSV
df = pd.read_csv("data/Echantillonnage-100-Echantillons.csv", sep=",")
print(df.head())  # Affiche les 5 premières lignes pour vérifier


# Sélection du premier échantillon
premier_echantillon = list(df.iloc[0].astype(int))
print("Premier échantillon :", premier_echantillon)


# Taille totale de l'échantillon
taille_echantillon = sum(premier_echantillon)


# Fréquences de chaque opinion
frequences = [val / taille_echantillon for val in premier_echantillon]
print("Fréquences du premier échantillon :", frequences)


z = 1.96


ic = []
for p in frequences:
   ecart_type = math.sqrt(p * (1 - p) / taille_echantillon)
   borne_inf = p - z * ecart_type
   borne_sup = p + z * ecart_type
   ic.append((round(borne_inf, 2), round(borne_sup, 2)))


print("Intervalle de confiance à 95% :", ic)

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import shapiro, probplot


# --- Fichiers CSV ---
fichiers = ["data/Loi-normale-Test-1.csv", "data/Loi-normale-Test-2.csv"]


for fichier in fichiers:
   # Lire le CSV
   df = pd.read_csv(fichier)
  
   # Extraire la colonne (supposons qu'il n'y ait qu'une colonne de données)
   valeurs = df.iloc[:, 0].dropna()
  
   print(f"\nAnalyse pour {fichier} :")
  
   # 1. Histogramme avec densité estimée
   plt.figure(figsize=(8, 4))
   plt.hist(valeurs, bins=20, density=True, alpha=0.6, color='g', edgecolor='black')
   plt.title(f"Histogramme de {fichier}")
   plt.xlabel("Valeurs")
   plt.ylabel("Densité")
   plt.show()
  
   # 2. QQ-plot
   plt.figure(figsize=(6, 6))
   probplot(valeurs, dist="norm", plot=plt)
   plt.title(f"QQ-plot de {fichier}")
   plt.show()
  
   # 3. Test de Shapiro-Wilk
   stat, p = shapiro(valeurs)
   print(f"Test de Shapiro-Wilk : Statistique = {stat:.4f}, p-value = {p:.4f}")
   if p > 0.05:
       print("→ Cette série peut être considérée comme suivant une loi normale.")
   else:
       print("→ Cette série ne suit pas une loi normale.")