import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from typing import Optional


class ChartBuilder:
    """
    Classe pour générer différents types de graphiques.
    Utilisation : donner un DataFrame pandas et les colonnes à visualiser.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    # ---------------------- Matplotlib ----------------------
    def plot_histogram(self, column: str, bins: int = 10, save_path: Optional[str] = None):
        """
        Génère un histogramme d'une colonne numérique.
        """
        plt.figure(figsize=(8, 5))
        plt.hist(self.df[column].dropna(), bins=bins, color='skyblue', edgecolor='black')
        plt.title(f'Histogramme de {column}')
        plt.xlabel(column)
        plt.ylabel('Fréquence')
        plt.grid(True)
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        plt.show()

    def plot_bar(self, x_col: str, y_col: str, save_path: Optional[str] = None):
        """
        Génère un graphique en barres.
        """
        plt.figure(figsize=(8, 5))
        plt.bar(self.df[x_col], self.df[y_col], color='orange', edgecolor='black')
        plt.title(f'{y_col} par {x_col}')
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        plt.show()

    def plot_pie(self, column: str, save_path: Optional[str] = None):
        """
        Génère un camembert pour une colonne catégorielle.
        """
        counts = self.df[column].value_counts()
        plt.figure(figsize=(6, 6))
        plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.tab20.colors)
        plt.title(f'Repartition de {column}')
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        plt.show()

    # ---------------------- Plotly pour interactivité ----------------------
    def interactive_line(self, x_col: str, y_col: str):
        """
        Génère un graphique interactif de type ligne avec Plotly.
        """
        fig = px.line(self.df, x=x_col, y=y_col, title=f'{y_col} par {x_col}')
        fig.show()

    def interactive_bar(self, x_col: str, y_col: str):
        """
        Génère un graphique interactif de type barres avec Plotly.
        """
        fig = px.bar(self.df, x=x_col, y=y_col, title=f'{y_col} par {x_col}')
        fig.show()
