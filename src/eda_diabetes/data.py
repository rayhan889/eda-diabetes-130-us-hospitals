import pandas as pd

from eda_diabetes.paths import DATA_PROCESSED, DATA_RAW

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


MISSING_ID_CODES = {
    "admission_type_id": {5, 6, 8},
    "discharge_disposition_id": {18, 25, 26},
    "admission_source_id": {9, 15, 17, 20, 21},
}

EXPIRED_HOSPICE_DISCHARGE = {11, 13, 14, 19, 20, 21}

NEAR_CONSTANT_COLUMNS = [
    "examide",
    "citoglipton",
    "glimepiride-pioglitazone",
    "metformin-rosiglitazone",
]


MEDICATION_COLUMNS = [
    "metformin",
    "repaglinide",
    "nateglinide",
    "chlorpropamide",
    "glimepiride",
    "acetohexamide",
    "glipizide",
    "glyburide",
    "tolbutamide",
    "pioglitazone",
    "rosiglitazone",
    "acarbose",
    "miglitol",
    "troglitazone",
    "tolazamide",
    "insulin",
    "glyburide-metformin",
    "glipizide-metformin",
    "metformin-pioglitazone",
]

TOP_SPECIALTIES = 10

DISCHARGE_GROUPS = {
    "Home": {1, 6, 8},
    "Facility": {2, 3, 4, 5, 15, 22, 23, 24, 27, 28, 29, 30},
    "Other": {7, 9, 10, 12, 16, 17},
}

ADMISSION_SOURCE_GROUPS = {
    "Referral": {1, 2, 3},
    "Emergency": {7},
    "Transfer": {4, 5, 6, 10, 18, 19, 22, 25, 26},
    "Other": {8, 11, 12, 13, 14, 23, 24},
}


def group_codes(codes: pd.Series, groups: dict[str, set[int]]) -> pd.Series:
    """Map integer codes to group names. NaN stays "Unknown"."""
    lookup = {code: name for name, members in groups.items() for code in members}
    return codes.map(lookup).fillna("Unknown")


def icd9_group(code: str | None) -> str:
    """Map an ICD-9 code to the chapter grouping used by Strack et al. (2014)."""
    if code is None or pd.isna(code):
        return "Unknown"
    if code.startswith("250"):
        return "Diabetes"
    if code[0] in "VE":
        return "Other"
    value = float(code)
    if 390 <= value < 460 or int(value) == 785:
        return "Circulatory"
    if 460 <= value < 520 or int(value) == 786:
        return "Respiratory"
    if 520 <= value < 580 or int(value) == 787:
        return "Digestive"
    if 580 <= value < 630 or int(value) == 788:
        return "Genitourinary"
    if 140 <= value < 240:
        return "Neoplasms"
    if 710 <= value < 740:
        return "Musculoskeletal"
    if 800 <= value < 1000:
        return "Injury"
    return "Other"


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the cleaning decisions from notebooks/02_cleaning.ipynb to the raw frame.

    Needs encounter_id and patient_nbr, so re-run scripts/download_data.py if they are absent.
    """
    df = df.copy()

    # Rows that cannot be readmitted or are invalid.
    df = df[~df["discharge_disposition_id"].isin(EXPIRED_HOSPICE_DISCHARGE)]
    df = df[df["gender"] != "Unknown/Invalid"]

    # One encounter per patient, so encounters are independent.
    df = df.sort_values("encounter_id").drop_duplicates("patient_nbr", keep="first")

    # NaN means unknown here, except the lab results where it means "not measured".
    df = df.drop(columns=["weight", *NEAR_CONSTANT_COLUMNS])
    df[["race", "payer_code", "medical_specialty"]] = df[
        ["race", "payer_code", "medical_specialty"]
    ].fillna("Unknown")
    df[["max_glu_serum", "A1Cresult"]] = df[["max_glu_serum", "A1Cresult"]].fillna("None")

    for col, codes in MISSING_ID_CODES.items():
        df[col] = df[col].mask(df[col].isin(codes))

    for col in ("diag_1", "diag_2", "diag_3"):
        df[col] = df[col].map(icd9_group)

    age_order = sorted(df["age"].unique(), key=lambda s: int(s[1:].split("-")[0]))
    df["age"] = pd.Categorical(df["age"], categories=age_order, ordered=True)
    df["readmitted"] = pd.Categorical(df["readmitted"], ["NO", ">30", "<30"], ordered=True)
    df["readmitted_30"] = (df["readmitted"] == "<30").astype(int)
    visit_cols = ["number_outpatient", "number_emergency", "number_inpatient"]
    df["total_visits"] = df[visit_cols].sum(axis=1)

    df["discharge_group"] = group_codes(df["discharge_disposition_id"], DISCHARGE_GROUPS)
    df["admission_source_group"] = group_codes(df["admission_source_id"], ADMISSION_SOURCE_GROUPS)

    top = df["medical_specialty"].value_counts().drop("Unknown", errors="ignore")
    keep = [*top.index[:TOP_SPECIALTIES], "Unknown"]
    df["medical_specialty"] = df["medical_specialty"].where(
        df["medical_specialty"].isin(keep), "Other"
    )

    meds = df[MEDICATION_COLUMNS]
    df["n_meds_used"] = (meds != "No").sum(axis=1)
    df["n_meds_changed"] = meds.isin(["Up", "Down"]).sum(axis=1)

    for col in df.select_dtypes("object"):
        df[col] = df[col].astype("category")

    return df.reset_index(drop=True)


def load_raw() -> pd.DataFrame:
    """Load the raw CSV written by scripts/download_data.py."""
    return pd.read_csv(DATA_RAW / "diabetic_data.csv", low_memory=False)


def load_processed() -> pd.DataFrame:
    """Load the cleaned parquet written by notebooks/02_cleaning.ipynb."""
    return pd.read_parquet(DATA_PROCESSED / "diabetic_data.parquet")
