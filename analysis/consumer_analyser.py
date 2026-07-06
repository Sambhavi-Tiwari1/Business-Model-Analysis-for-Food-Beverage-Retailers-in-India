"""
Consumer Behavior Analysis for F&B Retail
"""
import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple
from collections import Counter

logger = logging.getLogger(__name__)

class ConsumerAnalyzer:
    """
    Analyze consumer preferences, behavior, and segmentation
    """
    
    def __init__(self):
        self.cuisine_categories = [
            "North Indian", "South Indian", "Chinese", "Continental",
            "Street Food", "Beverages", "Desserts"
        ]
    
    def analyze(self, consumer_data: pd.DataFrame) -> Dict:
        """Complete consumer behavior analysis"""
        
        if consumer_data.empty:
            return self._generate_sample_analysis()
        
        # Demographic analysis
        demographic_insights = self._analyze_demographics(consumer_data)
        
        # Preference analysis
        preference_insights = self._analyze_preferences(consumer_data)
        
        # Behavioral segmentation
        behavioral_segments = self._segment_consumers(consumer_data)
        
        # High potential segments
        high_potential = self._identify_high_potential_segments(consumer_data)
        
        # Spending patterns
        spending_patterns = self._analyze_spending_patterns(consumer_data)
        
        return {
            'demographic_insights': demographic_insights,
            'preference_insights': preference_insights,
            'behavioral_segments': behavioral_segments,
            'high_potential_segments': high_potential,
            'spending_patterns': spending_patterns,
            'avg_spending': consumer_data['spending_per_visit'].mean(),
            'top_segments': [s['name'] for s in high_potential[:3]]
        }
    
    def _generate_sample_analysis(self) -> Dict:
        """Generate sample analysis when no data available"""
        return {
            'demographic_insights': {
                'primary_age_group': '26-35',
                'primary_income': 'Medium',
                'urban_vs_rural': '75% Urban'
            },
            'preference_insights': {
                'top_cuisines': ['North Indian', 'Chinese', 'South Indian'],
                'preferred_channels': ['Dine-in', 'Delivery'],
                'avg_spending': '₹500-800'
            },
            'behavioral_segments': {
                'working_professionals': 'High frequency, medium spend',
                'families': 'Medium frequency, high spend',
                'students': 'High frequency, low spend'
            },
            'high_potential_segments': [
                {'name': 'Working Professionals', 'potential': 'High'},
                {'name': 'Families', 'potential': 'Very High'},
                {'name': 'Students', 'potential': 'High'}
            ],
            'spending_patterns': {
                'avg_spending': 650,
                'frequency': '2-3 times per week',
                'top_occasions': ['Weekend', 'Special Occasions']
            },
            'avg_spending': 650
        }
    
    def _analyze_demographics(self, data: pd.DataFrame) -> Dict:
        """Analyze demographic characteristics"""
        
        age_distribution = data['age_group'].value_counts().to_dict()
        income_distribution = data['income_level'].value_counts().to_dict()
        city_distribution = data['city'].value_counts().to_dict()
        
        return {
            'age_distribution': age_distribution,
            'income_distribution': income_distribution,
            'city_distribution': city_distribution,
            'primary_age_group': max(age_distribution.items(), key=lambda x: x[1])[0],
            'primary_income': max(income_distribution.items(), key=lambda x: x[1])[0],
            'top_cities': sorted(city_distribution.items(), key=lambda x: x[1], reverse=True)[:3]
        }
    
    def _analyze_preferences(self, data: pd.DataFrame) -> Dict:
        """Analyze consumer preferences"""
        
        # Top cuisines
        cuisine_counts = Counter()
        for cuisines in data['top_cuisines']:
            for cuisine in cuisines.split(', '):
                cuisine_counts[cuisine] += 1
        
        top_cuisines = cuisine_counts.most_common(5)
        
        # Preferred channels
        channel_counts = Counter()
        for channels in data['preferred_channels']:
            for channel in channels.split(', '):
                channel_counts[channel] += 1
        
        top_channels = channel_counts.most_common(3)
        
        return {
            'top_cuisines': [{'cuisine': c, 'count': count} for c, count in top_cuisines],
            'top_channels': [{'channel': c, 'count': count} for c, count in top_channels],
            'dietary_preferences': data['dietary_preference'].value_counts().to_dict(),
            'online_ordering_rate': data['online_ordering'].mean() * 100,
            'loyalty_membership_rate': data['loyalty_member'].mean() * 100
        }
    
    def _segment_consumers(self, data: pd.DataFrame) -> Dict:
        """Segment consumers based on behavior"""
        
        segments = {}
        
        # Working Professionals (High income, high frequency)
        professionals = data[
            (data['income_level'] == 'High') &
            (data['visit_frequency'].isin(['Daily', '2-3/Week']))
        ]
        segments['working_professionals'] = {
            'count': len(professionals),
            'percentage': len(professionals) / len(data) * 100,
            'avg_spending': professionals['spending_per_visit'].mean(),
            'primary_channel': 'Delivery' if professionals['online_ordering'].mean() > 0.5 else 'Dine-in',
            'characteristics': 'High frequency, medium-high spending, convenience-focused'
        }
        
        # Families (Medium-high income, weekend dining)
        families = data[
            (data['income_level'].isin(['Medium', 'High'])) &
            (data['visit_frequency'].isin(['Weekly']))
        ]
        segments['families'] = {
            'count': len(families),
            'percentage': len(families) / len(data) * 100,
            'avg_spending': families['spending_per_visit'].mean(),
            'primary_channel': 'Dine-in',
            'characteristics': 'Medium frequency, high spending, experience-focused'
        }
        
        # Students (Low-medium income, high frequency)
        students = data[
            (data['income_level'].isin(['Low', 'Medium'])) &
            (data['visit_frequency'].isin(['Daily', '2-3/Week']))
        ]
        segments['students'] = {
            'count': len(students),
            'percentage': len(students) / len(data) * 100,
            'avg_spending': students['spending_per_visit'].mean(),
            'primary_channel': 'Takeaway' if students['online_ordering'].mean() < 0.3 else 'Delivery',
            'characteristics': 'High frequency, low-medium spending, budget-conscious'
        }
        
        # Couples (Medium-high income, occasional dining)
        couples = data[
            (data['income_level'].isin(['Medium', 'High'])) &
            (data['visit_frequency'].isin(['Weekly', 'Monthly']))
        ]
        segments['couples'] = {
            'count': len(couples),
            'percentage': len(couples) / len(data) * 100,
            'avg_spending': couples['spending_per_visit'].mean(),
            'primary_channel': 'Dine-in',
            'characteristics': 'Low-medium frequency, medium-high spending, experience-focused'
        }
        
        return segments
    
    def _identify_high_potential_segments(self, data: pd.DataFrame) -> List:
        """Identify high potential customer segments"""
        
        segments = self._segment_consumers(data)
        
        high_potential = []
        
        for segment_name, segment_data in segments.items():
            if segment_data['count'] > 0:
                # Calculate potential score based on size, spending, and growth
                size_score = segment_data['percentage'] / 100
                spending_score = segment_data['avg_spending'] / data['spending_per_visit'].max()
                potential_score = (size_score * 0.4 + spending_score * 0.6)
                
                high_potential.append({
                    'name': segment_name.replace('_', ' ').title(),
                    'size': segment_data['count'],
                    'percentage': segment_data['percentage'],
                    'avg_spending': segment_data['avg_spending'],
                    'potential_score': potential_score * 100,
                    'recommended_strategy': self._get_segment_strategy(segment_name)
                })
        
        return sorted(high_potential, key=lambda x: x['potential_score'], reverse=True)
    
    def _get_segment_strategy(self, segment_name: str) -> str:
        """Get recommended strategy for segment"""
        strategies = {
            'working_professionals': 'Focus on speed and convenience with loyalty programs',
            'families': 'Create family-friendly atmosphere with value bundles',
            'students': 'Offer budget-friendly options and student discounts',
            'couples': 'Create romantic ambiance with premium offerings'
        }
        return strategies.get(segment_name, 'General engagement strategy')
    
    def _analyze_spending_patterns(self, data: pd.DataFrame) -> Dict:
        """Analyze consumer spending patterns"""
        
        # Frequency distribution
        frequency_counts = data['visit_frequency'].value_counts().to_dict()
        
        # Channel spending
        channel_spending = data.groupby('preferred_channels')['spending_per_visit'].mean()
        
        # Income vs spending
        income_spending = data.groupby('income_level')['spending_per_visit'].mean().to_dict()
        
        return {
            'frequency_distribution': frequency_counts,
            'channel_spending': channel_spending.to_dict(),
            'income_spending': income_spending,
            'avg_spending': data['spending_per_visit'].mean(),
            'max_spending': data['spending_per_visit'].max(),
            'min_spending': data['spending_per_visit'].min(),
            'top_occasions': ['Weekend', 'Special Occasions', 'Work Lunch', 'Family Dinner']
        }
