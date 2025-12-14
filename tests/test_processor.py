import pandas as pd

from data_processor.aggregator import DataAggregator
from data_processor.statistics import StatisticsCalculator


def _make_df():
    # dataset minimal mais suffisant pour tester groupby / stats
    return pd.DataFrame(
        [
            {"date": "2025-01-01", "produit": "Stylo", "categorie": "Fournitures", "prix": 1.5, "quantite": 10, "ville": "Paris", "source": "web"},
            {"date": "2025-01-01", "produit": "Cahier", "categorie": "Fournitures", "prix": 3.0, "quantite": 5, "ville": "Lyon", "source": "magasin"},
            {"date": "2025-01-02", "produit": "Souris", "categorie": "Electronique", "prix": 25.0, "quantite": 2, "ville": "Paris", "source": "web"},
            {"date": "2025-01-02", "produit": "Souris", "categorie": "Electronique", "prix": 25.0, "quantite": 1, "ville": "Lyon", "source": "magasin"},
        ]
    )


def test_aggregator_ventes_par_categorie_et_source():
    df = _make_df()
    agg = DataAggregator(df)
    out = agg.ventes_par_categorie_et_source()

    # Vérifs de structure
    assert isinstance(out, pd.DataFrame)
    assert "categorie" in out.columns
    assert "source" in out.columns

    
    # On détecte la colonne numérique de montant
    numeric_cols = [c for c in out.columns if c not in ("categorie", "source")]
    assert len(numeric_cols) >= 1

    # Fournitures/web : 1.5*10 = 15
    # Fournitures/magasin : 3*5 = 15
    # Electronique/web : 25*2 = 50
    # Electronique/magasin : 25*1 = 25
    # On vérifie au moins que les catégories existent
    assert set(out["categorie"].unique()) == {"Fournitures", "Electronique"}


def test_aggregator_chiffre_affaires_par_ville():
    df = _make_df()
    agg = DataAggregator(df)
    out = agg.chiffre_affaires_par_ville()

    assert isinstance(out, pd.DataFrame)
    assert "ville" in out.columns

    # Paris total attendu: (1.5*10) + (25*2) = 15 + 50 = 65
    # Lyon total attendu: (3*5) + (25*1) = 15 + 25 = 40
    # On cherche la colonne CA (col num différente selon ton code)
    ca_col = [c for c in out.columns if c != "ville"][0]

    paris = out.loc[out["ville"] == "Paris", ca_col].iloc[0]
    lyon = out.loc[out["ville"] == "Lyon", ca_col].iloc[0]

    assert float(paris) == 65.0
    assert float(lyon) == 40.0


def test_aggregator_top_produits_par_revenu():
    df = _make_df()
    agg = DataAggregator(df)
    out = agg.top_produits_par_revenu(n=2)

    assert isinstance(out, pd.DataFrame)
    assert "produit" in out.columns
    assert len(out) == 2

    
    assert out["produit"].iloc[0] == "Souris"


def test_statistics_basic_stats_returns_expected_columns():
    df = _make_df()

    stats = StatisticsCalculator(df).basic_stats()
    assert isinstance(stats, pd.DataFrame)

    # Stats attendues 
    for col in ["mean", "median", "std", "min", "max"]:
        assert col in stats.columns

    # Doit inclure au moins prix et quantite
    assert "prix" in stats.index
    assert "quantite" in stats.index
