# Test: Regression Model Evaluation

Testing a regression model with MAE and RMSE tracking


## Model Predictions

Generated 20 samples with true = 2*x + 3 + noise


### Sample Predictions

 * x= 0: true=  3.99, pred=  7.40, error= 3.40
 * x= 1: true=  4.72, pred=  4.32, error= 0.40
 * x= 2: true=  8.30, pred=  7.20, error= 1.09
 * x= 3: true= 12.05, pred=  4.73, error= 7.32
 * x= 4: true= 10.53, pred=  9.37, error= 1.16


## Regression Metrics

Tracking with ±10% tolerance for error metrics

 * MAE: 2.788 (was 2.788, Δ+0.000)
 * RMSE: 3.659 (was 3.659, Δ-0.000)
 * R² Score: 0.878 (was 0.878, Δ+0.000)


## Minimum Requirements


 * MAE ≤ 5.0.. ok
 * RMSE ≤ 6.0.. ok
 * R² ≥ 0.80.. ok
