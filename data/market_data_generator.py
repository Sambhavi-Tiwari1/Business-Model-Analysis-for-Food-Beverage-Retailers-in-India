"""
Market data generator for F&B retail analysis
"""
import numpy as np
import pandas as pd
import logging
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)

class MarketDataGenerator:
    """Generate synthetic market data for F&B retail sector"""
    
    def __init__(self, seed=42):
        np.random.seed(seed)
        random.seed(seed)
        
        self.cities = ["Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai", "Kolkata", "Pune"]
        self.segments = ["QSR", "Casual Dining", "Fine Dining", "Cloud Kitchens", "Street Food"]
        
    def generate_market_size_data(self, years=5):
        """Generate market size and growth data"""
        base_size = 100  # Base market size in billion INR
        data = []
        
        for year in range(2020, 2020 + years):
            growth = np.random.normal(0.12, 0.03)  # 12% avg growth
            size = base_size * (1 + growth) ** (year - 2020)
            
            for segment in self.segments:
                segment_share = {
                    "QSR": 0.45,
                    "Casual Dining": 0.30,
                    "Fine Dining": 0.10,
                    "Cloud Kitchens": 0.10,
                    "Street Food": 0.05
                }.get(segment, 0.10)
                
                segment_size = size * segment_share * np.random.uniform(0.9, 1.1)
                
                data.append({
                    "year": year,
                    "segment": segment,
                    "market_size_bn": round(segment_size, 1),
                    "growth_rate": round(growth * 100, 1),
                    "segment_share": round(segment_share * 100, 1)
                })
        
        return pd.DataFrame(data)
    
    def generate_consumer_preferences(self, n=1000):
        """Generate consumer preference data"""
        categories = [
            "North Indian", "South Indian", "Chinese", "Continental",
            "Street Food", "Beverages", "Desserts"
        ]
        
        data = []
        for i in range(n):
            age = random.choice(["18-25", "26-35", "36-45", "45+"])
            income = random.choice(["Low", "Medium", "High"])
            city = random.choice(self.cities)
            
            # Preferences based on demographic
            if age in ["18-25", "26-35"]:
                top_cuisines = random.sample(categories, 3)
            else:
                top_cuisines = random.sample(categories, 2)
            
            # Spending habits
            spending_per_visit = {
                "Low": random.randint(200, 500),
                "Medium": random.randint(500, 1000),
                "High": random.randint(1000, 2500)
            }[income]
            
            frequency = random.choice(["Daily", "2-3/Week", "Weekly", "Monthly"])
            
            channels = random.sample(["Dine-in", "Delivery", "Takeaway"], 
                                    random.randint(1, 2))
            
            data.append({
                "consumer_id": f"C{str(i+1).zfill(4)}",
                "age_group": age,
                "income_level": income,
                "city": city,
                "top_cuisines": ", ".join(top_cuisines),
                "spending_per_visit": spending_per_visit,
                "visit_frequency": frequency,
                "preferred_channels": ", ".join(channels),
                "dietary_preference": random.choice(["Veg", "Non-Veg", "Vegan"]),
                "online_ordering": random.choice([True, False]),
                "loyalty_member": random.choice([True, False])
            })
        
        return pd.DataFrame(data)
