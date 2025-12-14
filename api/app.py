import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import pandas as pd

from config import setup_logger, REPORT_DIR
from data_loader.csv_loader import CSVLoader
from data_loader.data_validator import DataValidator
from data_processor.cleaner import DataCleaner
from data_processor.aggregator import DataAggregator
from data_processor.statistics import StatisticsCalculator
from visualization.chart_builder import ChartBuilder
from visualization.report_generator import ReportGenerator

from .schemas import HealthResponse, LoadRequest, MessageResponse, PreviewResponse, StatsResponse, ReportResponse

app = FastAPI(title="Plateforme Analyse Ventes API", version="1.0.0")
logger = setup_logger("api")

# Stockage simple en mémoire
STATE = {
    "df_raw": None,
    "df_valid": None,
    "df_clean": None,
}


def run_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """Applique validate + clean et met à jour STATE."""
    try:
        validator = DataValidator(df)
        df_valid = validator.validate()

        cleaner = DataCleaner(df_valid)
        df_clean = cleaner.clean() if hasattr(cleaner, "clean") else cleaner.get()

        STATE["df_raw"] = df
        STATE["df_valid"] = df_valid
        STATE["df_clean"] = df_clean

        return df_clean
    except Exception as e:
        logger.exception("Pipeline failed")
        raise HTTPException(status_code=400, detail=str(e))


def require_df_clean() -> pd.DataFrame:
    df_clean = STATE.get("df_clean")
    if df_clean is None or df_clean.empty:
        raise HTTPException(status_code=400, detail="Aucune donnée chargée. Utilise /load ou /upload d'abord.")
    return df_clean


@app.get("/health", response_model=HealthResponse)
def health():
    return {"status": "ok"}


@app.post("/load", response_model=MessageResponse)
def load_csv(payload: LoadRequest):
    """Charge un CSV depuis un chemin local (serveur)."""
    csv_path = payload.csv_path
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail=f"Fichier introuvable: {csv_path}")

    try:
        df = CSVLoader(csv_path).load()
        run_pipeline(df)
        return {"message": f"CSV chargé et traité: {csv_path}"}
    except Exception as e:
        logger.exception("Load failed")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/upload", response_model=MessageResponse)
def upload_csv(file: UploadFile = File(...)):
    """Upload d'un CSV (cas SaaS classique)."""
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Le fichier doit être un .csv")

    tmp_dir = os.path.join(REPORT_DIR, "uploads")
    os.makedirs(tmp_dir, exist_ok=True)
    tmp_path = os.path.join(tmp_dir, file.filename)

    try:
        with open(tmp_path, "wb") as f:
            f.write(file.file.read())

        df = CSVLoader(tmp_path).load()
        run_pipeline(df)
        return {"message": f"Fichier uploadé, chargé et traité: {file.filename}"}
    except Exception as e:
        logger.exception("Upload failed")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/data/preview", response_model=PreviewResponse)
def preview(limit: int = 5):
    df_clean = require_df_clean()
    return {
        "rows": int(len(df_clean)),
        "columns": list(df_clean.columns),
        "preview": df_clean.head(limit).to_dict(orient="records"),
    }


@app.get("/sales/by-category")
def sales_by_category():
    df_clean = require_df_clean()
    agg = DataAggregator(df_clean)
    out = agg.ventes_par_categorie_et_source()
    return out.to_dict(orient="records")


@app.get("/sales/by-city")
def sales_by_city():
    df_clean = require_df_clean()
    agg = DataAggregator(df_clean)
    out = agg.chiffre_affaires_par_ville()
    return out.to_dict(orient="records")


@app.get("/sales/top-products")
def top_products(n: int = 10):
    df_clean = require_df_clean()
    agg = DataAggregator(df_clean)
    out = agg.top_produits_par_revenu(n=n)
    return out.to_dict(orient="records")


@app.get("/stats/basic", response_model=StatsResponse)
def basic_stats():
    df_clean = require_df_clean()
    stats = StatisticsCalculator(df_clean).basic_stats()
    return {"stats": stats.reset_index().rename(columns={"index": "column"}).to_dict(orient="records")}


@app.post("/report/pdf", response_model=ReportResponse)
def generate_pdf():
    df_clean = require_df_clean()

    charts_output = os.path.join(REPORT_DIR, "charts")
    os.makedirs(charts_output, exist_ok=True)

    # charts
    cb = ChartBuilder(df_clean)
    cb.plot_sales_by_category(save_path=os.path.join(charts_output, "ventes_par_categorie.png"))
    cb.plot_sales_by_city(save_path=os.path.join(charts_output, "ventes_par_ville.png"))
    cb.plot_top_products(n=10, save_path=os.path.join(charts_output, "top_produits.png"))

    # report
    report_file = os.path.join(REPORT_DIR, "rapport_ventes_api.pdf")
    report = ReportGenerator(df_clean, output_dir=REPORT_DIR)
    report.generate_pdf_report("rapport_ventes_api.pdf", charts_dir=charts_output)

    return {"pdf_path": report_file}


@app.get("/report/pdf/download")
def download_pdf():
    pdf_path = os.path.join(REPORT_DIR, "rapport_ventes_api.pdf")
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="Aucun PDF généré. Appelle /report/pdf d'abord.")
    return FileResponse(pdf_path, media_type="application/pdf", filename="rapport_ventes_api.pdf")
