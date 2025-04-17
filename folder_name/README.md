
# 🎓 Student Career Advisor (Data Processing + GPT Recommendation)

This project provides a complete pipeline for processing student career survey data and generating GPT-based career advice using OpenAI.

---

## 📁 Project Structure

| File                  | Description |
|-----------------------|-------------|
| `prepare_data.py`     | Load and clean raw Excel data, export cleaned dataset |
| `run_advisor.py`      | Randomly select a student and query OpenAI GPT |
| `data_loader.py`      | Load Excel sheets into PostgreSQL (auto-clears old data) |
| `data_cleaner.py`     | Perform standardization, merging, missing value handling |
| `api_server.py`       | GPT interaction wrapper with logging and key validation |
| `db_config.py`        | PostgreSQL connection configuration |
| `table_manager.py`    | (Optional) Create tables from SQL schema |
| `prompt.txt`          | Custom system prompt for GPT (manually editable) |

---

## 🚀 How to Use

### 1️⃣ Install Dependencies

```bash
pip install pandas openai psycopg2 sqlalchemy openpyxl
```

---

### 2️⃣ Configure Database (Required)

In `prepare_data.py`, set your PostgreSQL credentials:

```python
config = DBConfig(
    name="your_db_name",
    user="your_username",
    password="your_password",
    host="localhost",
    port="5432"
)
```

---

### 3️⃣ Set Your OpenAI API Key (Required)

In `api_server.py`, set OpenAI API Key:
---

### 4️⃣ Run Data Preparation (once)

```bash
python prepare_data.py
```

- Loads and cleans `Survey_result_2025.xlsx`
- Exports `cleaned_full_data.csv`
- (Optional) writes data into PostgreSQL tables

---

### 5️⃣ Run GPT Advisor (anytime)

```bash
python run_advisor.py
```

- Reads system prompt from prompt.txt
- Selects a random student record from cleaned_full_data.csv
- Sends a combined prompt to GPT-4 for career advice
- Prints the result and saves it into response_log.csv

---

## ⚠️ Notes

- Sheet names are pre-configured in `data_loader.py`
- You can use the advisor without PostgreSQL — just run `run_advisor.py`

---

## 📎 Example Output (CSV)

| timestamp           | user_prompt        | gpt_response |
|--------------------|--------------------|--------------|
| 2024-04-09 21:55:02 | {...}              | As an ENFP...|

---
