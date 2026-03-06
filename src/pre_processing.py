from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


def get_column_groups(df, target):
    """
    Separates dataframe columns into numerical
    and categorical groups for ColumnTransformer.

    Args:
        df     : engineered dataframe
        target : target column name string
    Returns:
        numerical_features   : list of numerical column names
        categorical_features : list of categorical column names
    """

    numerical_features = [col for col in df.columns
                          if col != target and col != "age_group"
                          ]
    categorical_features = ['age_group']

    return numerical_features, categorical_features

def build_processor(numerical_features, categorical_features):
    """
    Builds sklearn ColumnTransformer with:
    - StandardScaler on numerical features
    - OneHotEncoder on categorical features

    Args:
        numerical_features   : list of numerical column names
        categorical_features : list of categorical column names
    Returns:
        preprocessor : fitted ColumnTransformer object
    """

    # Combining the  two to a column transformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ]
    )

    return preprocessor

def build_pipeline(model, preprocessor):
    """
    Builds full sklearn Pipeline with preprocessor and model.

    Args:
        model                : sklearn model object
        numerical_features   : list of numerical column names
        categorical_features : list of categorical column names
    Returns:
        pipeline : sklearn Pipeline object
    """

    pipeline = Pipeline(
        steps = [
            ('preprocessor', preprocessor),
            ('model', model)
        ]
    )

    return pipeline

if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    from data_loader import load_raw_data
    from feature_engineering import engineer_features
    from xgboost import XGBRegressor

    # Test full chain
    df_raw = load_raw_data()
    df_engineered = engineer_features(df_raw)



    #Step 1 Get column names
    target = 'Concrete compressive strength(MPa, megapascals)'
    numerical_features, categorical_features = get_column_groups(
        df_engineered, target
    )

    print(f"Numerical features  : {len(numerical_features)}")
    print(f"Categorical features: {categorical_features}")

    # Step 2 Build preprocessor
    preprocessor = build_processor(numerical_features, categorical_features)

    # Step 3: Build Pipeline
    pipeline = build_pipeline(
        XGBRegressor(),
        preprocessor
    )
    print("\n Pipeline built successfully")
    print(pipeline)
