"""
Business Model Framework Analyzer
"""
import pandas as pd
import numpy as np
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class BusinessModelAnalyzer:
    """
    Analyze and develop business model framework for F&B retail
    """
    
    def __init__(self):
        self.revenue_streams = {
            'dine_in': {'share': 0.45, 'growth': 0.08, 'margin': 0.25},
            'delivery': {'share': 0.30, 'growth': 0.18, 'margin': 0.15},
            'catering': {'share': 0.15, 'growth': 0.12, 'margin': 0.30},
            'merchandise': {'share': 0.05, 'growth': 0.15, 'margin': 0.40},
            'loyalty': {'share': 0.03, 'growth': 0.20, 'margin': 0.35},
            'others': {'share': 0.02, 'growth': 0.10, 'margin': 0.20}
        }
        
        self.cost_structure = {
            'food_cost': 0.32,
            'labor_cost': 0.22,
            'rent_cost': 0.12,
            'marketing_cost': 0.05,
            'utilities': 0.04,
            'technology': 0.03,
            'others': 0.22
        }
    
    def analyze(self, market_data: pd.DataFrame, competitor_data: pd.DataFrame) -> Dict:
        """Complete business model analysis"""
        
        # Revenue model analysis
        revenue_analysis = self._analyze_revenue_streams()
        
        # Cost structure analysis
        cost_analysis = self._analyze_cost_structure()
        
        # Value proposition
        value_proposition = self._analyze_value_proposition(market_data)
        
        # Key success factors
        key_success_factors = self._identify_success_factors(competitor_data)
        
        return {
            'revenue_streams': revenue_analysis,
            'cost_structure': cost_analysis,
            'value_proposition': value_proposition,
            'success_factors': key_success_factors,
            'model_summary': self._generate_summary(
                revenue_analysis, cost_analysis, value_proposition
            )
        }
    
    def _analyze_revenue_streams(self) -> Dict:
        """Analyze revenue streams"""
        analysis = {}
        
        total_revenue = sum(v['share'] for v in self.revenue_streams.values())
        
        for stream, data in self.revenue_streams.items():
            analysis[stream] = {
                'share': data['share'] * 100,
                'growth_rate': data['growth'] * 100,
                'margin': data['margin'] * 100,
                'contribution_to_profit': data['share'] * data['margin'] / total_revenue * 100,
                'priority': 'High' if data['share'] > 0.20 else 'Medium' if data['share'] > 0.10 else 'Low'
            }
        
        return analysis
    
    def _analyze_cost_structure(self) -> Dict:
        """Analyze cost structure"""
        analysis = {
            'breakdown': self.cost_structure,
            'total_cost': sum(self.cost_structure.values()),
            'optimization_opportunities': {}
        }
        
        # Identify optimization opportunities
        for cost, percentage in self.cost_structure.items():
            if percentage > 0.20:
                analysis['optimization_opportunities'][cost] = {
                    'current': percentage * 100,
                    'potential': (percentage * 0.85) * 100,  # 15% reduction potential
                    'savings': (percentage * 0.15) * 100,
                    'priority': 'High'
                }
            elif percentage > 0.10:
                analysis['optimization_opportunities'][cost] = {
                    'current': percentage * 100,
                    'potential': (percentage * 0.90) * 100,
                    'savings': (percentage * 0.10) * 100,
                    'priority': 'Medium'
                }
        
        return analysis
    
    def _analyze_value_proposition(self, market_data: pd.DataFrame) -> Dict:
        """Analyze value proposition"""
        value_proposition = {
            'unique_selling_points': [
                'Quality consistency across locations',
                'Innovative menu offerings',
                'Superior customer experience',
                'Convenient ordering options',
                'Value for money'
            ],
            'competitive_advantages': [
                'Strong brand recognition',
                'Efficient supply chain',
                'Technology integration',
                'Customer loyalty',
                'Location strategy'
            ],
            'target_segments': [
                'Working professionals - quick meals',
                'Families - weekend dining',
                'Students - budget options',
                'Couples - experience dining',
                'Corporates - events/catering'
            ]
        }
        
        # Add market-specific insights
        if not market_data.empty:
            top_segments = market_data.groupby('segment')['market_size_bn'].sum().nlargest(3)
            value_proposition['high_potential_segments'] = top_segments.index.tolist()
        
        return value_proposition
    
    def _identify_success_factors(self, competitor_data: pd.DataFrame) -> List:
        """Identify key success factors"""
        success_factors = [
            {
                'factor': 'Location Strategy',
                'importance': 0.85,
                'description': 'High foot traffic areas with target demographic'
            },
            {
                'factor': 'Quality Consistency',
                'importance': 0.90,
                'description': 'Standardized recipes and training'
            },
            {
                'factor': 'Pricing Optimization',
                'importance': 0.80,
                'description': 'Competitive pricing with value perception'
            },
            {
                'factor': 'Customer Experience',
                'importance': 0.75,
                'description': 'Ambiance, service, and overall experience'
            },
            {
                'factor': 'Supply Chain Efficiency',
                'importance': 0.70,
                'description': 'Cost-effective sourcing and inventory management'
            },
            {
                'factor': 'Technology Integration',
                'importance': 0.65,
                'description': 'Digital ordering, loyalty apps, analytics'
            }
        ]
        
        # Adjust based on competitor data
        if not competitor_data.empty:
            avg_market_share = competitor_data['market_share'].mean()
            success_factors.append({
                'factor': 'Market Positioning',
                'importance': 0.75,
                'description': f'Differentiation in competitive landscape (avg share: {avg_market_share:.1f}%)'
            })
        
        return sorted(success_factors, key=lambda x: x['importance'], reverse=True)
    
    def _generate_summary(self, revenue_analysis: Dict, cost_analysis: Dict,
                         value_proposition: Dict) -> Dict:
        """Generate business model summary"""
        summary = {
            'business_model_type': 'Hybrid (Dine-in + Delivery)',
            'key_revenue_stream': max(revenue_analysis.items(), 
                                    key=lambda x: x[1]['share'])[0],
            'key_cost_driver': max(cost_analysis['breakdown'].items(),
                                  key=lambda x: x[1])[0],
            'profit_potential': 'High' if revenue_analysis['dine_in']['margin'] > 20 else 'Medium',
            'competitive_advantage': 'Strong' if len(value_proposition['competitive_advantages']) > 3 else 'Medium'
        }
        
        return summary
