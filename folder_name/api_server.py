import os
import pandas as pd
import random
from datetime import datetime
from openai import OpenAI

# Load OpenAI API key securely, fallback to manual override (only for testing)
api_key = ""
client = OpenAI(api_key=api_key)

def validate_api_key():
    try:
        client.models.list()
        print("✅ OpenAI API key is valid.")
    except Exception as e:
        print("❌ Invalid API Key:", e)

def generate_custom_prompt_response(system_prompt: str, user_prompt: str) -> str:
    if not client.api_key:
        return "Error: OPENAI_API_KEY is not set or invalid."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": user_prompt.strip()}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred while contacting OpenAI: {str(e)}"

def load_random_user_prompt(file_path: str) -> str:
    try:
        df = pd.read_csv(file_path)
        random_row = df.sample(n=1).iloc[0]
        user_input = str(random_row.to_dict())
        print("\nSelected random sample as user prompt:")
        print(user_input)
        return user_input
    except Exception as e:
        print("Error loading data:", e)
        return input("Enter user prompt manually (fallback): ")

def get_unique_filename(base_filename: str) -> str:
    if not os.path.exists(base_filename):
        return base_filename

    base, ext = os.path.splitext(base_filename)
    counter = 1
    while True:
        new_filename = f"{base}_{counter}{ext}"
        if not os.path.exists(new_filename):
            return new_filename
        counter += 1

def write_response_to_file(user_prompt: str, response: str, folder: str = ".", csv_name: str = "response_log.csv"):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, csv_name)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row = pd.DataFrame([{
        "timestamp": timestamp,
        "user_prompt": user_prompt,
        "gpt_response": response
    }])

    if not os.path.exists(path):
        row.to_csv(path, index=False, encoding='utf-8-sig')
    else:
        row.to_csv(path, mode='a', index=False, header=False, encoding='utf-8-sig')

    print(f"\n✅ Output appended to '{path}'")

# Optional direct run
if __name__ == "__main__":
    validate_api_key()

    system_input = ()

    user_input = load_random_user_prompt("cleaned_full_data.csv")
    result = generate_custom_prompt_response(system_input, user_input)
    print("\nResponse:\n", result)
    write_response_to_file(user_input, result)
