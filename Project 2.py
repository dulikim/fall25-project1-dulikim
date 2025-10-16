"""
Name: Duli Kim
Student ID: [Your ID]
Email: [Your Email]
Dataset: Agriculture Crop Yield
Collaborators: None (solo project)
AI Tools: ChatGPT (for structure + debugging)
"""

# Required Libraries
import kagglehub
from kagglehub import KaggleDatasetAdapter
import csv
from collections import defaultdict

# load_crop_data()
def load_crop_data():
    """
    Loads the Agriculture Crop Yield dataset directly from Kaggle using kagglehub.
    Converts it to a list of dictionaries for processing.
    Converts numeric columns to appropriate data types.
    
    INPUT: None
    OUTPUT: list of dictionaries with properly typed numeric values
    """
    print("Loading dataset from Kaggle...")

    file_path = "crop_yield.csv"

    df = kagglehub.load_dataset(
        KaggleDatasetAdapter.PANDAS,
        "samuelotiattakorah/agriculture-crop-yield",
        file_path
    )

    print("✅ Dataset loaded successfully with", len(df), "records")

    # Convert numeric columns to proper types
    df["Rainfall_mm"] = df["Rainfall_mm"].astype(float)
    df["Temperature_Celsius"] = df["Temperature_Celsius"].astype(float)
    df["Yield_tons_per_hectare"] = df["Yield_tons_per_hectare"].astype(float)
    df["Days_to_Harvest"] = df["Days_to_Harvest"].astype(int)

    return df.to_dict(orient="records")
