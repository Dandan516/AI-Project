"""
Suggests products.
"""
import os
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
df = pd.read_csv("ecommerce_product_dataset.csv", index_col = 0)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    generation_config={"temperature": 0}
    )

def suggest_categories(prompt: str) -> list[str]:
    """
    Returns a list of categories that might be related to the given prompt.
    """
    categories = df["Category"].drop_duplicates().tolist()

    response = model.generate_content(
        f"Here is a list of categories of some retail products: '{categories}'\n"
        f"Given the below prompt, suggest at least 2 related categories from the above list.\n"
        f"{prompt}\n"
        f"The result should only contain the name(s) of the category(s), separated by commas.\n"
        f"If the user prompt does not contain sufficient information, return \"None of the above\" instead."
        )
    comma_separated_categories = response._result.candidates[0].content.parts[0].text
    
    # Turn into list, delete the white spaces,  e.g. [A, B]
    matching_categories = [x.strip() for x in comma_separated_categories.split(sep=",")]
    
    return matching_categories

def find_products(prompt: str) -> pd.DataFrame:
    """
    Returns a list of products that might be related to the given prompt.
    """
    matching_categories = suggest_categories(prompt)
    matching_products = pd.DataFrame({})

    # Finds the category match the response in the data and concatenate each category together
    for x in matching_categories:
        matching_products = pd.concat([matching_products, df.query("Category == @x")])

    # Finds the (item name)index of filtered columns that are greater than 2
    product_counts = matching_products["ProductName"].value_counts()

    # Selects products from eachproduct that match the suggested categories and has 1 instance only
    index_single_row = product_counts[product_counts == 1].index
    filtered_single_row = matching_products[matching_products["ProductName"].isin(index_single_row)]

    # Randomly selects 2 products from each product that match the suggested categories and has >=2 occurences
    index_multiple_rows = product_counts[product_counts >= 2].index
    filtered_multiple_rows = matching_products[matching_products["ProductName"].isin(index_multiple_rows)]
    group = filtered_multiple_rows.groupby("ProductName")
    atmost2row = group.apply(lambda x: x.sample(n=2) if len(x) >= 2 else x).reset_index(drop=True)

    result_df = pd.DataFrame({})
    result_df = pd.concat([atmost2row, filtered_single_row], ignore_index=True)

    return result_df

if __name__ == "__main__":
    print(find_products("I want to go hiking"))