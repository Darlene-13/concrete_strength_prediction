"""
    This file is the bridge between FastAPI and the ML model. It has two responsibilities:

    Load the saved model once when the app starts — not on every request
    Take a ConcreteInput object, convert it to the format the model expects, run prediction and return the result
"""

import os
import sys
import joblib
import pandas as pd

# Add src/ to path so we can import feature_engineering
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, 'src')
sys.path.insert(0, SRC_DIR)

from feature_engineering import engineer_features
from schemas import ConcreteInput

#-------Column name mapping------API names to model column names
COLUMN_MAPPING = {
    'cement': 'Cement (component 1)(kg in a m^3 mixture)',
    'blast_furnace_slag': 'Blast Furnace Slag (component 2)(kg in a m^3 mixture)',
    'fly_ash': 'Fly Ash (component 3)(kg in a m^3 mixture)',
    'water': 'Water  (component 4)(kg in a m^3 mixture)',
    'superplasticizer': 'Superplasticizer (component 5)(kg in a m^3 mixture)',
    'coarse_aggregate': 'Coarse Aggregate  (component 6)(kg in a m^3 mixture)',
    'fine_aggregate': 'Fine Aggregate (component 7)(kg in a m^3 mixture)',
    'age': 'Age (day)'
}



#--------Model version tag -------
MODEL_VERSION = "xgboost_tuned_v1"

def load_model():
    """
    Loads saved pipeline from models/ directory.
    Called once at application startup.
    Returns:
        model : fitted sklearn Pipeline
    """

    model_path = os.path.join(BASE_DIR, 'models', 'best_model.pkl')

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")

    model = joblib.load(model_path)
    print("Loaded model successfully")
    return model



def input_to_dataframe(input_data: ConcreteInput) -> pd.DataFrame:
    """
    Converts ConcreteInput Pydantic object to
    engineered feature dataframe ready for prediction.

    Args:
        input_data : validated ConcreteInput object
    Returns:
        df_engineered : single row engineered dataframe
    """
    # Step 1: Convert pydantic object to dictionary
    raw_dict = input_data.model_dump()
    #Step 2: Rename API fields to model column names
    mapped_dict = {
        COLUMN_MAPPING[key]:value
        for key, value in raw_dict.items()
    }


    #Step 3: Add target column as placeholder
    #engineer_feature expects a full dataframe structure
    mapped_dict['Concrete compressive strength(MPa, megapascals)'] = 0.0

    # Step 4: Convert it to a single row dataframe
    df = pd.DataFrame([mapped_dict])

    # Step 5: Run feature engineering
    df_engineered = engineer_features(df)

    return df_engineered

def predict(model, input_data: ConcreteInput) -> dict:
    """
    Runs prediction on a single concrete mix input.

    Args:
        model      : loaded sklearn Pipeline
        input_data : validated ConcreteInput object
    Returns:
        result : dictionary with prediction and metadata
    """

    # Step 1- Engineer features
    df_engineered = input_to_dataframe(input_data)

    # Step 2: Predict
    prediction = model.predict(df_engineered)[0]

    # Step 3: Return a result dictionary

    return {
        "predicted_strength_mpa": round(float(prediction), 2),
        "model_version": MODEL_VERSION,
        "status": "success"
    }




