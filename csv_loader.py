import pandas as pd
from pathlib import Path

# Get project directory
BASE_DIR = Path(__file__).resolve().parent

# CSV file location
CSV_FILE = BASE_DIR / "student_enrollment_raw.csv"

# Read CSV file
df = pd.read_csv(
    CSV_FILE,
    dtype=str,
    keep_default_na=False
)

# Display first 5 student records
print("\nFirst 5 Student Records:")
print(df.head().to_string(index=False))

# Display total student count
print("\nTotal Students:", len(df))

# Display column names
print("\nCSV Columns:")
print(df.columns.tolist())