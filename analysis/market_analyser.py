"""
Market analysis for F&B retail sector
"""
import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

class MarketAnalyzer:
    """
    Analyze market trends, growth, and opportunities
    """
    
    def __init__(self):
        self.segments = ["QSR", "Casual Dining", "Fine Dining", "Cloud Kitchens", "Street Food"]
        
    def calculate_growth_rate(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate year-over-year growth rates"""
        data = data.copy()
        data['yoy_growth'] = data.groupby('segment')['market_size_bn'].pct_change() * 100
        return data
    
    def get_market_share_trends(self, data: pd.DataFrame) -> Dict:
        """Analyze market share trends"""
        trends = {}
        for segment in self.segments:
            segment_data = data[data['segment'] == segment]
            if not segment_data.empty:
                trends[segment] = {
                    'current_share': segment_data.iloc[-1]['segment_share'],
                    'growth_5y': segment_data['segment_share'].pct_change().sum(),
                    'avg_share': segment_data['segment_share'].mean()
                }
        return trends
    
    def identify_high_potential_segments(self, data: pd.DataFrame) -> List:
        """Identify high potential segments"""
        segment_growth = data.groupby('segment')['market_size_bn'].mean()
        segment_growth_rate = data.groupby('segment')['growth_rate'].mean()
        
        high_potential = []
        for segment in self.segments:
            score = segment_growth_rate.get(segment, 0) * 0.6 + \
                    segment_growth.get(segment, 0) * 0.4
            high_potential.append({
                'segment': segment,
                'growth_rate': segment_growth_rate.get(segment, 0),
                'market_size': segment_growth.get(segment, 0),
                'potential_score': score
            })
        
        return sorted(high_potential, key=lambda x: x['potential_score'], reverse=True)
