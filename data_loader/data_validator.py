import pandas as pd

class DataValidator:
    """
    Validates a DataFrame:
    - Checks for missing values
    - Checks for duplicate rows
    - Optionally enforces column types
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def validate(self, expected_types: dict = None) -> pd.DataFrame:
        """
        Validate the DataFrame.

        Parameters:
        - expected_types: dict of {column_name: type}, optional

        Returns:
        - Cleaned DataFrame
        """
        # Drop duplicate rows
        self.df.drop_duplicates(inplace=True)

        # Fill missing values with defaults
        self.df.fillna(method='ffill', inplace=True)

        # Enforce types if specified
        if expected_types:
            for col, dtype in expected_types.items():
                if col in self.df.columns:
                    self.df[col] = self.df[col].astype(dtype)

        return self.df 