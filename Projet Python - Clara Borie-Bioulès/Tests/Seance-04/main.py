import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def moyenne(data):
    return np.mean(data)


def ecart_type(data):
    return np.std(data)


def plot_distribution(distribution, params=None, size=1000, title="Distribution"):
    """
    Génère un histogramme pour une distribution donnée et calcule moyenne et écart type.

    distribution : fonction scipy.stats (ex : stats.binom) OU fonction générant des données
    params : dictionnaire des paramètres de la distribution
    size : nombre de valeurs à générer
    title : titre de l'histogramme
    """
    if params is None:
        params = {}

    # Si c'est un objet scipy.stats (avec .rvs), on l'utilise pour générer les données
    if hasattr(distribution, "rvs"):
        data = distribution.rvs(size=size, **params)
    else:
        # Sinon on considère que c'est une fonction Python qui prend size en argument
        data = distribution(size=size, **params)

    mean = moyenne(data)
    std = ecart_type(data)

    plt.figure(figsize=(6, 4))
    plt.hist(data, bins=30, density=True, alpha=0.7,
             color='skyblue', edgecolor='black')
    plt.title(f"{title}\nMoyenne = {mean:.2f}, Écart type = {std:.2f}")
    plt.xlabel("Valeurs")
    plt.ylabel("Densité")
    plt.show()

    return mean, std


print("Bienvenue dans le cours d'analyse de données en géographie !\n")


def zipf_mandelbrot(size, s=2, v=1):
    ranks = np.arange(1, size + 1)
    probs = 1 / (ranks + v) ** s
    probs /= probs.sum()
    return np.random.choice(ranks, size=size, p=probs)


# Distributions discrètes
discrete_distributions = {
    "Dirac (tous égaux à 5)": (lambda size: np.full(size, 5), {}),
    "Uniforme discrète 1-10": (stats.randint, {"low": 1, "high": 11}),
    "Binomiale (n=10, p=0.5)": (stats.binom, {"n": 10, "p": 0.5}),
    "Poisson (mu=3)": (stats.poisson, {"mu": 3}),
    "Zipf-Mandelbrot (s=2, v=1)": (zipf_mandelbrot, {"s": 2, "v": 1}),
}

for name, (dist, params) in discrete_distributions.items():
    if callable(dist) and name.startswith("Dirac"):
        # Cas particulier de la Dirac
        data = dist(1000)
        mean = moyenne(data)
        std = ecart_type(data)

        plt.figure(figsize=(6, 4))
        plt.hist(
            data,
            bins=[4.5, 5.5],
            density=True,
            alpha=0.7,
            color='skyblue',
            edgecolor='black'
        )
        plt.title(f"{name}\nMoyenne = {mean:.2f}, Écart type = {std:.2f}")
        plt.xlabel("Valeurs")
        plt.ylabel("Densité")
        plt.show()
    else:
        mean, std = plot_distribution(dist, params=params, title=name)

    print(name, "=> Moyenne:", mean, ", Écart type:", std, "\n")


# Distributions continues
continuous_distributions = {
    "Poisson (μ=3) (approche continue)": (stats.poisson, {"mu": 3}),
    "Normale (loc=0, scale=1)": (stats.norm, {"loc": 0, "scale": 1}),
    "Log-Normale (s=0.5)": (stats.lognorm, {"s": 0.5}),
    "Uniforme continue 0-1": (stats.uniform, {"loc": 0, "scale": 1}),
    "Chi² (df=4)": (stats.chi2, {"df": 4}),
    "Pareto (b=2)": (stats.pareto, {"b": 2}),
}

for name, (dist, params) in continuous_distributions.items():
    mean, std = plot_distribution(dist, params=params, title=name)
    print(name, "=> Moyenne:", mean, ", Écart type:", std, "\n")
