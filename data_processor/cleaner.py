import pandas as pd

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

    def get(self) -> pd.DataFrame:
        """Return the cleaned DataFrame."""
        return self.df