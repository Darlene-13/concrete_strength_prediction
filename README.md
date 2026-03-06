# Concrete Compressive Strength Prediction
### Domain: Civil Engineering | Type: Regression | Model: XGBoost

---

## Problem Statement

Concrete compressive strength is the most critical mechanical property 
in structural engineering. Traditional measurement requires destroying 
a concrete cylinder in a lab after 28 days of curing — slow and expensive.

This project builds a machine learning model that predicts compressive 
strength (MPa) from mix ingredients and curing age, enabling engineers 
to screen mix designs computationally before physical testing.

---

## Project Structure
```
concrete_strength_prediction/
│
├── data/
│   ├── raw/                          ← original UCI dataset
│   └── processed/                    ← engineered feature dataset
│
├── notebooks/
│   ├── 01_EDA.ipynb                  ← exploratory data analysis
│   ├── 02_feature_engineering.ipynb  ← feature creation & validation
│   ├── 03_preprocessing_and_modeling.ipynb ← pipeline & model training
│   └── 04_evaluation.ipynb           ← residual analysis & feature importance
│
├── src/
│   ├── data_loader.py                ← loads and validates raw data
│   ├── feature_engineering.py        ← creates all engineered features
│   ├── pre_processing.py             ← builds sklearn pipeline
│   ├── train.py                      ← full training pipeline
│   └── predict.py                    ← single mix prediction
│
├── models/
│   └── best_model.pkl                ← saved tuned XGBoost pipeline
│
├── reports/
│   └── figures/                      ← all evaluation plots
│
├── requirements.txt
└── README.md
```

---

## Dataset

- **Source:** UCI Machine Learning Repository
- **Author:** Prof. I-Cheng Yeh (1998)
- **Link:** https://archive.ics.uci.edu/dataset/165/concrete+compressive+strength
- **Samples:** 1030 rows → 1005 after duplicate removal
- **Features:** 8 raw ingredients + age
- **Target:** Compressive Strength in MPa (range: 2.3 – 82.6 MPa)

---

## Setup & Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/concrete_strength_prediction.git
cd concrete_strength_prediction
```

**2. Create virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

---

## Usage

**Run full training pipeline:**
```bash
python src/train.py
```

**Make a single prediction:**
```bash
python src/predict.py
```

**Run notebooks in order:**
```
01_EDA.ipynb
02_feature_engineering.ipynb
03_preprocessing_and_modeling.ipynb
04_evaluation.ipynb
```

---

## Feature Engineering

17 new features created from 8 raw inputs using concrete domain knowledge:

| Group | Features | Engineering Basis |
|-------|----------|------------------|
| Ratio | w/c ratio, w/b ratio, agg/binder ratio | Abrams Law |
| Summation | total binder, total mix | Cementitious system behaviour |
| SCM Ratios | cement ratio, slag ratio | Binder composition |
| Age | log age, age group | Non-linear hydration kinetics |
| Interactions | cement×age, slag×age | Time-dependent reactivity |
| Flags | sp_flag, slag_flag | Mix design philosophy |

**Key finding:** Top engineered feature `cement_age_interaction` 
achieved +0.701 correlation with strength vs raw Cement at +0.488.

---

## Results

| Model | RMSE | MAE | R² |
|-------|------|-----|----|
| Linear Regression | 6.89 MPa | 5.17 MPa | 0.8409 |
| Random Forest | 4.96 MPa | 3.48 MPa | 0.9177 |
| XGBoost (default) | 4.32 MPa | 2.70 MPa | 0.9375 |
| **XGBoost (tuned)** | **4.20 MPa** | **2.56 MPa** | **0.9407** |

**Best model:** Tuned XGBoost Pipeline  
**Cross-validation RMSE:** 4.04 MPa  
**Explains:** 94.07% of all concrete strength variation

### Top 5 Features by Importance
1. `slag_flag` — 27.6%
2. `cement_age_interaction` — 16.6%
3. `water_binder_ratio` — 15.3%
4. `sp_flag` — 10.9%
5. `log_age` — 5.8%

---

## Tech Stack

| Purpose | Library |
|---------|---------|
| Data handling | pandas, numpy |
| Visualisation | matplotlib, seaborn |
| ML pipeline | scikit-learn |
| Boosting model | XGBoost |
| Model persistence | joblib |
| Statistics | scipy |

---

## Limitations

- Underestimates high strength mixes above 60 MPa
- Trained on lab conditions — field variability not captured
- Residuals show mild right skew at high strength range
- Additional validation recommended for C60+ grade concrete

---

## Author

**Darlene Wendy**  
Civil/ML Engineering Project Series — Project 1 of 4  
Regression → Classification → Clustering → Dimensionality Reduction