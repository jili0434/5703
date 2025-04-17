import openpyxl

from api_server import (
    validate_api_key,
    load_random_user_prompt,
    generate_custom_prompt_response,
    write_response_to_file
)

def main():
    validate_api_key()

    with open('prompt.txt', 'r', encoding='utf-8') as f:
        system_input = f.read()

    user_input = load_random_user_prompt("cleaned_full_data.csv")
    result = generate_custom_prompt_response(system_input, user_input)
    print("\nResponse:\n", result)
    write_response_to_file(user_input, result)

if __name__ == "__main__":
    main()