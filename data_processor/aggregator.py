import pandas as pd

class DataAggregator:
    """
    Performs complex aggregations on ventes_2025.csv data.
    Columns available:
        - date
        - produit
        - categorie
        - prix
        - quantite
        - ville
        - source
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    # --------------------------------------------------------------
    # 1) AGRÉGATIONS MULTIPLES (groupby)
    # --------------------------------------------------------------
    def groupby_multiple(self, group_cols: list, agg_dict: dict) -> pd.DataFrame:
        """
        General multi-column groupby with multiple aggregations.

        Example:
            aggregator.groupby_multiple(
                ["ville", "categorie"],
                {"prix": ["mean"], "quantite": ["sum", "mean"]}
            )
        """
        return self.df.groupby(group_cols).agg(agg_dict).reset_index()

    # --------------------------------------------------------------
    # 2) TABLEAUX CROISÉS (PIVOT TABLES)
    # --------------------------------------------------------------
    def pivot_quantite(self, index: str, columns: str, aggfunc: str = "sum") -> pd.DataFrame:
        """
        Pivot table for quantite.
        Example:
            aggregator.pivot_quantite("ville", "categorie")
        """
        return pd.pivot_table(
            self.df,
            index=index,
            columns=columns,
            values="quantite",
            aggfunc=aggfunc
        )

    def pivot_chiffre_affaires(self, index: str, columns: str, aggfunc: str = "sum") -> pd.DataFrame:
        """
        Pivot table for revenue = prix × quantite.
        """
        df = self.df.copy()
        df["revenu"] = df["prix"] * df["quantite"]
        return pd.pivot_table(
            df,
            index=index,
            columns=columns,
            values="revenu",
            aggfunc=aggfunc
        )

    # --------------------------------------------------------------
    # 3) AGRÉGATIONS SPÉCIFIQUES AU PROJET
    # --------------------------------------------------------------
    def total_quantite_par_produit(self) -> pd.DataFrame:
        """
        Total sold quantity by product.
        """
        return (
            self.df.groupby("produit")["quantite"]
            .sum()
            .reset_index()
            .sort_values("quantite", ascending=False)
        )

    def chiffre_affaires_par_ville(self) -> pd.DataFrame:
        """
        Sum of revenue per city.
        """
        df = self.df.copy()
        df["revenu"] = df["prix"] * df["quantite"]
        return df.groupby("ville")["revenu"].sum().reset_index()

    def ventes_par_categorie_et_source(self) -> pd.DataFrame:
        """
        Quantity sold by category and sales channel (web/magasin).
        """
        return (
            self.df.groupby(["categorie", "source"])["quantite"]
            .sum()
            .reset_index()
        )

    # --------------------------------------------------------------
    # 4) MÉTRIQUES AVANCÉES
    # --------------------------------------------------------------
    def detecter_doublons(self) -> pd.DataFrame:
        """
        Detect duplicated rows (common in the CSV example).
        """
        return self.df[self.df.duplicated()]

    def taux_valeurs_manquantes(self) -> pd.DataFrame:
        """
        Percentage of missing values per column.
        """
        return (self.df.isna().mean() * 100).reset_index(name="taux_manquant (%)")

    def top_produits_par_revenu(self, n: int = 5) -> pd.DataFrame:
        """
        Find the N highest-revenue products.
        """
        df = self.df.copy()
        df["revenu"] = df["prix"] * df["quantite"]
        return (
            df.groupby("produit")["revenu"]
            .sum()
            .reset_index()
            .sort_values("revenu", ascending=False)
            .head(n)
        )
