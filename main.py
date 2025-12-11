from config import setup_logger, CSV_FILE, REPORT_DIR
from data_loader.csv_loader import CSVLoader
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
    df = loader.load()

    # 2) Nettoyage des données
    logger.info("Nettoyage des données...")
    cleaner = DataCleaner(df)
    df_clean = cleaner.clean()

    # 3) Agrégations
    logger.info("Agrégation des données...")
    aggregator = DataAggregator(df_clean)

    ventes_par_categorie = aggregator.total_sales_by_category()
    ventes_par_ville = aggregator.total_sales_by_city()
    top_produits = aggregator.top_products(n=10)

    # 4) Statistiques
    logger.info("Calcul des statistiques...")
    stats = StatisticsCalculator(df_clean)
    stats_resume = stats.basic_stats()

    # 5) Visualisation
    logger.info("Génération des graphiques...")
    charts_output = os.path.join(REPORT_DIR, "charts")
    os.makedirs(charts_output, exist_ok=True)

    chart_builder = ChartBuilder(df_clean)
    chart_builder.plot_sales_by_category(save_path=os.path.join(charts_output, "ventes_par_categorie.png"))
    chart_builder.plot_sales_by_city(save_path=os.path.join(charts_output, "ventes_par_ville.png"))
    chart_builder.plot_top_products(n=10, save_path=os.path.join(charts_output, "top_produits.png"))

    # 6) Génération du rapport
    logger.info("Génération du rapport PDF...")
    report_file = os.path.join(REPORT_DIR, "rapport_ventes.pdf")
    report = ReportGenerator()

    report.generate(
        output_path=report_file,
        summary_stats=stats_resume,
        category_sales=ventes_par_categorie,
        city_sales=ventes_par_ville,
        top_products=top_produits,
        charts_dir=charts_output
    )

    logger.info("=== PIPELINE TERMINÉ AVEC SUCCÈS ===")
    logger.info(f"Rapport disponible ici : {report_file}")


if __name__ == "__main__":
    main()
