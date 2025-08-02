import json
from eda_pipeline import EDA
import pandas as pd
import os

if __name__ == "__main__":
    with open('data/gemini/extracted_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

<<<<<<< HEAD
    # type is no use in this example, median will be used by default
    eda = EDA(data) 
    eda.run_pipeline()

    eda.get_dataframe().to_csv('eda_output.csv', index=False)
=======
    # Initialize the EDA pipeline với dataset chatgpt
    eda = EDA(data)
    eda.run_pipeline()
    df = eda.get_dataframe()
    print(eda.get_metadata())
>>>>>>> parent of 989ebe4 (Update statistical report func)
