import os
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from .chart_builder import ChartBuilder
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


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



    def generate_pdf_report(self, filename: str = "rapport_ventes.pdf", charts_dir: str = None):
        pdf_path = os.path.join(self.output_dir, filename)
        c = canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4

        if charts_dir is None:
            charts_dir = os.path.join(self.output_dir, "charts")

        charts = [
            ("Ventes par catégorie", os.path.join(charts_dir, "ventes_par_categorie.png")),
            ("Ventes par ville", os.path.join(charts_dir, "ventes_par_ville.png")),
            ("Top produits", os.path.join(charts_dir, "top_produits.png")),
         ]

        def header(title: str):
            c.setFont("Helvetica-Bold", 18)
            c.drawString(50, height - 50, "Rapport de Ventes 2025")
            c.setFont("Helvetica-Bold", 13)
            c.drawString(50, height - 80, title)

        for title, img_path in charts:
            if not os.path.exists(img_path):
                continue

            header(title)

        # Zone image (marges)
            left = 50
            bottom = 90
            available_w = width - 2 * left
            available_h = height - 140  # laisse de l'air pour titres + bas de page

            img = ImageReader(img_path)
            iw, ih = img.getSize()

        # conserve le ratio
            scale = min(available_w / iw, available_h / ih)
            draw_w = iw * scale
            draw_h = ih * scale

            x = left + (available_w - draw_w) / 2
            y = bottom + (available_h - draw_h) / 2

            c.drawImage(img, x, y, width=draw_w, height=draw_h, preserveAspectRatio=True, mask='auto')

        # numéro de page (optionnel)
            c.setFont("Helvetica", 9)
            c.drawRightString(width - 50, 30, f"Page {c.getPageNumber()}")

            c.showPage()

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
