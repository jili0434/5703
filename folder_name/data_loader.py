import pandas as pd
import psycopg2

def load_data_to_db(config, excel_path):
    conn = psycopg2.connect(
        dbname=config.name,
        user=config.user,
        password=config.password,
        host=config.host,
        port=config.port
    )
    cur = conn.cursor()

    xlsx = pd.ExcelFile(excel_path)

    table_sheet_info = {
        "students": "Section0",
        "values": "Section 1 - Value",
        "career_orientation": "Section2 - Career Orientation",
        "personality": "Section 3 - Personality",
        "creative_thinking": "Section 4 - creativity thinking",
        "family_info": "Section 5 - Family"
    }

    # Delete in correct order to respect foreign key constraints
    delete_order = [
        "values", "career_orientation", "personality",
        "creative_thinking", "family_info", "students"
    ]
    for table in delete_order:
        cur.execute(f"DELETE FROM {table}")

    for table_name, sheet_name in table_sheet_info.items():
        df = xlsx.parse(sheet_name)
        records = df.values.tolist()
        placeholders = ', '.join(['%s'] * df.shape[1])
        insert_sql = f'INSERT INTO {table_name} VALUES ({placeholders})'
        cur.executemany(insert_sql, records)
        print(f"✅ Inserted into {table_name}: {len(records)} records")

    conn.commit()
    cur.close()
    conn.close()