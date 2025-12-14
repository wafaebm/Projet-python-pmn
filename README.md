# Plateforme d’Analyse de Données – Python Avancé 

## Contexte
Création d’une plateforme SaaS d’analyse des ventes capable de récupérer des fichiers CSV de plusieurs sources, de traiter beaucoup de données de façon fiable, et de rester facile à faire évoluer et à maintenir. 
La plateforme doit proposer une API pour consulter les données et les analyses, ainsi que des tableaux de bord avec des graphiques. Elle doit aussi bien gérer les erreurs, être performante, et être bien testée et documentée pour une équipe de développeurs.

## Objectifs 

Le pipeline permet de :
- Charger des données depuis des fichiers CSV
- Valider et nettoyer les données (doublons, valeurs manquantes, types)
- Réaliser des agrégations et calculs statistiques
- Générer des visualisations (PNG) et un rapport PDF
- Tracer l’exécution via un logging professionnel

---

## Architecture (couches)

```
projet_analyse/
├── data_loader/          # Couche d'entree des donnees
│   ├── __init__.py
│   ├── csv_loader.py
│   └── data_validator.py
├── data_processor/       # Couche de traitement des donnees
│   ├── __init__.py
│   ├── cleaner.py
│   ├── aggregator.py
│   └── statistics.py
├── visualization/        # Couche de visualisation
│   ├── __init__.py
│   ├── chart_builder.py
│   └── report_generator.py
├── tests/                # Tests unitaires
│   ├── __init__.py
│   ├── test_loader.py
│   ├── test_processor.py
│   └── test_visualization.py
├── main.py               # Point d'entree principal
├── config.py             # Configuration centralisee
├── requirements.txt      # Dependencies
└── README.md             # Documentation
```
---

## Installation

### Cloner le projet

#### Executer le projet 
git clone https://github.com/wafaebm/Projet-python-pmn
cd Projet-python-pmn

#### Creer et activer un environement virtuel
python -m venv venv
venv\Scripts\activate

#### Installer les dépendances
pip install -r requirements.txt

#### Exécuter le pipeline complet
python main.py

### Lancer les tests
python -m pytest -q

### Lancer la couverture
python -m pytest --cov=. --cov-report=term-missing

### Patterns + architecture (mission demande “patterns utilisés”)

- **Architecture en couches (SoC)** : séparation claire des responsabilités (loader / processor / visualization).
- **Programmation orientée objet** : classes par responsabilité (CSVLoader, DataValidator, DataCleaner, etc.).
- **Principes SOLID / DRY** : modules courts, responsabilités uniques, code maintenable.
- **Optimisation performance** : opérations vectorisées pandas/NumPy (éviter les boucles inutiles).
- **Logging** : traçabilité et debug en contexte production.


## Guide de contribution

1. Respecter la structure du projet (couches).
2. Ajouter des **docstrings** à toute classe/méthode publique.
3. Ajouter des tests si une fonctionnalité change.
4. Exécuter avant commit :
   python -m pytest -q


### Exemples d’utilisation

## Charger un CSV
```python
from data_loader.csv_loader import CSVLoader

df = CSVLoader("data/ventes_2025.csv").load()
print(df.head())

### Valider les données :
from data_loader.data_validator import DataValidator

df_valid = DataValidator(df).validate()

### Nettoyer les données :
from data_processor.cleaner import DataCleaner

cleaner = DataCleaner(df_valid)
df_clean = cleaner.clean()  

### Agréger les données
from data_processor.aggregator import DataAggregator

agg = DataAggregator(df_clean)
print(agg.chiffre_affaires_par_ville().head())

### Calcul des statistiques
from data_processor.statistics import StatisticsCalculator

stats = StatisticsCalculator(df_clean).basic_stats()
print(stats)

### Génération des graphiques
from visualization.chart_builder import ChartBuilder

cb = ChartBuilder(df_clean)
cb.plot_histogram("prix", save_path="reports/charts/histo_prix.png")

### Générer le rapport PDF
from visualization.report_generator import ReportGenerator

report = ReportGenerator(df_clean, output_dir="reports")
report.generate_pdf_report("rapport_ventes.pdf", charts_dir="reports/charts")
```

### Docstrings

Toutes les classes et méthodes publiques du projet sont documentées
directement dans les fichiers `.py`.

 **Où ?** Directement dans les fichiers `.py` (dans `data_loader`, `data_processor`, `visualization`)


### Exemple à appliquer 
Dans `data_loader/csv_loader.py` :

```python
class CSVLoader:
    """
    Charge un fichier CSV et retourne un DataFrame pandas.

    Responsabilité :
    - Lire les données depuis un fichier CSV
    - Gérer les erreurs de lecture (fichier introuvable, format invalide, etc.)

    Parameters
    ----------
    filepath : str
        Chemin vers le fichier CSV.
    separator : str
        Séparateur utilisé dans le fichier (par défaut '

```
Dans une méthode : 

```python
def load(self) -> pd.DataFrame:
    """
    Charge le fichier CSV et retourne un DataFrame.

    Returns
    -------
    pd.DataFrame
        Données chargées depuis le CSV.

    Raises
    ------
    Exception
        Si le fichier n'existe pas ou si la lecture échoue.
    """
```

### API REST (FastAPI)

## Lancer l'API
uvicorn api.app:app --reload

## Documentation interactive

FastAPI génère automatiquement une documentation interactive de l’API (Swagger UI).
Une fois l’API lancée, ouvrir dans le navigateur :
/docs → interface Swagger (tests des endpoints)
/openapi.json → spécification OpenAPI

## Tests de l’API

Les endpoints ont été validés manuellement via la documentation interactive FastAPI.
Des tests automatisés peuvent être ajoutés avec fastapi.testclient pour les scénarios critiques (upload CSV, génération PDF).
