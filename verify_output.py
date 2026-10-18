import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

raw_file = BASE_DIR / "student_enrollment_raw.csv"
cleaned_file = BASE_DIR / "student_enrollment_cleaned.csv"

raw_df = pd.read_csv(raw_file, dtype=str, keep_default_na=False)
cleaned_df = pd.read_csv(cleaned_file, dtype=str, keep_default_na=False)

print("\n===== ETL VALIDATION REPORT =====")

print("Input Records :", len(raw_df))
print("Output Records:", len(cleaned_df))

print("Missing Student IDs:",
      (cleaned_df["Student_ID"].str.strip() == "").sum())

print("Missing Names:",
      (cleaned_df["Name"].str.strip() == "").sum())

print("Invalid Emails:",
      (cleaned_df["Email"] == "INVALID_EMAIL").sum())

print("Missing Phone Numbers:",
      (cleaned_df["Phone"] == "MISSING").sum())

print("Invalid Dates:",
      (cleaned_df["Enrolled_Date"] == "INVALID_DATE").sum())

same_ids = (
    raw_df["Student_ID"].tolist()
    == cleaned_df["Student_ID"].tolist()
)

print("Original Student IDs Preserved:", same_ids)

if (
    len(raw_df) == len(cleaned_df)
    and same_ids
    and (cleaned_df["Name"].str.strip() != "").all()
):
    print("\nSUCCESS: All student records are preserved.")
else:
    print("\nWARNING: Review the cleaned CSV.")