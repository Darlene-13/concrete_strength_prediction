# The file is meant to load raw dta, validate it and return a clean data frame ready for feature engineering.
import pandas as pd
import os

def load_raw_data():
    """
    Loads raw concrete dataset from Excel file.

    Args:
        filepath: path to Excel file.
    :return:
        df: pandas dataframe
    """

    #Build filepath relative to project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(base_dir, 'data', 'raw', 'Concrete_Data.xlsx')


    #Validate if the file exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File {filepath} not found.")

    # Load and clean column names
    df = pd.read_excel(filepath)
    df.columns = df.columns.str.strip()

    print("Data loaded successfully. ")
    print(f" Shape: {df.shape[0]} rows x {df.shape[1]} columns")

    return df

def validate_data(df):
    """
    Validates the loaded dataframe for quality.
    Args:
        filepath: path to Excel file.
    Return:
    results: dictionary of validation outcomes
    """
    results = {}

    # Check for missing values
    missing = df.isnull().sum().sum()

    if missing > 0:
        print(f"WARNING: {missing} rows missing from dataframe.")
    else:
        print("No missing values found.")

    results["missing_values"] = missing

    # Checks for duplicate rows and print count
    duplicates = df.duplicated(subset=df.columns, keep=False).sum()
    if duplicates > 0:
       print(f"WARNING: {duplicates} duplicates found in dataframe.")
    else:
        print("No duplicates found.")
    results["duplicates"] = duplicates

    # Confirming no negative values
    negatives = (df < 0).sum().any()
    if negatives:
        print(f"{negatives} rows missing from dataframe.")
    else:
        print("No negative values found.")

    results["negatives"] = negatives

    # return a dictionary values of validation results
    return results

def get_feature_names():
    """
     Return a raw features and target column names.
     Returns:
         features: list of feature names
         target: list of target columns
    """
    target: str = "Concrete compressive strength(MPa, megapascals)"
    features: list[str] = [
        'Cement (component 1)(kg in a m^3 mixture)',
        'Blast Furnace Slag (component 2)(kg in a m^3 mixture)',
        'Fly Ash (component 3)(kg in a m^3 mixture)',
        'Water  (component 4)(kg in a m^3 mixture)',
        'Superplasticizer (component 5)(kg in a m^3 mixture)',
        'Coarse Aggregate  (component 6)(kg in a m^3 mixture)',
        'Fine Aggregate (component 7)(kg in a m^3 mixture)', 'Age (day)',
    ]

    return features, target


if __name__ == '__main__':
    # Testing the functions directly
    df = load_raw_data()
    results = validate_data(df)
    print(results)
    features, target = get_feature_names()
    print(f"\nFEATURES: {len(features)} columns")
    print(f"\nTARGET: {target}")

