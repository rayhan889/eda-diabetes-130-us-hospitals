import pandas as pd

from eda_diabetes.paths import DATA_PROCESSED, DATA_RAW

# Code tables from the dataset's original IDS_mapping.csv.
ADMISSION_TYPE = {
    1: "Emergency",
    2: "Urgent",
    3: "Elective",
    4: "Newborn",
    5: "Not Available",
    6: "NULL",
    7: "Trauma Center",
    8: "Not Mapped",
}

DISCHARGE_DISPOSITION = {
    1: "Discharged to home",
    2: "Transferred to another short term hospital",
    3: "Transferred to SNF",
    4: "Transferred to ICF",
    5: "Transferred to another type of inpatient care institution",
    6: "Transferred to home with home health service",
    7: "Left AMA",
    8: "Transferred to home under care of Home IV provider",
    9: "Admitted as an inpatient to this hospital",
    10: "Neonate discharged to another hospital for neonatal aftercare",
    11: "Expired",
    12: "Still patient or expected to return for outpatient services",
    13: "Hospice / home",
    14: "Hospice / medical facility",
    15: "Transferred within this institution to Medicare approved swing bed",
    16: "Referred to another institution for outpatient services",
    17: "Referred to this institution for outpatient services",
    18: "NULL",
    19: "Expired at home (Medicaid only, hospice)",
    20: "Expired in a medical facility (Medicaid only, hospice)",
    21: "Expired, place unknown (Medicaid only, hospice)",
    22: "Transferred to another rehab facility",
    23: "Transferred to a long term care hospital",
    24: "Transferred to a nursing facility certified under Medicaid only",
    25: "Not Mapped",
    26: "Unknown/Invalid",
    27: "Transferred to a federal health care facility",
    28: "Referred to a psychiatric hospital or psychiatric unit",
    29: "Transferred to a Critical Access Hospital (CAH)",
    30: "Transferred to another type of health care institution not defined elsewhere",
}

ADMISSION_SOURCE = {
    1: "Physician Referral",
    2: "Clinic Referral",
    3: "HMO Referral",
    4: "Transfer from a hospital",
    5: "Transfer from a Skilled Nursing Facility (SNF)",
    6: "Transfer from another health care facility",
    7: "Emergency Room",
    8: "Court/Law Enforcement",
    9: "Not Available",
    10: "Transfer from critical access hospital",
    11: "Normal Delivery",
    12: "Premature Delivery",
    13: "Sick Baby",
    14: "Extramural Birth",
    15: "Not Available",
    17: "NULL",
    18: "Transfer from another Home Health Agency",
    19: "Readmission to same Home Health Agency",
    20: "Not Mapped",
    21: "Unknown/Invalid",
    22: "Transfer from hospital inpatient, same facility, separate claim",
    23: "Born inside this hospital",
    24: "Born outside this hospital",
    25: "Transfer from Ambulatory Surgery Center",
    26: "Transfer from Hospice",
}

ID_MAPPINGS = {
    "admission_type_id": ADMISSION_TYPE,
    "discharge_disposition_id": DISCHARGE_DISPOSITION,
    "admission_source_id": ADMISSION_SOURCE,
}


def load_raw() -> pd.DataFrame:
    """Load the raw CSV written by scripts/download_data.py."""
    return pd.read_csv(DATA_RAW / "diabetic_data.csv", low_memory=False)


def load_processed() -> pd.DataFrame:
    """Load the cleaned parquet written by notebooks/02_cleaning.ipynb."""
    return pd.read_parquet(DATA_PROCESSED / "diabetic_data.parquet")
