from data_loader import load_data_to_db
from data_cleaner import (
    clean_data_from_db,
    preview_raw_data,
    standardize_and_clean_columns,
    merge_all_tables,
    drop_duplicates,
    handle_merged_level_cleaning,
    export_cleaned_data
)
from db_config import DBConfig

def main():
    # Define DB connection
    config = DBConfig(
        name="",
        user="",
        password="",
        host="",
        port=""
        # name = "Daniel",
        # user = "postgres",
        # password = "88888887",
        # host = "localhost",
        # port = "5432"
    )

    # Load Excel data into DB
    load_data_to_db(config, "Survey_result_2025.xlsx")

    # Data cleaning workflow
    dfs_raw, dfs_cleaned = clean_data_from_db(config)
    preview_raw_data(dfs_raw)
    dfs_cleaned = standardize_and_clean_columns(dfs_cleaned)
    merged_df = merge_all_tables(dfs_cleaned)
    merged_df = drop_duplicates(merged_df)
    merged_df = handle_merged_level_cleaning(merged_df)

    # Export to CSV, Excel, and DB
    export_cleaned_data(merged_df, config)

if __name__ == "__main__":
    main()
