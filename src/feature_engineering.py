# Takes the dataframe from the data loader and returns a fully engineered data frame ready for preprocessing pipeline.

import os
import numpy as np

def drop_duplicates(df):
    """
    Removes duplicate rows and resets index.
    Args: df: raw dataframe
    Returns: df: cleaned dataframe
    """

    # Drop duplicates and reset index
    df = df.drop_duplicates().reset_index(drop=True)
    return df

def create_ratio_features(df):
    """
    Creates Group 1 ratio features.
    w_c_ratio, w_b_ratio, agg_binder_ratio
    Args: df: dataframe
    Returns: df with new ratio columns
    """

    # Ratio features
    df.columns.str.strip()
    # 1. Water to Cement Ratio
    df["water_cement_ratio"] = df["Water  (component 4)(kg in a m^3 mixture)"] / df[
        "Cement (component 1)(kg in a m^3 mixture)"]

    # 2. Water to Binder ratio
    total_binder_content = df["Cement (component 1)(kg in a m^3 mixture)"] + df[
        "Blast Furnace Slag (component 2)(kg in a m^3 mixture)"] + df["Fly Ash (component 3)(kg in a m^3 mixture)"]
    df["water_binder_ratio"] = df["Water  (component 4)(kg in a m^3 mixture)"] / total_binder_content

    # 3. Aggregate to binder ratio
    total_aggregate_quantity = df["Coarse Aggregate  (component 6)(kg in a m^3 mixture)"] + df[
        "Fine Aggregate (component 7)(kg in a m^3 mixture)"]
    df["agg_binder_ratio"] = total_aggregate_quantity / total_binder_content

    return df


def create_summation_features(df):
    """
    Creates Group 2 summation features.
    total_binder_content, total_aggregate_content, total_mix
    """

    df.columns.str.strip()
    # 1. Total binder content
    df["total_binder_content"] = df["Cement (component 1)(kg in a m^3 mixture)"] + df[
        "Blast Furnace Slag (component 2)(kg in a m^3 mixture)"] + df["Fly Ash (component 3)(kg in a m^3 mixture)"]
    # 2. Total aggregate content
    df["total_aggregate_content"] = df["Coarse Aggregate  (component 6)(kg in a m^3 mixture)"] + df[
        "Fine Aggregate (component 7)(kg in a m^3 mixture)"]
    # 3. Total mix content
    df["total_mix"] = df["Cement (component 1)(kg in a m^3 mixture)"] + df[
        "Blast Furnace Slag (component 2)(kg in a m^3 mixture)"] + df["Fly Ash (component 3)(kg in a m^3 mixture)"] + \
                      df["Coarse Aggregate  (component 6)(kg in a m^3 mixture)"] + df[
                          "Fine Aggregate (component 7)(kg in a m^3 mixture)"] + df[
                          "Water  (component 4)(kg in a m^3 mixture)"]


    return df


def create_scm_features(df):
    """
    Creates Group 3 SCM ratio features.
    cement_ratio, slag_ratio, flyash_ratio
    """
    df.columns.str.strip()
    # 1. Cement Dominance Ratio
    df["cement_ratio"] = df["Cement (component 1)(kg in a m^3 mixture)"] / df["total_binder_content"]
    # 2.  Slag Replacement Ratio
    df["slag_ratio"] = df["Blast Furnace Slag (component 2)(kg in a m^3 mixture)"] / df["total_binder_content"]
    # 3. Fly Ash Replacement Ratio
    df["flyash_ratio"] = df["Fly Ash (component 3)(kg in a m^3 mixture)"] / df["total_binder_content"]

    return df

def create_age_features(df):
    """
    Creates Group 4 age transformation features.
    log_age, age_group
    """
    # Age transformations
    df.columns.str.strip()
    # 1. Log age
    df["log_age"] = np.log(df["Age (day)"] + 1)

    # 2. Age group categorical
    def age_groups(age):
        df.columns.str.strip()
        if age <= 7:
            return "Early"
        elif age <= 28:
            return "Standard"
        elif age <= 90:
            return "Mature"
        else:
            return "Long-term"

    df["age_group"] = df["Age (day)"].apply(age_groups)
    print(df["age_group"].value_counts())

    return df

def create_interaction_features(df):
    """
       Creates Group 5 interaction features.
       cement_age, slag_age, flyash_age interactions
    """
    df.columns.str.strip()
    # 1. Slag age interaction
    df["slag_age_interaction"] = df["Blast Furnace Slag (component 2)(kg in a m^3 mixture)"] * df["log_age"]

    # 2. Fly ash age interaction
    df["flyash_age_interaction"] = df["Fly Ash (component 3)(kg in a m^3 mixture)"] * df["log_age"]

    # 3. Cement age interaction
    df["cement_age_interaction"] = df["Cement (component 1)(kg in a m^3 mixture)"] * df["log_age"]

    return df

def create_flag_features(df):
    """
    Creates Group 6 binary flag features.
    sp_flag, slag_flag, flyash_flag
    """

    # Binary flag features
    # 1. Superplasticizer flag
    def uses_superplasticizer(superplasticizer):
        df.columns.str.strip()
        return 1 if superplasticizer > 0 else 0

    df["sp_flag"] = df["Superplasticizer (component 5)(kg in a m^3 mixture)"].apply(uses_superplasticizer)

    # 2. Slag flag
    def uses_slag(slag):
        return 1 if slag > 0 else 0

    df["slag_flag"] = df["Blast Furnace Slag (component 2)(kg in a m^3 mixture)"].apply(uses_slag)

    # 3. Uses fly ash
    def uses_flyash(flyash):
        return 1 if flyash > 0 else 0

    df["flyash_flag"] = df["Fly Ash (component 3)(kg in a m^3 mixture)"].apply(uses_flyash)

    return df


def drop_weak_features(df):
    """
    Drops low importance features identified in analysis.
    """

    df = df.drop(
        columns=["slag_ratio", "flyash_ratio", "flyash_flag", "flyash_age_interaction", "total_aggregate_content",
                 "Coarse Aggregate  (component 6)(kg in a m^3 mixture)",
                 "Fine Aggregate (component 7)(kg in a m^3 mixture)"])

    # Dir path
    dir_path = os.path.join(os.path.dirname(os.getcwd()), "data", "processed")
    # Make the directory if it does not exist
    os.makedirs(dir_path, exist_ok=True)
    # Save the new dataset
    file_path = os.path.join(dir_path, "Concrete_processed_data.xlsx")
    df.to_excel(file_path, index=False)
    print(f"Processed data saved at: {file_path}")

    return df


def engineer_features(df):
    """
    Master function — runs full feature engineering pipeline.
    Args: df: raw dataframe
    Returns: df_engineered: fully engineered dataframe
    """

    df = drop_duplicates(df)
    df = create_ratio_features(df)
    df = create_summation_features(df)
    df = create_scm_features(df)
    df = create_age_features(df)
    df = create_interaction_features(df)
    df = create_flag_features(df)
    df = drop_weak_features(df)

    print("Feature Engineering Completed")
    print(f"   Shape: {df.shape[0]} rows x {df.shape[1]} columns")

    return df


if __name__ == "__main__":
    from data_loader import load_raw_data

    df_raw = load_raw_data()
    df_engineered = engineer_features(df_raw)
    print(df_engineered.columns.tolist())