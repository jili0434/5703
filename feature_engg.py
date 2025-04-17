import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

def merge_all_tables_with_features(dfs_cleaned):
    """
    Merge all cleaned tables and apply feature engineering:
    - Create interaction features
    - Extract date-based features
    - Normalize numeric columns
    - Encode categorical features
    """
    # Merge tables on "identifier"
    merged_df = dfs_cleaned["students"]
    for table in ["values", "career_orientation", "personality", "creative_thinking", "family_info"]:
        merged_df = pd.merge(merged_df, dfs_cleaned[table], on="identifier", how="left")

    # Feature Engineering
    # 1. Interaction Features
    numeric_cols = merged_df.select_dtypes(include=["number"]).columns
    if len(numeric_cols) > 1:
        merged_df["interaction_personality"] = merged_df["extrovert"] * merged_df["introvert"]

    # 2. Date Features
    date_cols = merged_df.select_dtypes(include=["datetime64", "object"]).columns
    for col in date_cols:
        try:
            merged_df[col] = pd.to_datetime(merged_df[col])
            merged_df[f"{col}_year"] = merged_df[col].dt.year
            merged_df[f"{col}_month"] = merged_df[col].dt.month
            merged_df[f"{col}_day"] = merged_df[col].dt.day
        except Exception:
            pass  # Skip columns that cannot be converted to datetime

    # 3. Normalize Numeric Features
    scaler = MinMaxScaler()
    if len(numeric_cols) > 0:
        merged_df[numeric_cols] = scaler.fit_transform(merged_df[numeric_cols])

    # 4. Encode Categorical Features
    object_cols = merged_df.select_dtypes(include=["object"]).columns
    label_encoder = LabelEncoder()
    for col in object_cols:
        merged_df[col] = merged_df[col].fillna("Unknown")  # Fill missing for encoding
        merged_df[col] = label_encoder.fit_transform(merged_df[col].astype(str))

    print("Preview of merged data with feature engineering:")
    print(merged_df.head())

    return merged_df
```