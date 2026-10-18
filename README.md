# Python + OpenAI ETL Automation

## Project Overview

This project demonstrates an automated ETL (Extract, Transform, Load)
pipeline using Python, Pandas, and the OpenAI API.

The application reads raw student enrollment data from a CSV file,
uses OpenAI GPT-4.1-mini to clean and standardize the records,
validates the results using Python, and generates a cleaned CSV file.

The project successfully processed 50 student records.

## Technologies Used

- Python
- Pandas
- OpenAI API (GPT-4.1-mini)
- Python-dotenv
- CSV
- Visual Studio Code

## Project Architecture

```text
        Student Enrollment CSV
                  |
                  v
          Python CSV Loader
                  |
                  v
          Pandas DataFrame
                  |
                  v
          OpenAI GPT-4.1-mini
                  |
                  v
          AI Data Cleaning
                  |
                  v
          Python Data Validator
                  |
                  v
          Cleaned Student CSV
                  |
                  v
          ETL Validation Report
```

## Project Structure

```text
Python_OpenAI_ETL_Automation/
│
├── student_enrollment_raw.csv
├── student_enrollment_cleaned.csv
├── csv_loader.py
├── ai_cleaner.py
├── data_validator.py
├── verify_output.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## ETL Process

### 1. Extract

The application reads 50 student records from:

`student_enrollment_raw.csv`

Pandas is used to load and process the CSV data.

### 2. Transform

OpenAI GPT-4.1-mini cleans the student records.

Cleaning operations include:

- Standardizing student names
- Identifying invalid email addresses
- Validating phone numbers
- Standardizing course names
- Converting fee payment status to Boolean
- Standardizing city names
- Converting enrollment dates to YYYY-MM-DD format

### 3. Validate

Python validates the AI-generated output.

Validation rules ensure:

- Student IDs are preserved
- Student names are not missing
- Invalid emails are marked INVALID_EMAIL
- Invalid phone numbers are marked MISSING
- Enrollment dates follow YYYY-MM-DD format

### 4. Load

The cleaned student records are exported to:

`student_enrollment_cleaned.csv`

## Installation

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure OpenAI API

Create a `.env` file in the project root.

```env
OPENAI_API_KEY=your_openai_api_key
```

Never commit your actual API key to GitHub.

## How to Run

### Load CSV Data

```bash
python csv_loader.py
```

### Execute ETL Automation

```bash
python ai_cleaner.py
```

### Verify Cleaned Data

```bash
python verify_output.py
```

## Sample Data Transformation

| Field | Original Value | Cleaned Value |
|---|---|---|
| Student_ID | STU1001 | STU1001 |
| Name | manoj k | Manoj K |
| Email | manojk@gmail | INVALID_EMAIL |
| Phone | 9876543210 | 9876543210 |
| Course | python | Python |
| Fee_Paid | yes | True |
| City | Chennai | Chennai |
| Enrolled_Date | 23-05-2025 | 2025-05-23 |

## ETL Execution Results

| Metric | Result |
|---|---|
| Total Input Records | 50 |
| Total Output Records | 50 |
| Successful OpenAI Requests | 50 |
| Failed OpenAI Requests | 0 |
| Missing Student IDs | 0 |
| Missing Student Names | 0 |
| Invalid Emails Identified | 21 |
| Missing or Invalid Phone Numbers | 9 |
| Invalid Enrollment Dates | 0 |
| Student IDs Preserved | Yes |

## Key Features

- Automated CSV data processing
- OpenAI-powered data cleaning
- Python-based output validation
- Error handling with fallback processing
- Preservation of original student IDs
- Automated CSV generation
- ETL execution summary
- Final validation report

## Future Enhancements

- Streamlit dashboard for uploading CSV files
- PostgreSQL database integration
- Automated ETL scheduling
- Data quality reporting
- Batch processing for larger datasets
- Logging and error monitoring

## Project Status

**Core ETL Automation Completed Successfully**

All 50 student records were processed, and the final validation
confirmed record preservation with no missing student IDs or names.