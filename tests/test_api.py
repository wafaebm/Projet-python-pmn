import io
import pandas as pd
from fastapi.testclient import TestClient

from api.app import app


client = TestClient(app)


def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_upload_then_preview_then_stats():
    # CSV minimal en mémoire
    csv_content = """date,produit,categorie,prix,quantite,ville,source
2025-01-01,Stylo,Fournitures,1.5,10,Paris,web
2025-01-01,Cahier,Fournitures,3.0,5,Lyon,magasin
2025-01-02,Souris,Electronique,25.0,2,Paris,web
"""
    files = {"file": ("ventes_test.csv", csv_content, "text/csv")}
    r = client.post("/upload", files=files)
    assert r.status_code == 200

    # preview
    r = client.get("/data/preview?limit=2")
    assert r.status_code == 200
    data = r.json()
    assert data["rows"] >= 3
    assert "preview" in data
    assert len(data["preview"]) == 2

    # stats
    r = client.get("/stats/basic")
    assert r.status_code == 200
    stats = r.json()["stats"]
    assert isinstance(stats, list)
    assert len(stats) > 0
