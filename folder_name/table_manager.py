from db_config import get_connection

def create_tables_from_sql(config, sql_script):
    conn = get_connection(config)
    cur = conn.cursor()
    try:
        cur.execute(sql_script)
        conn.commit()
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error executing SQL script: {e}")
    finally:
        cur.close()
        conn.close()

