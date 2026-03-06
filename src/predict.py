import pandas as pd
import os
import sys
import joblib

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from feature_engineering import engineer_features


def load_model():
    """
    Loads saved pipeline from models/ directory.
    Returns:
        model : fitted sklearn Pipeline
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, 'models', 'best_model.pkl')

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at: {model_path}")

    model = joblib.load(model_path)
    print("Model loaded successfully")
    return model


def prepare_input(mix_dict):
    """
    Converts raw mix ingredient dictionary into
    fully engineered single-row dataframe.

    Args:
        mix_dict : dictionary of raw mix ingredients
    Returns:
        df_engineered : single row engineered dataframe
    """
    df = pd.DataFrame([mix_dict])
    df_engineered = engineer_features(df)
    return df_engineered


def predict_strength(mix_dict):
    """
    Master prediction function.
    Takes raw mix ingredients, returns predicted strength.

    Args:
        mix_dict   : dictionary of raw ingredients
    Returns:
        prediction : float — predicted strength in MPa
    """
    # Step 1 — Load model
    model = load_model()

    # Step 2 — Prepare input
    df_engineered = prepare_input(mix_dict)

    # Step 3 — Predict
    prediction = model.predict(df_engineered)[0]

    # Step 4 — Print results
    print("\n" + "="*40)
    print("Predicted Compressive Strength:")
    print(f"→  {prediction:.2f} MPa")
    print("="*40)
    print("Mix Details:")
    print(f"  Cement      : {mix_dict['Cement (component 1)(kg in a m^3 mixture)']} kg/m³")
    print(f"  Water       : {mix_dict['Water  (component 4)(kg in a m^3 mixture)']} kg/m³")
    print(f"  w/c ratio   : {mix_dict['Water  (component 4)(kg in a m^3 mixture)'] / mix_dict['Cement (component 1)(kg in a m^3 mixture)']:.2f}")
    print(f"  Age         : {mix_dict['Age (day)']} days")

    return prediction


if __name__ == "__main__":
    sample_mix = {
        'Cement (component 1)(kg in a m^3 mixture)': 350.0,
        'Blast Furnace Slag (component 2)(kg in a m^3 mixture)': 0.0,
        'Fly Ash (component 3)(kg in a m^3 mixture)': 0.0,
        'Water  (component 4)(kg in a m^3 mixture)': 175.0,
        'Superplasticizer (component 5)(kg in a m^3 mixture)': 0.0,
        'Coarse Aggregate  (component 6)(kg in a m^3 mixture)': 1050.0,
        'Fine Aggregate (component 7)(kg in a m^3 mixture)': 800.0,
        'Age (day)': 28,
        'Concrete compressive strength(MPa, megapascals)': 0.0
    }

    result = predict_strength(sample_mix)