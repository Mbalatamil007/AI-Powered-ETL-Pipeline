import os
import json
import time
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

from data_validator import validate_student


# =====================================
# STEP 1: CONFIGURATION
# =====================================

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is missing in .env file")

client = OpenAI(api_key=api_key)

INPUT_FILE = BASE_DIR / "student_enrollment_raw.csv"

OUTPUT_FILE = BASE_DIR / "student_enrollment_cleaned.csv"


# =====================================
# STEP 2: LOAD CSV FILE
# =====================================

df = pd.read_csv(
    INPUT_FILE,
    dtype=str,
    keep_default_na=False
)

print("\n===================================")
print("   PYTHON OPENAI ETL AUTOMATION")
print("===================================")

print(f"\nTotal Students Loaded: {len(df)}")


# =====================================
# STEP 3: OPENAI CLEANING PROMPT
# =====================================

SYSTEM_PROMPT = """
You are a student enrollment data cleaning assistant.

Clean the provided student record.

Rules:

1. Student_ID:
   Preserve the original Student_ID.

2. Name:
   Convert to Title Case.
   Do not invent missing names.

3. Email:
   Convert to lowercase.
   Invalid or missing emails must be INVALID_EMAIL.

4. Phone:
   Remove spaces and special characters.
   If not exactly 10 digits, return MISSING.

5. Course:
   python -> Python
   ml -> Machine Learning
   machine learning -> Machine Learning
   data science -> Data Science
   Unsupported or missing -> UNKNOWN

6. Fee_Paid:
   yes, true, 1 -> true
   no, false, 0 -> false

7. City:
   Convert to Title Case.
   Missing -> UNKNOWN

8. Enrolled_Date:
   Convert DD-MM-YYYY to YYYY-MM-DD.
   Invalid -> INVALID_DATE.

Return ONLY a valid JSON object.

Use exactly these fields:
Student_ID, Name, Email, Phone,
Course, Fee_Paid, City, Enrolled_Date.

Do not include explanations or markdown.
Do not invent missing information.
"""


# =====================================
# STEP 4: CLEAN ONE STUDENT USING AI
# =====================================

def clean_student_with_ai(student):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": json.dumps(student)
            }
        ]
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("OpenAI returned an empty response")

    return json.loads(content)


# =====================================
# STEP 5: PROCESS ALL 50 STUDENTS
# =====================================

cleaned_students = []

failed_students = []

for index, row in df.iterrows():

    student = row.to_dict()

    student_id = student.get("Student_ID", "")

    print(
        f"\nProcessing Student {index + 1}/{len(df)}: "
        f"{student_id}"
    )

    try:

        # Clean student using OpenAI
        ai_result = clean_student_with_ai(student)

        # Validate AI response using Python
        validated_result = validate_student(
            student,
            ai_result
        )

        cleaned_students.append(validated_result)

        print(f"SUCCESS: {student_id}")

    except Exception as error:

        print(f"AI FAILED: {student_id} - {error}")

        # Preserve and clean original data
        validated_result = validate_student(
            student,
            {}
        )

        cleaned_students.append(validated_result)

        failed_students.append(student_id)

    # Small delay between requests
    time.sleep(0.2)


# =====================================
# STEP 6: CREATE FINAL CSV FILE
# =====================================

cleaned_df = pd.DataFrame(cleaned_students)

cleaned_df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


# =====================================
# STEP 7: DISPLAY ETL SUMMARY
# =====================================

print("\n===================================")
print("        ETL COMPLETED")
print("===================================")

print(f"Input Records  : {len(df)}")
print(f"Output Records : {len(cleaned_df)}")

print(
    f"AI Success     : "
    f"{len(df) - len(failed_students)}"
)

print(
    f"AI Failed      : "
    f"{len(failed_students)}"
)

print(f"\nCleaned CSV File: {OUTPUT_FILE}")

print("\nFirst 5 Cleaned Student Records:")

print(cleaned_df.head().to_string(index=False))

if failed_students:
    print("\nStudents cleaned using Python fallback:")
    print(", ".join(failed_students))