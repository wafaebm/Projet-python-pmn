import pandas as pd


class CSVLoader:
    """
    The CSV Loader take a CSV file and returns a pandas DataFrame
    """

    def __init__(self, filepath: str, separator: str = ","):
        self.filepath = filepath
        self.separator = separator

    def load(self) -> pd.DataFrame:
        """
        Loads a CSV file using pandas.
        Raises LoaderError if loading fails.
        """
        return pd.read_csv(self.filepath, sep=self.separator)