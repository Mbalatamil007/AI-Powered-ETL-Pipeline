import re
from datetime import datetime


def title_case(value):
    return str(value or "").strip().title()


def validate_student(original, cleaned):

    # Preserve original Student ID and Name if AI omits them
    student_id = str(original.get("Student_ID", "")).strip()

    name = title_case(
        cleaned.get("Name") or original.get("Name")
    )

    # Validate Email
    email = str(
        cleaned.get("Email") or original.get("Email") or ""
    ).strip().lower()

    email_pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"

    if not re.fullmatch(email_pattern, email):
        email = "INVALID_EMAIL"

    # Validate Phone
    phone = str(
        cleaned.get("Phone") or original.get("Phone") or ""
    )

    phone = re.sub(r"\D", "", phone)

    if len(phone) != 10:
        phone = "MISSING"

    # Standardize Course
    course = str(
        cleaned.get("Course") or original.get("Course") or ""
    ).strip().lower()

    course_map = {
        "python": "Python",
        "ml": "Machine Learning",
        "machine learning": "Machine Learning",
        "data science": "Data Science"
    }

    course = course_map.get(course, "UNKNOWN")

    # Convert Fee_Paid to Boolean
    fee_value = str(
        original.get("Fee_Paid", "")
    ).strip().lower()

    fee_paid = fee_value in ("yes", "true", "1")

    # Standardize City
    city = title_case(
        cleaned.get("City") or original.get("City")
    ) or "UNKNOWN"

    # Validate Date using original source
    original_date = str(
        original.get("Enrolled_Date", "")
    ).strip()

    try:
        date_value = datetime.strptime(
            original_date, "%d-%m-%Y"
        ).strftime("%Y-%m-%d")
    except ValueError:
        date_value = "INVALID_DATE"

    return {
        "Student_ID": student_id,
        "Name": name,
        "Email": email,
        "Phone": phone,
        "Course": course,
        "Fee_Paid": fee_paid,
        "City": city,
        "Enrolled_Date": date_value
    }