from config import setup_logger, CSV_FILE, REPORT_DIR
from data_loader.csv_loader import CSVLoader
from data_loader.data_validator import DataValidator 
from data_processor.cleaner import DataCleaner
from data_processor.aggregator import DataAggregator
from data_processor.statistics import StatisticsCalculator
from visualization.chart_builder import ChartBuilder
from visualization.report_generator import ReportGenerator

import os


def main():
    logger = setup_logger("main")
    logger.info("=== DÉMARRAGE DU PIPELINE D'ANALYSE ===")

    # 1) Chargement des données
    logger.info("Chargement du fichier CSV...")
    loader = CSVLoader(CSV_FILE)
    df_raw = loader.load()
    logger.info("df_raw: %d lignes", len(df_raw))
    logger.info("Aperçu df_raw:\n%s", df_raw.head())

    # 2) Validation des données
    logger.info("Validation des données...")
    validator = DataValidator(df_raw)
    df_valid = validator.validate()
    logger.info("df_valid: %d lignes", len(df_valid))
    logger.info("Aperçu df_valid:\n%s", df_valid.head())

    # 3) Nettoyage des données
    logger.info("Nettoyage des données...")
    cleaner = DataCleaner(df_valid)
    df_clean = cleaner.clean()
    logger.info("df_clean: %d lignes", len(df_clean))
    logger.info("Aperçu df_clean:\n%s", df_clean.head())
    logger.info("Colonnes df_clean : %s", list(df_clean.columns))

    # 4) Agrégations
    logger.info("Agrégation des données...")
    aggregator = DataAggregator(df_clean)

    ventes_par_categorie = aggregator.ventes_par_categorie_et_source()
    ventes_par_ville = aggregator.chiffre_affaires_par_ville()
    top_produits = aggregator.top_produits_par_revenu(n=10)

    # 5) Statistiques
    logger.info("Calcul des statistiques...")
    stats = StatisticsCalculator(df_clean)
    stats_resume = stats.basic_stats()

    # 6) Visualisation
    logger.info("Génération des graphiques...")
    charts_output = os.path.join(REPORT_DIR, "charts")
    os.makedirs(charts_output, exist_ok=True)

    chart_builder = ChartBuilder(df_clean)
    chart_builder.plot_sales_by_category(
        save_path=os.path.join(charts_output, "ventes_par_categorie.png")
    )
    chart_builder.plot_sales_by_city(
        save_path=os.path.join(charts_output, "ventes_par_ville.png")
    )
    chart_builder.plot_top_products(
        n=10, save_path=os.path.join(charts_output, "top_produits.png")
    )

    # 7) Génération du rapport
    logger.info("Génération du rapport PDF...")

    report = ReportGenerator(df_clean, output_dir=REPORT_DIR)
    report.generate_pdf_report("rapport_ventes.pdf", charts_dir=charts_output)

    logger.info("=== PIPELINE TERMINÉ AVEC SUCCÈS ===")
    logger.info("Rapport disponible ici : %s", os.path.join(REPORT_DIR, "rapport_ventes.pdf"))


if __name__ == "__main__":
    main()
