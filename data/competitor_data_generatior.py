"""
Competitor data generator for F&B retail analysis
"""
import numpy as np
import pandas as pd
import logging
import random
from datetime import datetime

logger = logging.getLogger(__name__)

class CompetitorDataGenerator:
    """
    Generate synthetic competitor data for F&B retail
    """
    
    def __init__(self, seed: int = 42):
        np.random.seed(seed)
        random.seed(seed)
        
        self.competitor_names = [
            "Taj Sats", "Aamby Valley", "The Leela", "ITC Hotels",
            "Oberoi Hotels", "Radisson", "Marriott", "Hilton",
            "Dominos", "KFC", "McDonalds", "Pizza Hut",
            "Burger King", "Subway", "Starbucks", "Cafe Coffee Day",
            "Barista", "Theobroma", "Chaayos", "Sagar Ratna",
            "Bikanervala", "Haldiram", "Paratha Wala", "The Dosa Plaza"
        ]
        
        self.cities = ["Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai", "Kolkata", "Pune"]
        self.segments = ["QSR", "Casual Dining", "Fine Dining", "Cloud Kitchens", "Cafe", "Delivery Only"]
        
    def generate_competitor_data(self) -> pd.DataFrame:
        """
        Generate comprehensive competitor data
        
        Returns:
            DataFrame with competitor information
        """
        data = []
        
        for i, name in enumerate(self.competitor_names[:20]):
            segment = random.choice(self.segments)
            city = random.choice(self.cities)
            
            # Financial metrics
            annual_revenue = random.randint(50, 500) * 10  # In lakhs
            market_share = random.uniform(0.01, 0.15)
            growth_rate = random.uniform(-0.05, 0.25)
            
            # Operational metrics
            num_locations = random.randint(1, 50)
            avg_check_size = random.randint(300, 1500)
            table_turnover = random.uniform(1.5, 4.0)
            occupancy_rate = random.uniform(0.5, 0.9)
            
            # Customer metrics
            customer_rating = round(random.uniform(3.0, 4.8), 1)
            avg_reviews = random.randint(100, 5000)
            repeat_customer_rate = random.uniform(0.2, 0.7)
            
            # Marketing metrics
            marketing_spend = annual_revenue * random.uniform(0.02, 0.08)
            digital_presence_score = random.uniform(0.3, 0.9)
            social_media_followers = random.randint(1000, 100000)
            
            competitor = {
                "competitor_id": f"COMP{str(i+1).zfill(3)}",
                "competitor_name": name,
                "segment": segment,
                "city": city,
                "annual_revenue_lakhs": annual_revenue,
                "market_share": round(market_share * 100, 2),
                "growth_rate": round(growth_rate * 100, 2),
                "num_locations": num_locations,
                "avg_check_size": avg_check_size,
                "table_turnover": round(table_turnover, 1),
                "occupancy_rate": round(occupancy_rate * 100, 1),
                "customer_rating": customer_rating,
                "avg_reviews": avg_reviews,
                "repeat_customer_rate": round(repeat_customer_rate * 100, 1),
                "marketing_spend_lakhs": round(marketing_spend, 2),
                "digital_presence_score": round(digital_presence_score * 10, 1),
                "social_media_followers": social_media_followers,
                "delivery_partners": ", ".join(random.sample(["Swiggy", "Zomato", "UberEats", "Amazon"], k=random.randint(1, 3))),
                "has_loyalty_program": random.choice([True, False]),
                "has_mobile_app": random.choice([True, False]),
                "cloud_kitchen": random.choice([True, False]) if segment in ["Cloud Kitchens", "Delivery Only"] else False,
                "organic_certified": random.choice([True, False]),
                "sustainability_rating": random.choice(["A", "B", "C", "D"]),
                "entry_year": random.randint(2010, 2023),
                "cuisine_specialization": ", ".join(random.sample(
                    ["North Indian", "South Indian", "Chinese", "Continental", "Italian", "Mexican", "Japanese"],
                    k=random.randint(1, 3)
                ))
            }
            
            data.append(competitor)
        
        df = pd.DataFrame(data)
        
        # Add derived metrics
        df['revenue_per_location'] = df['annual_revenue_lakhs'] / df['num_locations']
        df['market_share_category'] = pd.cut(
            df['market_share'],
            bins=[0, 2, 5, 10, 30],
            labels=["Low", "Medium", "High", "Very High"]
        )
        df['competitive_score'] = (
            df['market_share'] * 0.3 +
            df['customer_rating'] * 20 * 0.2 +
            df['digital_presence_score'] * 10 * 0.2 +
            df['num_locations'] * 0.1 +
            df['growth_rate'] * 0.2
        )
        
        logger.info(f"Generated {len(df)} competitor records")
        return df
    
    def generate_market_positioning(self) -> pd.DataFrame:
        """
        Generate market positioning data for competitors
        
        Returns:
            DataFrame with positioning data
        """
        positioning_data = []
        
        for i in range(15):
            competitor = {
                "brand": random.choice(self.competitor_names[:15]),
                "price_positioning": round(random.uniform(1, 10), 1),  # 1=Budget, 10=Premium
                "quality_perception": round(random.uniform(1, 10), 1),
                "service_quality": round(random.uniform(1, 10), 1),
                "ambiance": round(random.uniform(1, 10), 1),
                "convenience": round(random.uniform(1, 10), 1),
                "brand_awareness": round(random.uniform(1, 10), 1),
                "customer_loyalty": round(random.uniform(1, 10), 1),
                "innovation": round(random.uniform(1, 10), 1),
                "digital_capability": round(random.uniform(1, 10), 1),
                "sustainability": round(random.uniform(1, 10), 1),
                "overall_score": 0  # Will be calculated
            }
            
            # Calculate overall score
            competitor['overall_score'] = sum([
                competitor['quality_perception'] * 0.25,
                competitor['service_quality'] * 0.15,
                competitor['brand_awareness'] * 0.15,
                competitor['convenience'] * 0.15,
                competitor['ambiance'] * 0.1,
                competitor['digital_capability'] * 0.1,
                competitor['innovation'] * 0.05,
                competitor['sustainability'] * 0.05
            ])
            
            competitor['overall_score'] = round(competitor['overall_score'], 1)
            positioning_data.append(competitor)
        
        df = pd.DataFrame(positioning_data)
        logger.info(f"Generated {len(df)} market positioning records")
        return df
    
    def generate_expansion_data(self) -> pd.DataFrame:
        """
        Generate expansion and growth data for competitors
        
        Returns:
            DataFrame with expansion data
        """
        expansion_data = []
        
        for i in range(30):
            year = random.randint(2018, 2024)
            city = random.choice(self.cities)
            brand = random.choice(self.competitor_names[:15])
            
            expansion = {
                "expansion_id": f"EXP{str(i+1).zfill(3)}",
                "brand": brand,
                "year": year,
                "city": city,
                "new_locations": random.randint(1, 5),
                "investment_lakhs": random.randint(50, 500),
                "expected_roi": round(random.uniform(0.15, 0.40), 2),
                "segment": random.choice(self.segments),
                "market_potential": random.choice(["High", "Medium", "Low"]),
                "competitive_intensity": random.choice(["High", "Medium", "Low"]),
                "success_likelihood": random.choice(["Very High", "High", "Medium"]),
                "strategy_type": random.choice(["Organic", "Franchise", "Acquisition"])
            }
            
            expansion_data.append(expansion)
        
        df = pd.DataFrame(expansion_data)
        logger.info(f"Generated {len(df)} expansion records")
        return df
