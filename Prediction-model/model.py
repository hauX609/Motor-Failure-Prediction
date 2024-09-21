import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from imblearn.over_sampling import SMOTE
from tqdm import tqdm
from itertools import product

# Load the data from the CSV file
csv_file_path = 'motor_data.csv'  # Update this path if necessary
df = pd.read_csv(csv_file_path)

# Check if the data is loaded correctly
print(df.head())

# Encode categorical variables
label_encoder = LabelEncoder()
df['motor_type'] = label_encoder.fit_transform(df['motor_type'])

# Derive power and energy consumption
df['power'] = df['speed'] * df['torque'] / 9550
df['energy_consumption'] = df['power'] * df['load'] / 100  # Simplified energy consumption calculation

# Check if the derived columns are added correctly
print(df[['power', 'energy_consumption']].head())

# Normalize/scale the data
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df.drop(columns=['failure_type', 'remaining_life', 'recommendation']))

# Split the data into training and testing sets
X = scaled_features
y_failure = df['failure_type']
y_life = df['remaining_life']
X_train, X_test, y_failure_train, y_failure_test, y_life_train, y_life_test = train_test_split(X, y_failure, y_life, test_size=0.2, random_state=42)

# Apply SMOTE to the training data
smote = SMOTE(random_state=42)
X_train_resampled, y_failure_train_resampled = smote.fit_resample(X_train, y_failure_train)

# Hyperparameter tuning for RandomForestClassifier
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Create a list of all parameter combinations
param_combinations = [dict(zip(param_grid, v)) for v in product(*param_grid.values())]

# Initialize the progress bar
pbar = tqdm(total=len(param_combinations))

# Custom GridSearchCV with progress bar
best_score = -np.inf
best_params = None

for params in param_combinations:
    model = RandomForestClassifier(random_state=42, **params)
    scores = cross_val_score(model, X_train_resampled, y_failure_train_resampled, cv=StratifiedKFold(n_splits=5), scoring='accuracy', n_jobs=-1)
    mean_score = np.mean(scores)
    
    if mean_score > best_score:
        best_score = mean_score
        best_params = params
    
    pbar.update(1)

pbar.close()

# Train a model to predict failure type on resampled data with best hyperparameters
failure_model = RandomForestClassifier(**best_params, random_state=42)
failure_model.fit(X_train_resampled, y_failure_train_resampled)

# Train a model to predict remaining life
life_model = RandomForestRegressor(n_estimators=100, random_state=42)
life_model.fit(X_train, y_life_train)

# Make predictions
failure_predictions = failure_model.predict(X_test)
life_predictions = life_model.predict(X_test)

# Map failure types to recommendations
recommendations = {
    0: 'N/A',
    1: 'Replace bearings',
    2: 'Check cooling system',
    3: 'Balance the motor',
    4: 'Inspect electrical connections',
    5: 'Perform full inspection'
}

# Provide recommendations based on predicted failure types
predicted_recommendations = [recommendations[failure] for failure in failure_predictions]

# Create a DataFrame with the predictions and recommendations
results = pd.DataFrame({
    'predicted_failure_type': failure_predictions,
    'predicted_remaining_life': life_predictions,
    'recommendation': predicted_recommendations
})

# Save the results to a CSV file
results.to_csv('predicted_motor_data.csv', index=False)

# Evaluate the classification model
accuracy = accuracy_score(y_failure_test, failure_predictions)
precision = precision_score(y_failure_test, failure_predictions, average='weighted')
recall = recall_score(y_failure_test, failure_predictions, average='weighted')
f1 = f1_score(y_failure_test, failure_predictions, average='weighted')
conf_matrix = confusion_matrix(y_failure_test, failure_predictions)

print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1 Score: {f1}")
print("Confusion Matrix:")
print(conf_matrix)

# Plot confusion matrix
plt.figure(figsize=(10, 7))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=recommendations.values(), yticklabels=recommendations.values())
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# Evaluate the regression model
mae = mean_absolute_error(y_life_test, life_predictions)
mse = mean_squared_error(y_life_test, life_predictions)
rmse = np.sqrt(mse)
r2 = r2_score(y_life_test, life_predictions)

print(f"Mean Absolute Error (MAE): {mae}")
print(f"Mean Squared Error (MSE): {mse}")
print(f"Root Mean Squared Error (RMSE): {rmse}")
print(f"R-squared (R²): {r2}")

# Feature importance for classification model
feature_importances = failure_model.feature_importances_
features = df.drop(columns=['failure_type', 'remaining_life', 'recommendation']).columns
importance_df = pd.DataFrame({'Feature': features, 'Importance': feature_importances})
importance_df = importance_df.sort_values(by='Importance', ascending=False)

print("Feature Importances for Classification Model:")
print(importance_df)

# Feature importance for regression model
feature_importances_reg = life_model.feature_importances_
importance_df_reg = pd.DataFrame({'Feature': features, 'Importance': feature_importances_reg})
importance_df_reg = importance_df_reg.sort_values(by='Importance', ascending=False)

print("Feature Importances for Regression Model:")
print(importance_df_reg)

# Perform cross-validation for classification model
cv_scores = cross_val_score(failure_model, X, y_failure, cv=5, scoring='accuracy')
print(f"Cross-Validation Accuracy Scores: {cv_scores}")
print(f"Mean Cross-Validation Accuracy: {cv_scores.mean()}")

# Perform cross-validation for regression model
cv_scores_reg = cross_val_score(life_model, X, y_life, cv=5, scoring='r2')
print(f"Cross-Validation R² Scores: {cv_scores_reg}")
print(f"Mean Cross-Validation R²: {cv_scores_reg.mean()}")

# Save the trained models to disk
joblib.dump(failure_model, 'failure_model.pkl')
print("Failure model saved as 'failure_model.pkl'")
joblib.dump(life_model, 'life_model.pkl')
print("Life model saved as 'life_model.pkl'")

# After fitting the scaler and label encoder during training
joblib.dump(scaler, 'scaler.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')