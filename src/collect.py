import io
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd
import requests

ECB_URL = "https://data-api.ecb.europa.eu/service/data"
INSEE_URL = "https://bdm.insee.fr/series/sdmx/data/SERIES_BDM"
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

START = "2015-01"
# un an de plus pour le taux directeur (taux en vigueur en janvier 2015)
# et pour l'IPC (inflation sur 12 mois de 2015)
EARLY_START = "2014-01"
MIN_LAST_PERIOD = "2026"

# nom -> (jeu de données, clé, début)
ECB_SERIES = {
    "taux_directeur_bce": ("FM", "B.U2.EUR.4F.KR.MRR_FR.LEV", EARLY_START),
    "taux_credit_habitat": ("MIR", "M.FR.B.A2C.A.R.A.2250.EUR.N", START),
    "volume_credit_habitat": ("MIR", "M.FR.B.A2C.A.B.A.2250.EUR.N", START),
    "taux_credit_conso": ("MIR", "M.FR.B.A2B.A.R.A.2250.EUR.N", START),
    "volume_credit_conso": ("MIR", "M.FR.B.A2B.A.B.A.2250.EUR.N", START),
}

# nom -> (idbank, début) : IPC base 2025, ensemble des ménages, France
INSEE_SERIES = {
    "ipc_ensemble": ("011814630", EARLY_START),
}

COLUMNS = ["KEY", "TIME_PERIOD", "OBS_VALUE", "OBS_STATUS"]


def fetch_ecb(dataset, key, start):
    response = requests.get(
        f"{ECB_URL}/{dataset}/{key}",
        params={"format": "csvdata", "startPeriod": start},
        timeout=30,
    )
    response.raise_for_status()
    return pd.read_csv(io.StringIO(response.text), usecols=lambda c: c in COLUMNS)


def parse_insee_xml(xml_text, idbank):
    rows = []
    for element in ET.fromstring(xml_text).iter():
        # on ignore l'espace de noms XML devant le nom de la balise
        if element.tag.split("}")[-1] == "Obs":
            rows.append(
                {
                    "KEY": idbank,
                    "TIME_PERIOD": element.get("TIME_PERIOD"),
                    "OBS_VALUE": element.get("OBS_VALUE"),
                    "OBS_STATUS": element.get("OBS_STATUS"),
                }
            )
    df = pd.DataFrame(rows, columns=COLUMNS)
    df["OBS_VALUE"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce")
    # l'INSEE renvoie les mois du plus récent au plus ancien
    return df.sort_values("TIME_PERIOD").reset_index(drop=True)


def fetch_insee(idbank, start):
    response = requests.get(
        f"{INSEE_URL}/{idbank}", params={"startPeriod": start}, timeout=30
    )
    response.raise_for_status()
    return parse_insee_xml(response.text, idbank)


def collect_all():
    data = {}
    for name, (dataset, key, start) in ECB_SERIES.items():
        data[name] = fetch_ecb(dataset, key, start)
    for name, (idbank, start) in INSEE_SERIES.items():
        data[name] = fetch_insee(idbank, start)
    return data


def check_series(name, df):
    if df.empty:
        return f"{name} : série vide"
    last = str(df["TIME_PERIOD"].iloc[-1])
    if last < MIN_LAST_PERIOD:
        return f"{name} : la série s'arrête à {last}"
    return None


def save_raw(df, name):
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(RAW_DIR / f"{name}.csv", index=False)


if __name__ == "__main__":
    problems = []
    for name, df in collect_all().items():
        problem = check_series(name, df)
        if problem:
            problems.append(problem)
        else:
            print(
                f"{name:24} {len(df):4} lignes | "
                f"{df['TIME_PERIOD'].iloc[0]} -> {df['TIME_PERIOD'].iloc[-1]}"
            )
        save_raw(df, name)

    if problems:
        print("ATTENTION :")
        for problem in problems:
            print(f"  - {problem}")
    else:
        print("Contrôles OK")
