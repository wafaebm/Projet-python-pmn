import numpy as np
import pandas as pd


class StatisticsCalculator:
    """
    Classe pour calculer des statistiques descriptives et simples statistiques
    "inférentielles" (corrélations) sur un DataFrame de ventes.

    L'utilisation de NumPy permet d'accélérer les opérations lourdes
    en contournant certaines surcharges de pandas.
    """

    def __init__(self, df: pd.DataFrame):
        # On stocke une copie pour ne pas modifier le df d'origine
        self.df = df.copy()

    def basic_stats(self) -> pd.DataFrame:
        """
        Calcule les principales statistiques descriptives
        (moyenne, médiane, écart-type, min, max) sur les colonnes numériques.
        """
        numeric_df = self.df.select_dtypes(include=[np.number])

        stats: dict[str, dict[str, float]] = {}

        for col in numeric_df.columns:
            array = numeric_df[col].to_numpy()

            stats[col] = {
                "mean": float(np.nanmean(array)),
                "median": float(np.nanmedian(array)),
                "std": float(np.nanstd(array)),
                "min": float(np.nanmin(array)),
                "max": float(np.nanmax(array)),
            }

        return pd.DataFrame(stats).T

    def correlation_matrix(self) -> pd.DataFrame:
        """
        Calcule la matrice de corrélation de Pearson entre colonnes numériques.
        """
        numeric_df = self.df.select_dtypes(include=[np.number])

        if numeric_df.shape[1] == 0:
            return pd.DataFrame()

        data_np = numeric_df.to_numpy()
        corr_np = np.corrcoef(data_np, rowvar=False)

        return pd.DataFrame(
            corr_np, index=numeric_df.columns, columns=numeric_df.columns
        )

    def revenue_quantity_correlation(self) -> float:
        """
        Corrélation entre le chiffre d'affaires (total) et la quantité vendue.
        """
        if "total" not in self.df.columns or "quantite" not in self.df.columns:
            return np.nan

        subset = self.df[["total", "quantite"]].dropna()
        if subset.empty:
            return np.nan

        corr_matrix = np.corrcoef(subset["total"], subset["quantite"])
        return float(corr_matrix[0, 1])
