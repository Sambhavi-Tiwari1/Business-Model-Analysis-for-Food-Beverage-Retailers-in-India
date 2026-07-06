"""
Consumer survey data generator for F&B retail analysis
"""
import numpy as np
import pandas as pd
import logging
import random
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ConsumerDataGenerator:
    """
    Generate synthetic consumer survey data for F&B retail
    """
    
    def __init__(self, seed: int = 42):
        np.random.seed(seed)
        random.seed(seed)
        
        self.cities = ["Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad"]
        self.age_groups = ["18-25", "26-35", "36-45", "46-55", "55+"]
        self.income_groups = ["Low", "Lower-Middle", "Middle", "Upper-Middle", "High"]
        self.occupations = ["Student", "Professional", "Entrepreneur", "Homemaker", "Retired", "Self-Employed"]
        self.cuisines = ["North Indian", "South Indian", "Chinese", "Continental", "Street Food", "Beverages", "Desserts"]
        self.dietary_preferences = ["Veg", "Non-Veg", "Vegan", "Gluten-Free", "Keto"]
        self.channels = ["Dine-in", "Delivery", "Takeaway"]
        self.frequency = ["Daily", "2-3/Week", "Weekly", "Monthly", "Occasionally"]
        
    def generate_consumer_preferences(self, n: int = 1000) -> pd.DataFrame:
        """
        Generate consumer preference data
        
        Args:
            n: Number of consumers to generate
            
        Returns:
            DataFrame with consumer preferences
        """
        data = []
        
        for i in range(n):
            # Demographics
            age = random.choice(self.age_groups)
            income = random.choice(self.income_groups)
            city = random.choice(self.cities)
            occupation = random.choice(self.occupations)
            
            # Lifestyle factors
            has_children = random.choice([True, False])
            works_from_home = random.choice([True, False]) if occupation in ["Professional", "Self-Employed", "Entrepreneur"] else False
            
            # Dining preferences
            top_cuisines = random.sample(self.cuisines, k=random.randint(2, 4))
            
            # Spending patterns based on income
            income_spending_map = {
                "Low": (100, 300),
                "Lower-Middle": (200, 500),
                "Middle": (400, 800),
                "Upper-Middle": (600, 1200),
                "High": (900, 2500)
            }
            spend_range = income_spending_map.get(income, (300, 800))
            spending_per_visit = random.randint(spend_range[0], spend_range[1])
            
            # Frequency based on occupation and income
            if occupation in ["Student", "Self-Employed"]:
                freq_weights = [0.2, 0.3, 0.25, 0.15, 0.1]
            elif occupation == "Professional":
                freq_weights = [0.15, 0.35, 0.25, 0.15, 0.1]
            else:
                freq_weights = [0.1, 0.2, 0.3, 0.25, 0.15]
            
            visit_frequency = random.choices(self.frequency, weights=freq_weights)[0]
            
            # Preferred channels
            num_channels = random.randint(1, 2)
            if visit_frequency in ["Daily", "2-3/Week"]:
                channels = random.choices(self.channels, weights=[0.3, 0.5, 0.2], k=num_channels)
            else:
                channels = random.choices(self.channels, weights=[0.5, 0.3, 0.2], k=num_channels)
            
            # Digital engagement
            online_ordering = random.choice([True, False])
            uses_swiggy_zomato = random.choice([True, False]) if online_ordering else False
            loyalty_member = random.choice([True, False])
            follows_social_media = random.choice([True, False])
            
            # Dining occasions
            dining_occasions = random.sample([
                "Weekend Dining", "Special Occasions", "Work Lunch", 
                "Family Dinner", "Date Night", "Quick Bite"
            ], k=random.randint(2, 4))
            
            # Health and sustainability consciousness
            health_conscious = random.choice([True, False])
            sustainability_focus = random.choice([True, False])
            reads_labels = random.choice([True, False])
            
            # Feedback and reviews
            leaves_reviews = random.choice([True, False]) if random.random() > 0.6 else False
            recommends_to_others = random.choice([True, False])
            
            # Brand preferences
            brands = random.sample([
                "Dominos", "KFC", "McDonalds", "Pizza Hut", "Taco Bell",
                "Burger King", "Subway", "Starbucks", "Cafe Coffee Day", "Barista"
            ], k=random.randint(2, 4))
            
            consumer = {
                "consumer_id": f"C{str(i+1).zfill(4)}",
                "age_group": age,
                "income_level": income,
                "city": city,
                "occupation": occupation,
                "has_children": has_children,
                "works_from_home": works_from_home,
                "top_cuisines": ", ".join(top_cuisines),
                "spending_per_visit": spending_per_visit,
                "visit_frequency": visit_frequency,
                "preferred_channels": ", ".join(set(channels)),
                "online_ordering": online_ordering,
                "uses_swiggy_zomato": uses_swiggy_zomato,
                "loyalty_member": loyalty_member,
                "follows_social_media": follows_social_media,
                "dining_occasions": ", ".join(dining_occasions),
                "dietary_preference": random.choice(self.dietary_preferences),
                "health_conscious": health_conscious,
                "sustainability_focus": sustainability_focus,
                "reads_labels": reads_labels,
                "leaves_reviews": leaves_reviews,
                "recommends_to_others": recommends_to_others,
                "preferred_brands": ", ".join(brands),
                "is_early_adopter": random.choice([True, False]),
                "monthly_dining_budget": round(random.randint(1000, 15000) / 100) * 100,
                "avg_rating_given": round(random.uniform(3.0, 5.0), 1),
                "willing_to_try_new": random.choice([True, False]),
                "prefers_healthy_options": random.choice([True, False])
            }
            
            data.append(consumer)
        
        df = pd.DataFrame(data)
        logger.info(f"Generated {len(df)} consumer records")
        return df
    
    def generate_survey_responses(self, n: int = 500) -> pd.DataFrame:
        """
        Generate survey responses for consumer behavior analysis
        
        Args:
            n: Number of survey responses
            
        Returns:
            DataFrame with survey responses
        """
        survey_data = []
        
        questions = {
            "price_sensitivity": {
                "1": "Only care about quality",
                "2": "Slightly price sensitive",
                "3": "Moderately price sensitive",
                "4": "Very price sensitive",
                "5": "Only care about price"
            },
            "quality_importance": {
                "1": "Not important",
                "2": "Slightly important",
                "3": "Moderately important",
                "4": "Very important",
                "5": "Extremely important"
            },
            "convenience_importance": {
                "1": "Not important",
                "2": "Slightly important",
                "3": "Moderately important",
                "4": "Very important",
                "5": "Extremely important"
            },
            "experience_importance": {
                "1": "Not important",
                "2": "Slightly important",
                "3": "Moderately important",
                "4": "Very important",
                "5": "Extremely important"
            },
            "brand_loyalty": {
                "1": "Always try new places",
                "2": "Prefer known brands",
                "3": "Mix of new and old",
                "4": "Highly loyal to favorites",
                "5": "Only visit specific brands"
            },
            "health_consciousness": {
                "1": "Not conscious",
                "2": "Slightly conscious",
                "3": "Moderately conscious",
                "4": "Very conscious",
                "5": "Extremely conscious"
            }
        }
        
        for i in range(n):
            response = {
                "response_id": f"R{str(i+1).zfill(4)}",
                "respondent_id": f"C{str(random.randint(1, 1000)).zfill(4)}"
            }
            
            # Random responses with biases
            for q, options in questions.items():
                # Add some bias based on demographics
                if q == "price_sensitivity":
                    weights = [0.1, 0.15, 0.3, 0.25, 0.2]
                elif q == "quality_importance":
                    weights = [0.05, 0.1, 0.2, 0.35, 0.3]
                elif q == "convenience_importance":
                    weights = [0.1, 0.15, 0.25, 0.3, 0.2]
                elif q == "experience_importance":
                    weights = [0.15, 0.2, 0.3, 0.2, 0.15]
                elif q == "brand_loyalty":
                    weights = [0.2, 0.25, 0.3, 0.15, 0.1]
                elif q == "health_consciousness":
                    weights = [0.2, 0.2, 0.25, 0.2, 0.15]
                else:
                    weights = [0.2] * 5
                
                response[q] = random.choices(list(options.keys()), weights=weights)[0]
            
            survey_data.append(response)
        
        df = pd.DataFrame(survey_data)
        logger.info(f"Generated {len(df)} survey responses")
        return df
    
    def generate_feedback_data(self, n: int = 300) -> pd.DataFrame:
        """
        Generate customer feedback and review data
        
        Args:
            n: Number of feedback entries
            
        Returns:
            DataFrame with feedback data
        """
        feedback_data = []
        
        restaurants = [
            "Taj Mahal Palace", "The Bombay Canteen", "Karavalli", "Bukhara",
            "Indian Accent", "Farzi Cafe", "Olive Bar & Kitchen", "SodaBottleOpenerwala",
            "The Rajdoot", "Swati Snacks", "Cafe Madras", "Mavalli Tiffin Room"
        ]
        
        feedback_templates = {
            "positive": [
                "Amazing food quality! The {dish} was exceptional.",
                "Great service and atmosphere. Will definitely visit again.",
                "Best {cuisine} in town. Highly recommend the {dish}.",
                "Loved the experience. Perfect for {occasion}.",
                "Excellent value for money. The portion sizes are generous."
            ],
            "neutral": [
                "Good food but service could be faster.",
                "Decent experience. Average pricing.",
                "Okay place. Would try again for different menu items.",
                "Standard quality. Nothing extraordinary but good.",
                "Ambiance is nice but food is average."
            ],
            "negative": [
                "Poor service. Had to wait too long.",
                "Food quality is declining. Used to be better.",
                "Overpriced for the portion size.",
                "Not as good as expected. Disappointed.",
                "Hygiene concerns. Needs improvement."
            ]
        }
        
        for i in range(n):
            restaurant = random.choice(restaurants)
            rating = random.choices([5, 4, 3, 2, 1], weights=[0.2, 0.3, 0.25, 0.15, 0.1])[0]
            
            if rating >= 4:
                sentiment = "positive"
            elif rating == 3:
                sentiment = "neutral"
            else:
                sentiment = "negative"
            
            template = random.choice(feedback_templates[sentiment])
            dish = random.choice(["butter chicken", "biryani", "pasta", "pizza", "sushi", "tacos", "burger"])
            cuisine = random.choice(self.cuisines)
            occasion = random.choice(["family dinner", "date night", "business meeting", "casual outing"])
            
            feedback = {
                "feedback_id": f"F{str(i+1).zfill(4)}",
                "restaurant": restaurant,
                "rating": rating,
                "review": template.format(dish=dish, cuisine=cuisine, occasion=occasion),
                "sentiment": sentiment,
                "date": datetime.now() - timedelta(days=random.randint(0, 365)),
                "would_recommend": random.choice([True, False]) if rating >= 3 else False,
                "dine_in": random.choice([True, False]),
                "cost_for_two": random.randint(500, 3000),
                "wait_time_minutes": random.randint(0, 60) if random.random() > 0.5 else None,
                "response_from_management": random.choice([True, False]) if random.random() > 0.6 else False
            }
            
            feedback_data.append(feedback)
        
        df = pd.DataFrame(feedback_data)
        logger.info(f"Generated {len(df)} feedback entries")
        return df
