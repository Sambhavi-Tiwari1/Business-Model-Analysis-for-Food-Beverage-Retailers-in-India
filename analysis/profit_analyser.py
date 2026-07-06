"""
Profitability Analysis for F&B Retail
"""
import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

class ProfitabilityAnalyzer:
    """
    Analyze profitability drivers and optimization opportunities
    """
    
    def __init__(self):
        self.benchmarks = {
            'food_cost': 0.32,
            'labor_cost': 0.22,
            'rent_cost': 0.12,
            'marketing_cost': 0.05,
            'utilities': 0.04,
            'technology': 0.03,
            'others': 0.22
        }
    
    def analyze(self, market_data: pd.DataFrame, consumer_data: pd.DataFrame) -> Dict:
        """Complete profitability analysis"""
        
        # Calculate profit metrics
        profit_metrics = self._calculate_profit_metrics()
        
        # Analyze pricing strategy
        pricing_analysis = self._analyze_pricing_strategy(consumer_data)
        
        # Analyze inventory management
        inventory_analysis = self._analyze_inventory_management()
        
        # Location profitability
        location_profitability = self._analyze_location_profitability()
        
        # Operational efficiency
        operational_efficiency = self._analyze_operational_efficiency()
        
        return {
            'profit_metrics': profit_metrics,
            'pricing_analysis': pricing_analysis,
            'inventory_analysis': inventory_analysis,
            'location_profitability': location_profitability,
            'operational_efficiency': operational_efficiency,
            'optimization_opportunities': self._identify_optimization_opportunities(
                profit_metrics, pricing_analysis, inventory_analysis
            ),
            'avg_profit_margin': profit_metrics['net_profit_margin']
        }
    
    def _calculate_profit_metrics(self) -> Dict:
        """Calculate key profit metrics"""
        
        # Revenue assumptions
        avg_revenue = 100  # Base number for percentage calculations
        
        # Cost structure
        costs = self.benchmarks
        total_cost = sum(costs.values())
        
        # Calculate metrics
        gross_profit = avg_revenue * (1 - costs['food_cost'])
        operating_profit = avg_revenue * (1 - total_cost)
        net_profit = operating_profit * 0.8  # 20% tax estimate
        
        return {
            'gross_profit_margin': (gross_profit / avg_revenue) * 100,
            'operating_profit_margin': (operating_profit / avg_revenue) * 100,
            'net_profit_margin': (net_profit / avg_revenue) * 100,
            'cost_breakdown': {k: v * 100 for k, v in costs.items()},
            'total_cost_percentage': total_cost * 100
        }
    
    def _analyze_pricing_strategy(self, consumer_data: pd.DataFrame) -> Dict:
        """Analyze pricing strategy and optimization"""
        
        # Price points based on consumer segments
        price_segments = {
            'value': {'range': (100, 300), 'market_share': 0.3},
            'mid': {'range': (300, 600), 'market_share': 0.5},
            'premium': {'range': (600, 1200), 'market_share': 0.2}
        }
        
        # Consumer willingness to pay
        if not consumer_data.empty:
            avg_spending = consumer_data['spending_per_visit'].mean()
            price_elasticity = -0.5  # 1% price increase = 0.5% demand decrease
        else:
            avg_spending = 500
            price_elasticity = -0.5
        
        return {
            'avg_spending': avg_spending,
            'price_segments': price_segments,
            'price_elasticity': price_elasticity,
            'optimal_price_point': avg_spending,
            'price_recommendations': [
                'Implement tiered pricing based on time of day',
                'Create combo offers for higher perceived value',
                'Introduce premium items for higher margins',
                'Offer loyalty discounts for repeat customers'
            ],
            'revenue_impact': {
                'price_increase_10pct': f"{(10 * price_elasticity):.1f}% demand decrease",
                'price_decrease_10pct': f"{(-10 * price_elasticity):.1f}% demand increase"
            }
        }
    
    def _analyze_inventory_management(self) -> Dict:
        """Analyze inventory management efficiency"""
        
        # Inventory metrics
        inventory_metrics = {
            'inventory_turnover': 4.5,  # Times per month
            'waste_percentage': 0.08,   # 8% waste
            'stockout_rate': 0.05,      # 5% stockouts
            'holding_cost_percentage': 0.15  # 15% of inventory value
        }
        
        # Improvement opportunities
        optimization = {
            'waste_reduction_potential': '20-30%',
            'turnover_improvement': '10-20%',
            'stockout_reduction': '50%'
        }
        
        return {
            'metrics': inventory_metrics,
            'optimization': optimization,
            'recommendations': [
                'Implement AI-based demand forecasting',
                'Adopt FIFO inventory management',
                'Use data analytics for menu optimization',
                'Develop supplier relationships for just-in-time delivery',
                'Monitor and analyze waste patterns'
            ],
            'cost_savings_opportunity': {
                'waste_reduction': '5-8% of food cost',
                'turnover_improvement': '3-5% reduction in holding costs',
                'stockout_reduction': '2-3% increase in sales'
            }
        }
    
    def _analyze_location_profitability(self) -> Dict:
        """Analyze location profitability factors"""
        
        location_types = {
            'high_street': {
                'foot_traffic': 0.9,
                'rent_cost': 0.20,
                'profit_margin': 0.12,
                'risk': 'High'
            },
            'mall': {
                'foot_traffic': 0.8,
                'rent_cost': 0.15,
                'profit_margin': 0.18,
                'risk': 'Medium'
            },
            'residential': {
                'foot_traffic': 0.5,
                'rent_cost': 0.08,
                'profit_margin': 0.20,
                'risk': 'Low'
            },
            'office_district': {
                'foot_traffic': 0.8,
                'rent_cost': 0.12,
                'profit_margin': 0.22,
                'risk': 'Medium'
            },
            'food_court': {
                'foot_traffic': 0.7,
                'rent_cost': 0.10,
                'profit_margin': 0.25,
                'risk': 'Low'
            }
        }
        
        # Calculate profitability score
        for location, data in location_types.items():
            data['profitability_score'] = (
                data['foot_traffic'] * 0.4 +
                (1 - data['rent_cost']) * 0.3 +
                data['profit_margin'] * 0.3
            ) * 100
        
        return {
            'location_types': location_types,
            'recommended_locations': sorted(
                location_types.items(),
                key=lambda x: x[1]['profitability_score'],
                reverse=True
            )[:3],
            'location_strategy': {
                'primary': 'office_district',
                'secondary': 'food_court',
                'tertiary': 'residential'
            }
        }
    
    def _analyze_operational_efficiency(self) -> Dict:
        """Analyze operational efficiency"""
        
        efficiency_metrics = {
            'table_turnover': {
                'current': 2.5,  # Times per day
                'target': 3.5,
                'improvement': '40%'
            },
            'staff_productivity': {
                'customers_per_staff': 15,
                'target': 20,
                'improvement': '33%'
            },
            'order_accuracy': {
                'current': 0.92,
                'target': 0.98,
                'improvement': '6.5%'
            }
        }
        
        return {
            'metrics': efficiency_metrics,
            'improvement_opportunities': [
                'Implement table management system',
                'Provide staff training programs',
                'Use technology for order accuracy',
                'Optimize kitchen workflow',
                'Implement performance tracking'
            ],
            'impact_on_profitability': {
                'table_turnover_impact': '15-20% revenue increase',
                'staff_productivity_impact': '10-15% cost reduction',
                'order_accuracy_impact': '5-8% customer satisfaction increase'
            }
        }
    
    def _identify_optimization_opportunities(self, profit_metrics: Dict,
                                            pricing_analysis: Dict,
                                            inventory_analysis: Dict) -> List:
        """Identify key optimization opportunities"""
        
        opportunities = []
        
        # Cost optimization
        if profit_metrics['net_profit_margin'] < 15:
            opportunities.append({
                'area': 'Cost Optimization',
                'opportunity': 'Reduce food and labor costs',
                'potential_impact': '3-5% margin improvement',
                'priority': 'High'
            })
        
        # Pricing optimization
        if pricing_analysis.get('price_elasticity', 0) < -0.3:
            opportunities.append({
                'area': 'Pricing Strategy',
                'opportunity': 'Implement value-based pricing',
                'potential_impact': '5-8% revenue increase',
                'priority': 'Medium'
            })
        
        # Inventory optimization
        if inventory_analysis['metrics']['waste_percentage'] > 0.05:
            opportunities.append({
                'area': 'Inventory Management',
                'opportunity': 'Reduce food waste through better forecasting',
                'potential_impact': '20-30% waste reduction',
                'priority': 'High'
            })
        
        return opportunities
