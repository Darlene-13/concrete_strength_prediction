# Regression

Regression in machine learning is a supervised learning technique used to predict continuous numerical values by learning the relationship between input variables (features) and an output variable (target). It helps quantify how changes in one or more factors influence a measurable outcome and is widely used in forecasting, risk analysis, decision-making, and trend estimation.

- Works with real-valued output variables  
- Helps identify the strength and type of relationships between variables  
- Supports both simple and complex predictive models  
- Commonly used for price prediction, trend forecasting, and risk scoring  

## Types of Regression

Regression methods can be classified based on the number of predictor variables and the nature of the relationship between variables.

### 1. Simple Linear Regression
Simple Linear Regression models the relationship between one independent variable and a continuous dependent variable by fitting a straight line that minimizes the sum of squared errors. It assumes a constant rate of change, meaning the output varies proportionally with the input.

- **Application:** Estimating house price based only on size  
- **Advantage:** Highly interpretable due to its simple mathematical structure  
- **Disadvantage:** Cannot capture curved or complex data patterns  

### 2. Multiple Linear Regression
Multiple Linear Regression extends simple linear regression by incorporating multiple independent variables to predict a continuous outcome. Each predictor is assigned a coefficient that reflects its individual impact while holding other variables constant.

- **Application:** Predicting house prices using factors such as size, location, age, and number of rooms  
- **Advantage:** Captures the combined influence of multiple factors simultaneously  
- **Disadvantage:** Performance can degrade in the presence of multicollinearity (highly correlated features)  

### 3. Ridge and Lasso Regression
Ridge and Lasso are regularized linear regression techniques that add penalty terms to limit large coefficients and reduce overfitting. Ridge (L2) shrinks coefficients smoothly, while Lasso (L1) can reduce some coefficients to zero, enabling feature selection.

- **Application:** High-dimensional datasets such as marketing attribution or gene expression analysis  
- **Advantage:** Controls overfitting and improves generalization, especially with many predictors  
- **Disadvantage:** Penalty terms can make interpretation less straightforward  

### 4. Support Vector Regression (SVR)
Support Vector Regression applies the principles of Support Vector Machines to regression tasks. It fits a function within a defined margin (epsilon tube) and penalizes errors only when predictions fall outside this boundary. Kernel functions allow SVR to model non-linear relationships.

- **Application:** Predicting continuous outcomes such as stock values or energy consumption  
- **Advantage:** Effective for high-dimensional datasets and non-linear patterns  
- **Disadvantage:** Computationally intensive and requires careful parameter tuning  

### 5. Decision Tree Regression
Decision Tree Regression splits data into hierarchical branches based on feature thresholds. Each internal node represents a decision rule, and leaf nodes represent predicted continuous values. The model learns patterns by recursively partitioning the data to minimize prediction error.

- **Application:** Predicting customer spending based on demographic and financial features  
- **Advantage:** Easy to visualize and interpret  
- **Disadvantage:** Prone to overfitting, especially with deep trees  

### 6. Random Forest Regression
Random Forest Regression is an ensemble method that builds multiple decision trees using different data samples and averages their predictions. This reduces the overfitting tendency of individual trees and improves accuracy through diversity (bagging).

- **Application:** Sales forecasting, demand planning, and churn prediction  
- **Advantage:** High accuracy and robust performance, even with noisy data  
- **Disadvantage:** Less interpretable due to the large number of trees (black-box behavior)  

## Regression Evaluation Metrics

Evaluation metrics measure how well a regression model performs by comparing predicted values to actual values.

1. **Mean Absolute Error (MAE):** The average absolute difference between predicted and actual values.  
2. **Mean Squared Error (MSE):** The average squared difference between predicted and actual values, giving more weight to large errors.  
3. **Root Mean Squared Error (RMSE):** The square root of MSE, expressed in the same units as the target variable.  
4. **Huber Loss:** A hybrid loss function that combines MAE and MSE behavior, balancing robustness to outliers with sensitivity to large errors.  
5. **R² Score (Coefficient of Determination):** Indicates how well the model explains variance in the target variable, typically ranging from 0 to 1, with higher values representing a better fit.  