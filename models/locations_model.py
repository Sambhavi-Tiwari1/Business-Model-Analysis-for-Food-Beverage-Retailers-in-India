"""
Location optimization model for F&B retail
"""
import numpy as np
import pandas as pd
import logging
from typing import Dict, List, Tuple
from sklearn.preprocessing import MinMaxScaler

logger = logging.getLogger(__name__)

class LocationModel:
    """
    Location analysis and optimization for F&B retail
    """
    
    def __init__(self):
        self.location_weights = {
            'foot_traffic': 0.30,
            'demographics': 0.20,
            'competition': 0.15,
            'rent_cost': 0.15,
            'accessibility': 0.10,
            'visibility': 0.10
        }
        
        self.location_types = {
            'high_street': {
                'foot_traffic': 0.9,
                'demographics': 0.7,
                'competition': 0.3,
                'rent_cost': 0.2,
                'accessibility': 0.8,
                'visibility': 0.9
            },
            'mall': {
                'foot_traffic': 0.8,
                'demographics': 0.8,
                'competition': 0.4,
                'rent_cost': 0.3,
                'accessibility': 0.7,
                'visibility': 0.8
            },
            'residential': {
                'foot_traffic': 0.5,
                'demographics': 0.6,
                'competition': 0.7,
                'rent_cost': 0.7,
                'accessibility': 0.6,
                'visibility': 0.5
            },
            'office_district': {
                'foot_traffic': 0.8,
                'demographics': 0.7,
                'competition': 0.5,
                'rent_cost': 0.5,
                'accessibility': 0.8,
                'visibility': 0.7
            },
            'food_court': {
                'foot_traffic': 0.7,
                'demographics': 0.6,
                'competition': 0.3,
                'rent_cost': 0.6,
                'accessibility': 0.8,
                'visibility': 0.7
            }
        }
    
    def analyze(self, config: Dict) -> Dict:
        """
        Analyze and recommend optimal locations
        
        Args:
            config: Configuration dictionary
            
        Returns:
            Location analysis and recommendations
        """
        
        # Score each location type
        location_scores = {}
        
        for location_type, features in self.location_types.items():
            score = 0
            for feature, weight in self.location_weights.items():
                score += features.get(feature, 0) * weight
            
            location_scores[location_type] = {
                'score': round(score * 100, 1),
                'features': features,
                'recommendation': self._get_recommendation(location_type, score)
            }
        
        # Calculate potential metrics
        potential_metrics = self._calculate_potential_metrics(location_scores)
        
        # Generate location strategy
        strategy = self._generate_strategy(location_scores, potential_metrics)
        
        return {
            'location_scores': location_scores,
            'potential_metrics': potential_metrics,
            'strategy': strategy,
            'avg_score': round(np.mean([v['score'] for v in location_scores.values()]), 1),
            'top_locations': self._get_top_locations(location_scores)
        }
    
    def _get_recommendation(self, location_type: str, score: float) -> str:
        """Get recommendation based on location score"""
        if score > 0.7:
            return "Highly Recommended"
        elif score > 0.5:
            return "Recommended"
        elif score > 0.3:
            return "Consider with Caution"
        else:
            return "Not Recommended"
    
    def _calculate_potential_metrics(self, location_scores: Dict) -> Dict:
        """Calculate potential metrics for locations"""
        
        metrics = {}
        
        for location_type, data in location_scores.items():
            score = data['score'] / 100
            
            # Calculate estimated metrics
            estimated_revenue = 50 * score * 100  # In lakhs
            estimated_profit = estimated_revenue * 0.15  # 15% profit margin
            payback_period = 36 / score  # Months
            roi = (estimated_profit / 100) * 100  # ROI percentage
            
            metrics[location_type] = {
                'estimated_revenue_lakhs': round(estimated_revenue, 1),
                'estimated_profit_lakhs': round(estimated_profit, 1),
                'payback_period_months': round(payback_period, 1),
                'roi_percentage': round(roi, 1),
                'break_even_months': round(payback_period * 0.8, 1)
            }
        
        return metrics
    
    def _generate_strategy(self, location_scores: Dict, potential_metrics: Dict) -> Dict:
        """Generate location strategy"""
        
        # Sort locations by score
        sorted_locations = sorted(location_scores.items(), 
                                 key=lambda x: x[1]['score'], 
                                 reverse=True)
        
        return {
            'primary_location': sorted_locations[0][0] if sorted_locations else 'office_district',
            'secondary_location': sorted_locations[1][0] if len(sorted_locations) > 1 else 'food_court',
            'expansion_priority': [loc[0] for loc in sorted_locations[:3]],
            'strategy_summary': self._get_strategy_summary(sorted_locations),
            'investment_priority': 'High' if sorted_locations[0][1]['score'] > 70 else 'Medium'
        }
    
    def _get_strategy_summary(self, sorted_locations: List) -> str:
        """Get strategy summary"""
        top_location = sorted_locations[0]
        summary = f"Focus on {top_location[0]} locations with a score of {top_location[1]['score']:.1f}%. "
        
        if top_location[1]['score'] > 70:
            summary += "This is a high-potential location with strong foot traffic and demographics."
        elif top_location[1]['score'] > 50:
            summary += "This location shows good potential with balanced characteristics."
        else:
            summary += "Consider multiple smaller locations to test the market."
        
        return summary
    
    def _get_top_locations(self, location_scores: Dict) -> List:
        """Get top 3 recommended locations"""
        sorted_locations = sorted(location_scores.items(), 
                                 key=lambda x: x[1]['score'], 
                                 reverse=True)
        
        top_locations = []
        for location, data in sorted_locations[:3]:
            top_locations.append({
                'type': location,
                'score': data['score'],
                'recommendation': data['recommendation']
            })
        
        return top_locations
    
    def calculate_site_suitability(self, location_data: Dict) -> Dict:
        """
        Calculate site suitability score for a specific location
        
        Args:
            location_data: Dictionary with location attributes
            
        Returns:
            Site suitability analysis
        """
        # Required fields
        required_fields = ['foot_traffic', 'demographics', 'competition', 
                          'rent_cost', 'accessibility', 'visibility']
        
        # Calculate weighted score
        score = 0
        for field in required_fields:
            value = location_data.get(field, 0)
            weight = self.location_weights.get(field, 0)
            score += value * weight
        
        # Calculate additional metrics
        risk_score = 1 - score  # Higher risk for lower scores
        
        return {
            'suitability_score': round(score * 100, 1),
            'risk_level': 'Low' if score > 0.7 else 'Medium' if score > 0.5 else 'High',
            'estimated_monthly_rent': location_data.get('rent_cost', 0) * 50000,
            'estimated_footfall': location_data.get('foot_traffic', 0) * 1000,
            'competitive_advantage': 'High' if location_data.get('competition', 0) < 0.4 else 'Medium',
            'recommendations': self._get_site_recommendations(score, location_data)
        }
    
    def _get_site_recommendations(self, score: float, location_data: Dict) -> List:
        """Get site-specific recommendations"""
        recommendations = []
        
        if score < 0.5:
            recommendations.append("Consider negotiating lower rent")
            recommendations.append("Focus on marketing to build awareness")
        
        if location_data.get('foot_traffic', 0) < 0.5:
            recommendations.append("Implement strong local marketing campaign")
            recommendations.append("Consider partnerships with nearby businesses")
        
        if location_data.get('competition', 0) > 0.6:
            recommendations.append("Differentiate through unique menu or service")
            recommendations.append("Focus on customer experience and quality")
        
        if location_data.get('visibility', 0) < 0.5:
            recommendations.append("Invest in prominent signage")
            recommendations.append("Enhance storefront presence")
        
        if not recommendations:
            recommendations.append("Maintain current strategy and optimize operations")
        
        return recommendations
