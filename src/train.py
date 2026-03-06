import pandas as pd
import numpy as np
import os
import sys
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import (mean_absolute_error, root_mean_squared_error, r2_score)
from xgboost import XGBRegressor
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_loader import load_raw_data
from feature_engineering import engineer_features
from pre_processing import get_column_groups, build_processor, build_pipeline

def remove_outliers(X_train, y_train):
    """
    Removes target outliers using IQR method.
    Only applied to training data — never test data.

    Args:
        X_train : training features
        y_train : training target
    Returns:
        X_train_clean : cleaned training features
        y_train_clean : cleaned training target
    """

    Q1 = y_train.quantile(0.25)
    Q3 = y_train.quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers_mask = (y_train < lower_bound) | (y_train > upper_bound)

    y_train_clean = y_train[
        ~outliers_mask]  # remove outliers  using ~ o tilde ensures to return true where the data is clean
    X_train_clean = X_train[~outliers_mask]  # remove same rows from features

    X_train_clean = X_train_clean.reset_index(drop=True)
    y_train_clean = y_train_clean.reset_index(drop=True)

    return X_train_clean, y_train_clean

def train_model(X_train_clean, y_train_clean, numerical_features, categorical_features):
    """
    Builds pipeline and runs GridSearchCV tuning.

    Args:
        X_train_clean        : cleaned training features
        y_train_clean        : cleaned training target
        numerical_features   : list of numerical column names
        categorical_features : list of categorical column names
    Returns:
        grid_search : fitted GridSearchCV object
    """

    # Calling build processor
    preprocessor = build_processor(numerical_features, categorical_features)
    model = build_pipeline(
        model = XGBRegressor(n_estimators=100, random_state=42),
        preprocessor = preprocessor
    )
    # Dictionary of parameters
    param_grid = {
        'model__n_estimators': [100, 200, 300],
        'model__learning_rate': [0.05, 0.1, 0.2],
        'model__max_depth': [3, 5, 6],
        'model__subsample': [0.8, 1.0],
        'model__colsample_bytree': [0.8, 1.0]
    }

    # Building GridSearchCV
    grid_search = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        cv=5,
        scoring='neg_root_mean_squared_error',
        # Maximizes scores so RMSE is negated, the best score will be the least negative number.
        n_jobs=-1,
        verbose=1  # Prints progress
    )

    grid_search = grid_search.fit(X_train_clean, y_train_clean)

    print(f" Best CV RMSE: {-grid_search.best_score_:.4f} MPa")
    print(f" Best Params : {grid_search.best_params_}")
    return grid_search

def evaluate_model(model, X_test, y_test):
    """
    Evaluates model on test set and prints metrics.

    Args:
        model  : fitted pipeline or GridSearchCV
        X_test : test features
        y_test : test target
    Returns:
        results : dictionary of metric values
    """
    # Dictionary for metric values
    results = {}

    # make the predictions.
    y_pred_xg = model.predict(X_test)

    # Model evaluation metrics
    rmse_xg = root_mean_squared_error(y_test, y_pred_xg)
    mae_xg = mean_absolute_error(y_test, y_pred_xg)
    r2_xg = r2_score(y_test, y_pred_xg)

    results['rmse'] = rmse_xg
    results['mae'] = mae_xg
    results['r2'] = r2_xg

    print("\n✅ Model Evaluation")
    print("=" * 35)
    print(f"RMSE : {rmse_xg:.2f} MPa")
    print(f"MAE  : {mae_xg:.2f} MPa")
    print(f"R²   : {r2_xg:.4f}")
    return results

def save_model(grid_search):
    """
    Saves fitted pipeline to models/ directory.

    Args:
        model    : fitted pipeline object
        filename : name of saved file
    """

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_dir = os.path.join(base_dir, 'models')
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, 'best_model.pkl')
    joblib.dump(grid_search.best_estimator_, model_path)
    # Save the full pipeline — preprocessor + model together
    print(f"Model saved successfully to: {model_path}")

def run_training():
    """
    Master function — runs full training pipeline end to end.
    Load → Engineer → Split → Clean → Train → Evaluate → Save
    """

    print("="*50)
    print("CONCRETE STRENGTH PREDICTION TRAINING")
    print("="*50)

    # Step 1: Load the data
    df_raw = load_raw_data()

    # Step 2: Engineer the features
    df = engineer_features(df_raw)

    #Step 3: Define x and y
    target = "Concrete compressive strength(MPa, megapascals)"
    X = df.drop(target, axis=1)
    y = df[target]

    #Step 4: Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"\n Split: {X_train.shape[0]} train shape, {X_test.shape[0]} test shape")

    # Step 5: Remove outliers
    X_train_clean, y_train_clean = remove_outliers(X_train, y_train)

    # Step 6: Get column groups
    numerical_features, categorical_features = get_column_groups(df, target)

    # Step 7: Train
    grid_search = train_model(X_train_clean, y_train_clean, numerical_features, categorical_features)


    # Step 8: Evaluate
    results = evaluate_model(grid_search, X_test, y_test)

    # Step 9: Save
    save_model(grid_search)

    print("TRAINING COMPLETED")

    return grid_search, results

if __name__ == "__main__":
    run_training()
