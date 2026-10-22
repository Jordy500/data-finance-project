import os
from pathlib import Path

from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()

PROJECT_ID = os.environ["GCP_PROJECT_ID"]
TABLE = f"{PROJECT_ID}.analytics.fct_credit_mensuel"
OUT_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "fct_credit_mensuel.csv"

if __name__ == "__main__":
    client = bigquery.Client(project=PROJECT_ID)
    df = client.query(f"select * from `{TABLE}` order by mois").to_dataframe()
    df.to_csv(OUT_PATH, index=False)
    print(f"{len(df)} lignes écrites dans {OUT_PATH.name}")
