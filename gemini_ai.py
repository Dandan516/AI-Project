import pandas as pd
import os
import google.generativeai as genai

def ask_gemini(user_prompt: str, df: pd.DataFrame) -> str:
    '''
    Returns the categories that might be related to the user's prompt in a comma-separated string.
    '''
    api_key = os.environ["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash-latest",generation_config={"temperature": 0},)

    categories = df['Category'].drop_duplicates().tolist()

    response = model.generate_content(
        f"Here is a list of categories of some retail products: '{categories}'\n"
        f"Given the below prompt, suggest two or more related categories from the above list.\n"
        f"{user_prompt}'\n"
        f"The result should only contain the name(s) of the category(s), separated by commas.\n"
        f"If the user prompt does not contain sufficient information, return \"None of the above\" instead."
        )
    
    return response._result.candidates[0].content.parts[0].text

def match_categories(user_prompt: str) -> pd.DataFrame:
    '''
    Returns a list of products that might be related to the user's prompt.
    '''
    df = pd.read_csv('https://raw.githubusercontent.com/Dandan516/AI-Project/main/ecommerce_product_dataset.csv',index_col = 0)
    
    print("User prompt is \'" + user_prompt + "\'")
    #turn into list, delete the white spaces,  e.g. [A, B]
    matching_categories = [x.strip() for x in ask_gemini(user_prompt, df).split(sep=",")]
    matching_products = pd.DataFrame({})
    #find the category match the response in the data and concatenate each category together 
    for x in matching_categories:
        matching_products = pd.concat([matching_products, df.query("Category == @x")])

    
    return matching_products



