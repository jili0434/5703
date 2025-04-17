import pandas as pd
from sqlalchemy import create_engine

def clean_data_from_db(config):
    """
    Load original tables from the database, clean common null tokens, and return both raw and cleaned versions.
    """
    engine = create_engine(f"postgresql://{config.user}:{config.password}@{config.host}:{config.port}/{config.name}")
    table_names = ["students", "values", "career_orientation", "personality", "creative_thinking", "family_info"]

    dfs_raw = {}
    dfs_cleaned = {}

    for table_name in table_names:
        try:
            df = pd.read_sql(f"SELECT * FROM {table_name}", engine)
            dfs_raw[table_name] = df
            print(f"Successfully loaded table '{table_name}', shape: {df.shape}")
            df_clean = df.copy()

            # Clean basic object columns: strip + standard null markers
            object_cols = df_clean.select_dtypes(include=["object"]).columns
            for col in object_cols:
                df_clean[col] = df_clean[col].replace(["na", "NA", ""], pd.NA)

            dfs_cleaned[table_name] = df_clean
        except Exception as e:
            print(f"Error loading table '{table_name}': {e}")

    return dfs_raw, dfs_cleaned

def preview_raw_data(dfs_raw):
    """Print preview of original raw data from each table."""
    for sheet, preview in dfs_raw.items():
        print(f"\nPreview of {sheet} (raw data):")
        print(preview.head())

def check_data_types(dfs_cleaned):
    """Print data types of cleaned tables."""
    for table_name, df in dfs_cleaned.items():
        print(f"Data types in {table_name}:\n{df.dtypes}\n")

def check_missing_duplicates(dfs_cleaned):
    for table_name, df in dfs_cleaned.items():
        print(f"Missing values in {table_name}:\n{df.isnull().sum()}")
        print(f"Duplicate rows in {table_name}: {df.duplicated().sum()}\n")

def describe_cleaned_data(dfs_cleaned):
    """Print descriptive statistics of each cleaned table."""
    for sheet, df in dfs_cleaned.items():
        print(f"Descriptive statistics for {sheet}:")
        print(df.describe())
        print("\n")

def standardize_and_clean_columns(dfs_cleaned):
    """
    Perform column-level cleaning and standardization:
    - Strip whitespace
    - Replace standard null tokens
    - Rename 'no' to 'identifier'
    - Standardize language, gender, qualification, and country
    """
    lang_map = {'Mandarin': 'Chinese', 'China': 'Chinese', 'English': 'English', 'Spanish': 'Spanish', 'French': 'French'}
    qual_map = {'A-level': 'A Level', 'A Level': 'A Level', 'IB': 'International Baccalaureate', 'ATAR': 'Australian Tertiary Admission Rank',
                'Diploma': 'Diploma', 'PhD': 'Doctorate', "Master's": "Master's Degree", 'Bachelor': "Bachelor's Degree"}
    gender_map = {'M': 'Male', 'F': 'Female'}
    country_map = {'UK': 'United Kingdom', 'USA': 'United States', 'China': 'China', 'Australia': 'Australia'}

    for table, df in dfs_cleaned.items():
        if 'no' in df.columns:
            df.rename(columns={'no': 'identifier'}, inplace=True)

        object_cols = df.select_dtypes(include=["object"]).columns
        for col in object_cols:
            df[col] = df[col].str.strip()
            df[col] = df[col].replace(["", "na", "NA", "NaN", "nan"], pd.NA)

        if 'first_language' in df.columns:
            df['first_language'] = df['first_language'].replace(lang_map)
        if 'other_language' in df.columns:
            df['other_language'] = df['other_language'].replace(lang_map)
        if 'secondary_qualification' in df.columns:
            df['secondary_qualification'] = df['secondary_qualification'].replace(qual_map)
        if 'gender' in df.columns:
            df['gender'] = df['gender'].replace(gender_map)
        if 'country_born' in df.columns:
            df['country_born'] = df['country_born'].replace(country_map)

        print(f"[Standardized] Preview of '{table}':")
        print(df.head())

    return dfs_cleaned

def merge_all_tables(dfs_cleaned):
    """Merge all cleaned tables on 'identifier' using left join."""
    merged_df = dfs_cleaned["students"]
    for table in ["values", "career_orientation", "personality", "creative_thinking", "family_info"]:
        merged_df = pd.merge(merged_df, dfs_cleaned[table], on="identifier", how="left")
    print("Preview of merged data:")
    print(merged_df.head())
    return merged_df

def drop_duplicates(df):
    """Remove duplicate rows and report the count."""
    duplicate_rows = df.duplicated().sum()
    df = df.drop_duplicates()
    print(f"Number of duplicate rows: {duplicate_rows}")
    return df

def handle_merged_level_cleaning(df):
    """
    Handle field-level cleaning on the merged dataframe:
    - Fill budget with max * 1.1
    - Fill missing MBTI using traits
    - Clean 'concern' column
    - Drop rows missing critical fields
    """
    # Handle budget
    if 'annual_budget_usd (usd)' in df.columns:
        max_val = df['annual_budget_usd (usd)'].max()
        df['annual_budget_usd (usd)'] = df['annual_budget_usd (usd)'].fillna(max_val * 1.1)

    # Drop rows missing essential qualification
    df = df.dropna(subset=['secondary_qualification'])

    # Fill MBTI
    def calculate_mbti(row):
        dim1 = 'E' if row['extrovert'] >= row['introvert'] else 'I'
        dim2 = 'S' if row['sensing'] >= row['intuition_n'] else 'N'
        dim3 = 'T' if row['thinking'] >= row['feeling'] else 'F'
        dim4 = 'J' if row['judging'] >= row['perceiving'] else 'P'
        return dim1 + dim2 + dim3 + dim4

    if 'result_' in df.columns:
        mask = df['result_'].isnull()
        df.loc[mask, 'result_'] = df.loc[mask].apply(calculate_mbti, axis=1)

    # Clean concern column
    if 'concern' in df.columns:
        df['concern'] = df['concern'].fillna('Other')
        df['concern'] = df['concern'].replace('yes', 'Yes')

    print("Remaining missing values:")
    print(df.isnull().sum())

    return df

def export_cleaned_data(df, config):
    """Export cleaned dataframe to CSV, Excel, and PostgreSQL."""
    df.to_csv('cleaned_full_data.csv', index=False)
    df.to_excel('cleaned_full_data.xlsx', index=False)
    engine = create_engine(f"postgresql://{config.user}:{config.password}@{config.host}:{config.port}/{config.name}")
    df.to_sql(name='cleaned_full_data', con=engine, if_exists='replace', index=False)
    print("\"cleaned_full_data\" saved successfully to CSV, Excel, and database.")
