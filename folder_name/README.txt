Student Career Advisor (Data Processing + GPT Recommendation)

This project provides a full-stack pipeline for managing and analyzing student career intention data. It includes:

- Data cleaning from raw Excel sheets
- PostgreSQL database creation and population
- Preprocessing, merging, and export of clean dataset
- GPT-based personalized career advice generation

The system enables education researchers and career advisors to transform messy survey responses into structured insight and AI-powered guidance.

------------------------------------------------------------------------------

Project Structure

File                         | Description
---------------------------- | ---------------------------------------------------------------
prepare_data.py              | Main pipeline: load → clean → merge → export
data_loader.py               | Load Excel to PostgreSQL, trim columns, convert NaN to None
data_cleaner.py              | Clean, deduplicate, and merge all DB tables
run_advisor.py               | Send student record to OpenAI and store GPT advice
api_server.py                | OpenAI API wrapper with logging and key control
table_manager.py             | Creates PostgreSQL schema from .sql script
db_config.py                 | Stores DB connection settings
StudnetDatabase.sql          | SQL schema file for table creation and constraints
prompt.txt                   | System prompt used for GPT interactions
response_log.csv             | Logs GPT outputs and student prompts
cleaned_full_data.xlsx/csv   | Exported and cleaned data, ready for modeling or analysis

------------------------------------------------------------------------------

How to Use

1. Install Dependencies
------------------------
pip install pandas openai psycopg2 sqlalchemy openpyxl

2. Configure Database
---------------------
Set credentials in prepare_data.py:

config = DBConfig(
    name="your_db",
    user="your_user",
    password="your_password",
    host="localhost",
    port="5432"
)

3. Create Database Tables
-------------------------
Optional (if not already created):

from table_manager import create_tables_from_sql
create_tables_from_sql(config, open("StudnetDatabase.sql").read())

4. Set Your OpenAI API Key (Required)
---------------------
In `api_server.py`, set OpenAI API Key:

5. Run Data Preparation
------------------------
python prepare_data.py

This will:
- Load Survey_result_2025（update）.xlsx
- Remove invalid fields except 3 new integers in section0
- Convert NaN to None to ensure DB compatibility
- Clean and merge tables from DB
- Export cleaned_full_data.xlsx/csv
- Store cleaned dataset in PostgreSQL

6. Generate GPT Career Advice
------------------------------
python run_advisor.py

- Loads 1 random student record
- Applies prompt from prompt.txt
- Sends to GPT-4
- Logs output in response_log.csv

------------------------------------------------------------------------------


------------------------------------------------------------------------------

Example Output (response_log.csv)
---------------------------------

timestamp             | user_prompt         | gpt_response
---------------------|---------------------|------------------------------
2024-04-09 21:55:02  | {"dream_career":...}| "As an ENFP, you may consider..."

------------------------------------------------------------------------------
