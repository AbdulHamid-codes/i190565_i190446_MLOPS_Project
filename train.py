import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import mlflow

# Read the preprocessed data
df_merged = pd.read_csv('regionSlotRequestsTotal.csv')
df_merged.columns = ['start_region_hash', 'demand']

# Read the data for picked requests
df_picked = pd.read_csv('pickedRequestTotal.csv')
df_picked.columns = ['start_region_hash', 'slots', 'picked']

# Merge the two data frames
df_merged = pd.merge(df_merged, df_picked, on=['start_region_hash', 'slots'], how='left')

# Calculate the gap between demand and picked requests
df_merged['gap'] = df_merged['demand'] - df_merged['picked']

# Read the cluster map data
clusters_df = pd.read_csv('cluster_map/cluster_map', sep='\t')
clusters_df.columns = ['start_region_hash', 'region_id']

# Merge with cluster map data
final_df = pd.merge(df_merged, clusters_df, on='start_region_hash')

# Extract input features and target variable
X = final_df[['region_id', 'slots']]
y = final_df['gap']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model on the test set
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

# Log the metrics and the model using MLflow
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("RideEz Mlflow Experiment")

with mlflow.start_run(run_name="RideEz model example"):
    mlflow.sklearn.autolog()
    mlflow.log_metric("test_mse", mse)
    mlflow.sklearn.log_model(model, "model")
