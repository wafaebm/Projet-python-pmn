import pandas as pd
import numpy as np

class DataCleaner:
    """
    Applies cleaning operations on a DataFrame:
    
keeps selected columns
renames columns
applies custom transformations
"""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def select_columns(self, columns: list) -> "DataCleaner":
        """Keep only the specified columns."""
        self.df = self.df[columns]
        return self

    def rename_columns(self, mapping: dict) -> "DataCleaner":
        """Rename columns using a dictionary {old: new}."""
        self.df.rename(columns=mapping, inplace=True)
        return self

    def apply_transform(self, column: str, func) -> "DataCleaner":
        """Apply a custom function to a column."""
        self.df[column] = self.df[column].apply(func)
        return self
    
    def remove_outliers_zscore(self, column, threshold=3):
        """Detect and  delete extreme values(outliers) in column with Z-score = (x - mean) / standard deviation
    A value is considered as outlier if |Z| > threshold."""
        data = self.df[column].to_numpy()
        z = np.abs((data - data.mean()) / data.std())
        mask = z < threshold
        self.df = self.df[mask]
        return self.df
        
    def clean(self) -> pd.DataFrame:
        """
        Default cleaning for the sales dataset.

        - Keep the columns from ventes_2025.csv
        (date, produit, categorie, prix, quantite, ville, source)
        """
        columns = ["date", "produit", "categorie", "prix", "quantite", "ville", "source"]
        # si une colonne manque, ça lèvera une KeyError -> c'est normal
        self.df = self.df[columns]
        return self.df
    
    def get(self) -> pd.DataFrame:
        """Return the cleaned DataFrame."""
        return self.df