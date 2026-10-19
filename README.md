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

1. `01_data_overview` - shape, dtypes, `?` placeholders, target balance, missing values, ID code mappings.
2. `02_cleaning` - cleaning, writes `data/processed/diabetic_data.parquet` (stub).
3. `03_univariate_bivariate` - distributions and relationships with `readmitted` (stub).
