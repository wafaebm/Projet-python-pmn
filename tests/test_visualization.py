import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from visualization.chart_builder import ChartBuilder
from visualization.report_generator import ReportGenerator


def _make_df():
    return pd.DataFrame(
        [
            {"date": "2025-01-01", "produit": "Stylo", "categorie": "Fournitures", "prix": 1.5, "quantite": 10, "ville": "Paris", "source": "web"},
            {"date": "2025-01-01", "produit": "Cahier", "categorie": "Fournitures", "prix": 3.0, "quantite": 5, "ville": "Lyon", "source": "magasin"},
            {"date": "2025-01-02", "produit": "Souris", "categorie": "Electronique", "prix": 25.0, "quantite": 2, "ville": "Paris", "source": "web"},
        ]
    )


def _make_dummy_png(path: str):
    """Crée une vraie image PNG (petit plot) pour que ReportLab/PIL puisse la lire."""
    plt.figure()
    plt.plot([1, 2], [1, 2])
    plt.savefig(path, bbox_inches="tight")
    plt.close()


def test_chart_builder_saves_png(tmp_path, monkeypatch):
    monkeypatch.setattr(plt, "show", lambda: None)

    df = _make_df()
    cb = ChartBuilder(df)

    out = tmp_path / "histo.png"
    cb.plot_histogram("prix", save_path=str(out))
    assert out.exists()


def test_report_generator_creates_pdf(tmp_path):
    df = _make_df()

    charts_dir = tmp_path / "charts"
    charts_dir.mkdir()

    # ✅ Créer de vraies images PNG lisibles
    _make_dummy_png(str(charts_dir / "ventes_par_categorie.png"))
    _make_dummy_png(str(charts_dir / "ventes_par_ville.png"))
    _make_dummy_png(str(charts_dir / "top_produits.png"))

    report = ReportGenerator(df, output_dir=str(tmp_path))
    report.generate_pdf_report("rapport_test.pdf", charts_dir=str(charts_dir))

    pdf = tmp_path / "rapport_test.pdf"
    assert pdf.exists()
    assert pdf.stat().st_size > 0
