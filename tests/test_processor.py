import pandas as pd
import pytest

from data_processor.aggregator import DataAggregator
from data_processor.statistics import StatisticsCalculator
from data_processor.cleaner import DataCleaner


def _df():
    return pd.DataFrame(
        [
            {"date": "2025-01-01", "produit": "Stylo", "categorie": "Fournitures", "prix": 1.5, "quantite": 10, "ville": "Paris", "source": "web"},
            {"date": "2025-01-01", "produit": "Cahier", "categorie": "Fournitures", "prix": 3.0, "quantite": 5, "ville": "Lyon", "source": "magasin"},
            {"date": "2025-01-02", "produit": "Souris", "categorie": "Electronique", "prix": 25.0, "quantite": 2, "ville": "Paris", "source": "web"},
        ]
    )


def test_cleaner_runs():
    df = _df()
    cleaner = DataCleaner(df)
    out = cleaner.clean() if hasattr(cleaner, "clean") else cleaner.get()
    assert isinstance(out, pd.DataFrame)
    assert len(out) == len(df)


def test_aggregator_returns_outputs():
    df = _df()
    agg = DataAggregator(df)
    assert not agg.ventes_par_categorie_et_source().empty
    assert not agg.chiffre_affaires_par_ville().empty
    assert len(agg.top_produits_par_revenu(n=2)) <= 2


def test_statistics_basic_stats():
    df = _df()
    stats = StatisticsCalculator(df).basic_stats()
    assert isinstance(stats, pd.DataFrame)
    for col in ["mean", "median", "std", "min", "max"]:
        assert col in stats.columns
