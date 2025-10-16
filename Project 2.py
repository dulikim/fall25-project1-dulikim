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


# ==================================================
# CALCULATION 1: calculate_avg_yield_by_weather()
# ==================================================
def calculate_avg_yield_by_weather(crop_data, weather_condition):
    """
    Calculates average yield per region for a given weather condition.
    Uses Region (categorical), Weather_Condition (categorical), and 
    Yield_tons_per_hectare (numerical).
    
    Addresses question: "Which region has the highest average yield under 
    sunny conditions?"
    
    INPUT: crop_data (list of dicts), weather_condition (string)
    OUTPUT: dict with regions and their average yields
    """
    region_yield = defaultdict(list)
    
    for row in crop_data:
        if row["Weather_Condition"].lower() == weather_condition.lower():
            region_yield[row["Region"]].append(row["Yield_tons_per_hectare"])

    avg_yield_by_region = {
        region: round(sum(vals) / len(vals), 2) 
        for region, vals in region_yield.items() 
        if vals
    }
    
    return avg_yield_by_region



# ==================================================
# CALCULATION 2: compare_irrigation_fertilizer_effect()
# ==================================================
def compare_irrigation_fertilizer_effect(crop_data):
    """
    Analyzes average yields for four categories based on irrigation and 
    fertilizer usage.
    Uses Irrigation_Used (categorical), Fertilizer_Used (categorical), and 
    Yield_tons_per_hectare (numerical).
    
    Addresses question: "Do crops that use both irrigation and fertilizer 
    produce higher yields than those that use neither?"
    
    INPUT: crop_data (list of dicts)
    OUTPUT: dict with four categories and their average yields
    """
    categories = {
        "Both": [], 
        "Only_Irrigation": [], 
        "Only_Fertilizer": [], 
        "Neither": []
    }

    for row in crop_data:
        # Safely handle both string and boolean types
        irr_val = row["Irrigation_Used"]
        fert_val = row["Fertilizer_Used"]

        # Normalize to boolean
        if isinstance(irr_val, str):
            irr = irr_val.strip().lower() == "yes"
        else:
            irr = bool(irr_val)

        if isinstance(fert_val, str):
            fert = fert_val.strip().lower() == "yes"
        else:
            fert = bool(fert_val)

        # Categorize yields
        if irr and fert:
            categories["Both"].append(row["Yield_tons_per_hectare"])
        elif irr and not fert:
            categories["Only_Irrigation"].append(row["Yield_tons_per_hectare"])
        elif fert and not irr:
            categories["Only_Fertilizer"].append(row["Yield_tons_per_hectare"])
        else:
            categories["Neither"].append(row["Yield_tons_per_hectare"])

    # Compute averages safely
    yield_comparison = {
        key: round(sum(vals) / len(vals), 2) if vals else 0
        for key, vals in categories.items()
    }

    return yield_comparison

