import pandas as pd
import pytest

from data_loader.csv_loader import CSVLoader
from data_loader.data_validator import DataValidator


def test_csv_loader_load_ok(tmp_path):
    csv_path = tmp_path / "ventes.csv"
    csv_path.write_text(
        "date,produit,categorie,prix,quantite,ville,source\n"
        "2025-01-01,Stylo,Fournitures,1.5,10,Paris,web\n"
        "2025-01-01,Cahier,Fournitures,3.0,5,Lyon,magasin\n",
        encoding="utf-8",
    )

    df = CSVLoader(str(csv_path)).load()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ["date", "produit", "categorie", "prix", "quantite", "ville", "source"]


def test_csv_loader_missing_file_raises(tmp_path):
    missing = tmp_path / "missing.csv"
    with pytest.raises(Exception):
        CSVLoader(str(missing)).load()


def test_data_validator_drops_duplicates_and_fills_na():
    df = pd.DataFrame(
        [
            {"date": "2025-01-01", "produit": "Stylo", "categorie": "Fournitures", "prix": 1.5, "quantite": 10, "ville": "Paris", "source": "web"},
            {"date": "2025-01-01", "produit": "Stylo", "categorie": "Fournitures", "prix": 1.5, "quantite": 10, "ville": "Paris", "source": "web"},  # doublon
            {"date": "2025-01-02", "produit": "Souris", "categorie": "Electronique", "prix": 25.0, "quantite": None, "ville": "Paris", "source": "web"},  # NaN
        ]
    )

    out = DataValidator(df).validate()
    assert len(out) == 2  # doublon supprimé
    assert out["quantite"].isna().sum() == 0  # NaN rempli (ffill)
