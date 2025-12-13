import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from typing import Optional


class ChartBuilder:
    """
    Classe pour générer différents types de graphiques à partir
    des données de ventes.

    df est supposé contenir au minimum :
    - date, produit, categorie, prix, quantite, ville, source
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

        # Si la colonne total n'existe pas, on la calcule (CA = prix * quantite)
        if "total" not in self.df.columns and {"prix", "quantite"}.issubset(self.df.columns):
            self.df["total"] = self.df["prix"] * self.df["quantite"]

    #  Matplotlib  

    def plot_histogram(self, column: str, bins: int = 10, save_path: Optional[str] = None):
        """Génère un histogramme d'une colonne numérique."""
        plt.figure(figsize=(8, 5))
        plt.hist(self.df[column].dropna(), bins=bins, edgecolor="black")
        plt.title(f"Histogramme de {column}")
        plt.xlabel(column)
        plt.ylabel("Fréquence")
        plt.grid(True)
        if save_path:
            plt.savefig(save_path, bbox_inches="tight")
        plt.show()

    def plot_bar(self, x_col: str, y_col: str, save_path: Optional[str] = None):
        """Génère un graphique en barres simple."""
        plt.figure(figsize=(8, 5))
        plt.bar(self.df[x_col], self.df[y_col], edgecolor="black")
        plt.title(f"{y_col} par {x_col}")
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.xticks(rotation=45)
        plt.grid(axis="y")
        if save_path:
            plt.savefig(save_path, bbox_inches="tight")
        plt.show()

    def plot_pie(self, column: str, save_path: Optional[str] = None):
        """Génère un camembert pour une colonne catégorielle."""
        counts = self.df[column].value_counts()
        plt.figure(figsize=(6, 6))
        plt.pie(
            counts,
            labels=counts.index,
            autopct="%1.1f%%",
            startangle=90,
        )
        plt.title(f"Répartition de {column}")
        if save_path:
            plt.savefig(save_path, bbox_inches="tight")
        plt.show()

    #  Matplotlib  (ventes) 

    def plot_sales_by_category(self, save_path: Optional[str] = None):
        """
        Graphique en barres : chiffre d'affaires par catégorie.
        """
        if "categorie" not in self.df.columns or "total" not in self.df.columns:
            raise ValueError("Colonnes 'categorie' ou 'total' manquantes pour plot_sales_by_category().")

        grouped = (
            self.df.groupby("categorie", as_index=False)
            .agg(total_revenue=("total", "sum"))
            .sort_values("total_revenue", ascending=False)
        )

        plt.figure(figsize=(8, 5))
        plt.bar(grouped["categorie"], grouped["total_revenue"], edgecolor="black")
        plt.title("Chiffre d'affaires par catégorie")
        plt.xlabel("Catégorie")
        plt.ylabel("Chiffre d'affaires")
        plt.xticks(rotation=45)
        plt.grid(axis="y")

        if save_path:
            plt.savefig(save_path, bbox_inches="tight")
        plt.show()

    def plot_sales_by_city(self, save_path: Optional[str] = None):
        """
        Graphique en barres : chiffre d'affaires par ville.
        """
        if "ville" not in self.df.columns or "total" not in self.df.columns:
            raise ValueError("Colonnes 'ville' ou 'total' manquantes pour plot_sales_by_city().")

        grouped = (
            self.df.groupby("ville", as_index=False)
            .agg(total_revenue=("total", "sum"))
            .sort_values("total_revenue", ascending=False)
        )

        plt.figure(figsize=(8, 5))
        plt.bar(grouped["ville"], grouped["total_revenue"], edgecolor="black")
        plt.title("Chiffre d'affaires par ville")
        plt.xlabel("Ville")
        plt.ylabel("Chiffre d'affaires")
        plt.xticks(rotation=45)
        plt.grid(axis="y")

        if save_path:
            plt.savefig(save_path, bbox_inches="tight")
        plt.show()

    def plot_top_products(self, n: int = 10, save_path: Optional[str] = None):
        """
        Graphique en barres : top N produits par chiffre d'affaires.
        """
        if "produit" not in self.df.columns or "total" not in self.df.columns:
            raise ValueError("Colonnes 'produit' ou 'total' manquantes pour plot_top_products().")

        grouped = (
            self.df.groupby("produit", as_index=False)
            .agg(total_revenue=("total", "sum"))
            .sort_values("total_revenue", ascending=False)
            .head(n)
        )

        plt.figure(figsize=(10, 5))
        plt.bar(grouped["produit"], grouped["total_revenue"], edgecolor="black")
        plt.title(f"Top {n} produits par chiffre d'affaires")
        plt.xlabel("Produit")
        plt.ylabel("Chiffre d'affaires")
        plt.xticks(rotation=45, ha="right")
        plt.grid(axis="y")

        if save_path:
            plt.savefig(save_path, bbox_inches="tight")
        plt.show()

    #  Plotly pour interactivité 

    def interactive_line(self, x_col: str, y_col: str):
        """Graphique interactif de type ligne avec Plotly."""
        fig = px.line(self.df, x=x_col, y=y_col, title=f"{y_col} par {x_col}")
        fig.show()

    def interactive_bar(self, x_col: str, y_col: str):
        """Graphique interactif de type barres avec Plotly."""
        fig = px.bar(self.df, x=x_col, y=y_col, title=f"{y_col} par {x_col}")
        fig.show()
