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

# ==================================================
# CALCULATION 3: calculate_avg_rainfall_temperature()
# ==================================================
def calculate_avg_rainfall_temperature(crop_data):
    """
    Calculates average rainfall and temperature for each crop type.
    Uses Crop (categorical), Rainfall_mm (numerical), and 
    Temperature_Celsius (numerical).
    
    Addresses question: "What is the average rainfall and temperature for 
    each crop type?"
    
    INPUT: crop_data (list of dicts)
    OUTPUT: dict with crops and their avg rainfall and temperature
    """
    crop_info = defaultdict(lambda: {"rainfall": [], "temperature": []})
    
    for row in crop_data:
        crop_info[row["Crop"]]["rainfall"].append(row["Rainfall_mm"])
        crop_info[row["Crop"]]["temperature"].append(row["Temperature_Celsius"])

    crop_conditions = {
        crop: {
            "avg_rainfall": round(sum(vals["rainfall"]) / len(vals["rainfall"]), 2),
            "avg_temperature": round(sum(vals["temperature"]) / len(vals["temperature"]), 2)
        }
        for crop, vals in crop_info.items()
    }
    
    return crop_conditions


# ==================================================
# CALCULATION 4: calculate_yield_above_threshold()
# ==================================================
def calculate_yield_above_threshold(crop_data, threshold):
    """
    Calculates percentage of crops in each region with yield above a threshold.
    Uses Region (categorical), Yield_tons_per_hectare (numerical), and 
    Days_to_Harvest (numerical for context).
    
    Addresses question: "What percentage of harvest in each region has yield 
    above X tons per hectare?"
    
    INPUT: crop_data (list of dicts), threshold (float)
    OUTPUT: dict with regions and percentage of crops above threshold
    """
    region_stats = defaultdict(lambda: {"above": 0, "total": 0})
    
    for row in crop_data:
        region = row["Region"]
        yield_val = row["Yield_tons_per_hectare"]
        
        region_stats[region]["total"] += 1
        if yield_val > threshold:
            region_stats[region]["above"] += 1
    
    percentage_above = {
        region: round((stats["above"] / stats["total"]) * 100, 2) 
        if stats["total"] > 0 else 0
        for region, stats in region_stats.items()
    }
    
    return percentage_above

def generate_report(avg_yield_by_region, yield_comparison, crop_conditions, 
                   percentage_above, output_file):
    """
    Writes all calculation results to a CSV output file.
    
    INPUT: Four calculation results (dicts), output_file (string)
    OUTPUT: None (writes to file)
    """
    with open(output_file, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Calculation 1
        writer.writerow(["=== Average Yield by Region (Sunny Conditions) ==="])
        writer.writerow(["Region", "Avg Yield (tons/hectare)"])
        for region, val in sorted(avg_yield_by_region.items()):
            writer.writerow([region, val])

        writer.writerow([])
        
        # Calculation 2
        writer.writerow(["=== Yield Comparison: Irrigation vs Fertilizer ==="])
        writer.writerow(["Condition", "Avg Yield (tons/hectare)"])
        for condition, val in yield_comparison.items():
            writer.writerow([condition, val])

        writer.writerow([])
        
        # Calculation 3
        writer.writerow(["=== Avg Rainfall & Temperature by Crop ==="])
        writer.writerow(["Crop", "Avg Rainfall (mm)", "Avg Temperature (°C)"])
        for crop, stats in sorted(crop_conditions.items()):
            writer.writerow([crop, stats["avg_rainfall"], stats["avg_temperature"]])

        writer.writerow([])
        
        # Calculation 4
        writer.writerow(["=== Percentage of Yield Above 5 tons/hectare by Region ==="])
        writer.writerow(["Region", "Percentage (%)"])
        for region, pct in sorted(percentage_above.items()):
            writer.writerow([region, pct])

    print(f"📁 Report saved successfully as: {output_file}")
