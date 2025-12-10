import os
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from .chart_builder import ChartBuilder

class ReportGenerator:
    """
    Génère des rapports complets en PDF et HTML pour les ventes.
    Utilise ChartBuilder pour créer les graphiques.
    """

    def __init__(self, df: pd.DataFrame, output_dir: str = "reports"):
        self.df = df.copy()
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.chart_builder = ChartBuilder(self.df)
        # Calcul de colonne utile pour certains graphiques
        if "total_ventes" not in self.df.columns:
            self.df["total_ventes"] = self.df["prix"] * self.df["quantite"].fillna(0)

    # ---------------------- PDF ----------------------
    def generate_pdf_report(self, filename: str = "rapport_ventes.pdf"):
        pdf_path = os.path.join(self.output_dir, filename)
        c = canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4

        # Titre
        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, height - 50, "Rapport de Ventes 2025")

        # Ajouter un graphique histogramme
        hist_path = os.path.join(self.output_dir, "hist_quantite.png")
        self.chart_builder.plot_histogram("quantite", save_path=hist_path)
        c.drawImage(ImageReader(hist_path), 50, height - 350, width=500, height=250)

        # Ajouter un graphique bar chart (total ventes par catégorie)
        bar_path = os.path.join(self.output_dir, "bar_categorie.png")
        agg_df = self.df.groupby("categorie")["total_ventes"].sum().reset_index()
        self.chart_builder.df = agg_df  # temporaire pour le plot
        self.chart_builder.plot_bar("categorie", "total_ventes", save_path=bar_path)
        c.drawImage(ImageReader(bar_path), 50, height - 650, width=500, height=250)

        c.save()
        print(f"[INFO] PDF généré : {pdf_path}")

    # ---------------------- HTML ----------------------
    def generate_html_report(self, filename: str = "rapport_ventes.html"):
        html_path = os.path.join(self.output_dir, filename)
        html_content = "<html><head><title>Rapport Ventes</title></head><body>"
        html_content += "<h1>Rapport de Ventes 2025</h1>"

        # Ajouter histogramme
        hist_path = os.path.join(self.output_dir, "hist_quantite.png")
        self.chart_builder.plot_histogram("quantite", save_path=hist_path)
        html_content += f'<h2>Histogramme Quantité</h2><img src="{hist_path}" width="600">'

        # Ajouter bar chart
        bar_path = os.path.join(self.output_dir, "bar_categorie.png")
        agg_df = self.df.groupby("categorie")["total_ventes"].sum().reset_index()
        self.chart_builder.df = agg_df
        self.chart_builder.plot_bar("categorie", "total_ventes", save_path=bar_path)
        html_content += f'<h2>Total ventes par catégorie</h2><img src="{bar_path}" width="600">'

        html_content += "</body></html>"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"[INFO] HTML généré : {html_path}")
