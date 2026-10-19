# EDA: Diabetes 130-US Hospitals

Exploratory data analysis of the UCI [Diabetes 130-US Hospitals](https://archive.ics.uci.edu/dataset/296)

## Layout

```
data/raw/            downloaded CSVs (gitignored)
data/processed/      cleaned parquet (gitignored)
notebooks/           numbered, single-purpose notebooks
reports/figures/     exported plots
scripts/             download_data.py
src/eda_diabetes/    paths.py (project paths), data.py (load_raw, load_processed, ID code maps)
```

## Notebooks

1. `01_data_overview` - problem statement, data dictionary, shape and dtypes, repeat patients, summary statistics, cardinality, missing values (including codes that mean missing), target balance, ID code mappings.
2. `02_cleaning` - row and column drops, missing-value treatment, transformations. Runs `eda_diabetes.data.clean` and writes `data/processed/diabetic_data.parquet`.
3. `03_univariate_bivariate` - distributions, outliers, relationships with `readmitted_30`, multivariate views. Saves figures to `reports/figures/`.
4. `04_findings` - summary of findings, limitations and modelling recommendations.

## Setup

```
uv sync
uv run python scripts/download_data.py
```

Run the notebooks in order. Use the project kernel (`uv run jupyter ...` or the VS Code kernel picker).
