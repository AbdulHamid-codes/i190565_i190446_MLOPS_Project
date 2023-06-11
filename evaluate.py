import mlflow
from sklearn.metrics import mean_squared_error
import pandas as pd

# Load the trained model
model_uri = "models:/model"
model = mlflow.sklearn.load_model(model_uri)

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

# Predict on the data using the trained model
y_pred = model.predict(X)

# Calculate the mean squared error
mse = mean_squared_error(y, y_pred)

# Log the MSE
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("RideEz Mlflow Experiment")

with mlflow.start_run(run_name="RideEz model evaluation"):
    mlflow.log_metric("mse", mse)
