import pandas as pd

#function that returns the df associated with a specific file
def get_df():

    file_name = "data/billionaires.csv"
    df_billionaires = pd.read_csv(file_name)
    
    return df_billionaires