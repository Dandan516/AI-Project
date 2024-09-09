import pandas as pd
import os
import google.generativeai as genai
from dotenv import load_dotenv

def classify(user_prompt):
    '''
    Analyzes user prompt and suggests related categories from the list of categories accordingly.
    '''
    load_dotenv()
    api_key = os.environ["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash-latest",generation_config={"temperature": 0},)

    df = pd.read_csv('https://raw.githubusercontent.com/Dandan516/AI-Project/main/ecommerce_product_dataset.csv',index_col = 0)
    category = df['Category'].drop_duplicates().tolist()

    response = model.generate_content(
        f"Here is a list of categories of some retail products: '{category}'\n"
        f"Given the below prompt, suggest two or more related categories from the above list.\n"
        f"{user_prompt}'\n"
        f"The result should only contain the name(s) of the category(s), separated by commas.\n"
        f"If the user prompt does not contain sufficient information, return \"None of the above\" instead."
        )
    
    return response._result.candidates[0].content.parts[0].text

def main():
    '''
    For testing only.
    '''
    print(classify("I want to sleep"))

if __name__ == "__main__":
    main()

