import os
from pathlib import Path

from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()

PROJECT_ID = os.environ["GCP_PROJECT_ID"]
DATASET = "raw"
LOCATION = "EU"
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

# même schéma pour toutes les séries
SCHEMA = [
    bigquery.SchemaField("KEY", "STRING"),
    bigquery.SchemaField("TIME_PERIOD", "STRING"),
    bigquery.SchemaField("OBS_VALUE", "FLOAT"),
    bigquery.SchemaField("OBS_STATUS", "STRING"),
]


def create_dataset(client):
    dataset = bigquery.Dataset(f"{PROJECT_ID}.{DATASET}")
    dataset.location = LOCATION
    client.create_dataset(dataset, exists_ok=True)


def load_csv(client, path):
    table_id = f"{PROJECT_ID}.{DATASET}.{path.stem}"
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        schema=SCHEMA,
        write_disposition="WRITE_TRUNCATE",  # on remplace la table à chaque chargement
    )
    with open(path, "rb") as f:
        client.load_table_from_file(f, table_id, job_config=job_config).result()
    return client.get_table(table_id).num_rows


if __name__ == "__main__":
    client = bigquery.Client(project=PROJECT_ID)
    create_dataset(client)
    for path in sorted(RAW_DIR.glob("*.csv")):
        print(f"{path.stem:24} {load_csv(client, path):4} lignes chargées")
