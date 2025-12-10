import numpy as np
import pandas as pd


class StatisticsCalculator:
    """
    Classe regroupant des méthodes pour calculer diverses statistiques
    sur un DataFrame pandas.
    L'utilisation de NumPy permet d'accélérer les opérations lourdes
    en contournant certaines limites de performance de pandas.
    """

    def basic_stats(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule les principales statistiques descriptives
        (moyenne, médiane, écart-type, min, max).

        Optimisation performance :
        - Conversion préalable en NumPy array pour effectuer les calculs
          → évite l'overhead de pandas
        - np.nanmean, np.nanstd, np.nanmedian sont bien plus rapides
          sur de gros volumes
        """
        numeric_df = df.select_dtypes(include=[np.number])

        stats = {}

        for col in numeric_df.columns:
            array = numeric_df[col].to_numpy()

            stats[col] = {
                "mean": np.nanmean(array),         # Calcul vectorisé NumPy
                "median": np.nanmedian(array),     # Plus rapide que pandas median()
                "std": np.nanstd(array),           # Ecart-type NumPy optimisé
                "min": np.nanmin(array),
                "max": np.nanmax(array)
            }

        return pd.DataFrame(stats).T

    def correlation_matrix(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule la matrice de corrélation.

        Optimisation performance :
        - pandas utilise déjà NumPy sous le capot, mais on
          convertit explicitement en array pour minimiser les copies
        """
        numeric_df = df.select_dtypes(include=[np.number])

        # Conversion pour optimisation (pandas corr peut être lent)
        data_np = numeric_df.to_numpy()

        corr = np.corr