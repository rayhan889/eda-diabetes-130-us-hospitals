"""Download the UCI Diabetes 130-US Hospitals dataset into data/raw/."""

import pandas as pd
from ucimlrepo import fetch_ucirepo

from eda_diabetes.paths import DATA_RAW

DATASET_ID = 296
DATA_FILE = DATA_RAW / "diabetic_data.csv"
VARIABLES_FILE = DATA_RAW / "variables.csv"


def main() -> None:
    if DATA_FILE.exists():
        print(f"{DATA_FILE} already exists, skipping download")
        return

    DATA_RAW.mkdir(parents=True, exist_ok=True)
    dataset = fetch_ucirepo(id=DATASET_ID)
    df = pd.concat([dataset.data.features, dataset.data.targets], axis=1)
    df.to_csv(DATA_FILE, index=False)
    dataset.variables.to_csv(VARIABLES_FILE, index=False)
    print(f"Wrote {len(df):,} rows to {DATA_FILE}")


if __name__ == "__main__":
    main()
