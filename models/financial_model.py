"""
Financial modeling for F&B retail business
"""
import numpy as np
import pandas as pd
import logging
from typing import Dict, List, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class FinancialModel:
    """
    Financial modeling for F&B retail business analysis
    """
    
    def __init__(self):
        self.assumptions = {
            'revenue_growth_rate': 0.12,
            'cost_inflation_rate': 0.05,
            'tax_rate': 0.30,
            'discount_rate': 0.12,
            'terminal_growth_rate': 0.03,
            'working_capital_percent': 0.10,
            'capex_percent': 0.05
        }
    
    def project(self, business_model: Dict, profitability: Dict, years: int = 5) -> Dict:
        """
        Project financial statements for F&B retail business
        
        Args:
            business_model: Business model analysis results
            profitability: Profitability analysis results
            years: Number of years to project
            
        Returns:
            Dictionary with financial projections
        """
        
        # Get baseline metrics
        base_revenue = 100  # Base number for projections (in lakhs)
        
        # Revenue projections
        revenue_projections = self._project_revenue(base_revenue, years)
        
        # Cost projections
        cost_projections = self._project_costs(revenue_projections)
        
        # P&L statement
        income_statement = self._build_income_statement(revenue_projections, cost_projections)
        
        # Cash flow projections
        cash_flow = self._build_cash_flow(income_statement)
        
        # Balance sheet projections
        balance_sheet = self._build_balance_sheet(income_statement, cash_flow)
        
        # Key financial metrics
        metrics = self._calculate_metrics(income_statement, cash_flow, balance_sheet)
        
        return {
            'assumptions': self.assumptions,
            'income_statement': income_statement,
            'cash_flow': cash_flow,
            'balance_sheet': balance_sheet,
            'metrics': metrics,
            'summary': self._generate_summary(metrics)
        }
    
    def _project_revenue(self, base_revenue: float, years: int) -> List[float]:
        """Project revenue for given years"""
        revenues = [base_revenue]
        
        for year in range(1, years + 1):
            # Add some growth variability
            growth = self.assumptions['revenue_growth_rate'] * (1 + np.random.normal(0, 0.05))
            next_revenue = revenues[-1] * (1 + growth)
            revenues.append(next_revenue)
        
        return revenues
    
    def _project_costs(self, revenues: List[float]) -> Dict:
        """Project costs based on revenue"""
        cost_components = {
            'food_cost': 0.32,
            'labor_cost': 0.22,
            'rent_cost': 0.12,
            'marketing_cost': 0.05,
            'utilities': 0.04,
            'technology': 0.03,
            'admin_overhead': 0.10,
            'others': 0.12
        }
        
        costs = {}
        for year, revenue in enumerate(revenues):
            year_costs = {}
            for cost, percentage in cost_components.items():
                # Add some inflation
                inflation_factor = 1 + (self.assumptions['cost_inflation_rate'] * year / 5)
                year_costs[cost] = revenue * percentage * inflation_factor
            
            costs[f'year_{year}'] = year_costs
        
        return costs
    
    def _build_income_statement(self, revenues: List[float], costs: Dict) -> Dict:
        """Build income statement"""
        income_statements = {}
        
        for year_idx, revenue in enumerate(revenues):
            year_key = f'year_{year_idx}'
            year_costs = costs.get(year_key, {})
            
            total_costs = sum(year_costs.values())
            gross_profit = revenue - year_costs.get('food_cost', 0)
            operating_profit = revenue - total_costs
            ebitda = operating_profit  # Simplified
            net_profit = operating_profit * (1 - self.assumptions['tax_rate'])
            
            income_statements[year_key] = {
                'revenue': round(revenue, 2),
                'cost_of_goods_sold': round(year_costs.get('food_cost', 0), 2),
                'gross_profit': round(gross_profit, 2),
                'operating_expenses': round(total_costs - year_costs.get('food_cost', 0), 2),
                'operating_profit': round(operating_profit, 2),
                'ebitda': round(ebitda, 2),
                'tax': round(operating_profit * self.assumptions['tax_rate'], 2),
                'net_profit': round(net_profit, 2),
                'gross_margin': round((gross_profit / revenue) * 100, 1) if revenue > 0 else 0,
                'operating_margin': round((operating_profit / revenue) * 100, 1) if revenue > 0 else 0,
                'net_margin': round((net_profit / revenue) * 100, 1) if revenue > 0 else 0
            }
        
        return income_statements
    
    def _build_cash_flow(self, income_statement: Dict) -> Dict:
        """Build cash flow projections"""
        cash_flows = {}
        
        for year_key, statement in income_statement.items():
            # Simplified cash flow
            operating_cash = statement['net_profit'] + statement.get('depreciation', 0)
            
            # Working capital changes (simplified)
            working_capital = statement['revenue'] * self.assumptions['working_capital_percent']
            capex = statement['revenue'] * self.assumptions['capex_percent']
            
            free_cash_flow = operating_cash - working_capital - capex
            
            cash_flows[year_key] = {
                'operating_cash_flow': round(operating_cash, 2),
                'working_capital_change': round(-working_capital, 2),
                'capex': round(-capex, 2),
                'free_cash_flow': round(free_cash_flow, 2),
                'cumulative_cash_flow': 0  # Will be calculated
            }
        
        # Calculate cumulative cash flow
        cumulative = 0
        for year_key in sorted(cash_flows.keys()):
            cumulative += cash_flows[year_key]['free_cash_flow']
            cash_flows[year_key]['cumulative_cash_flow'] = round(cumulative, 2)
        
        return cash_flows
    
    def _build_balance_sheet(self, income_statement: Dict, cash_flow: Dict) -> Dict:
        """Build balance sheet projections"""
        balance_sheets = {}
        
        for year_key, statement in income_statement.items():
            # Simplified balance sheet
            assets = {
                'cash': cash_flow.get(year_key, {}).get('cumulative_cash_flow', 0),
                'inventory': statement['cost_of_goods_sold'] * 0.15,
                'receivables': statement['revenue'] * 0.10,
                'fixed_assets': statement['revenue'] * 0.50,
                'total_assets': 0
            }
            
            liabilities = {
                'payables': statement['cost_of_goods_sold'] * 0.20,
                'debt': statement['revenue'] * 0.20,
                'total_liabilities': 0,
                'equity': 0
            }
            
            # Calculate totals
            total_assets = sum([v for v in assets.values() if v != 'total_assets'])
            total_liabilities = sum([v for v in liabilities.values() if v != 'total_liabilities'])
            
            # Calculate equity (balancing figure)
            equity = total_assets - total_liabilities
            
            # Update values
            assets['total_assets'] = round(total_assets, 2)
            liabilities['total_liabilities'] = round(total_liabilities, 2)
            liabilities['equity'] = round(equity, 2)
            
            balance_sheets[year_key] = {
                'assets': {k: round(v, 2) if isinstance(v, (int, float)) else v 
                          for k, v in assets.items()},
                'liabilities': {k: round(v, 2) if isinstance(v, (int, float)) else v 
                               for k, v in liabilities.items()}
            }
        
        return balance_sheets
    
    def _calculate_metrics(self, income_statement: Dict, cash_flow: Dict, 
                          balance_sheet: Dict) -> Dict:
        """Calculate key financial metrics"""
        
        metrics = {}
        
        for year_key, statement in income_statement.items():
            # Profitability ratios
            metrics[f'{year_key}_profitability'] = {
                'gross_profit_margin': statement['gross_margin'],
                'operating_profit_margin': statement['operating_margin'],
                'net_profit_margin': statement['net_margin'],
                'return_on_assets': statement['net_profit'] / balance_sheet[year_key]['assets']['total_assets'] * 100,
                'return_on_equity': statement['net_profit'] / balance_sheet[year_key]['liabilities']['equity'] * 100
            }
            
            # Liquidity ratios
            current_assets = balance_sheet[year_key]['assets']['cash'] + \
                           balance_sheet[year_key]['assets']['inventory'] + \
                           balance_sheet[year_key]['assets']['receivables']
            current_liabilities = balance_sheet[year_key]['liabilities']['payables']
            
            metrics[f'{year_key}_liquidity'] = {
                'current_ratio': current_assets / current_liabilities if current_liabilities > 0 else 0,
                'quick_ratio': (current_assets - balance_sheet[year_key]['assets']['inventory']) / current_liabilities if current_liabilities > 0 else 0
            }
            
            # Efficiency ratios
            metrics[f'{year_key}_efficiency'] = {
                'inventory_turnover': statement['cost_of_goods_sold'] / balance_sheet[year_key]['assets']['inventory'] if balance_sheet[year_key]['assets']['inventory'] > 0 else 0,
                'receivables_turnover': statement['revenue'] / balance_sheet[year_key]['assets']['receivables'] if balance_sheet[year_key]['assets']['receivables'] > 0 else 0,
                'asset_turnover': statement['revenue'] / balance_sheet[year_key]['assets']['total_assets'] if balance_sheet[year_key]['assets']['total_assets'] > 0 else 0
            }
        
        return metrics
    
    def _generate_summary(self, metrics: Dict) -> Dict:
        """Generate financial summary"""
        
        # Calculate averages for the first year's metrics
        first_year_key = next(iter(metrics.keys()))
        
        if first_year_key:
            profitability = metrics.get(f'{first_year_key}_profitability', {})
            liquidity = metrics.get(f'{first_year_key}_liquidity', {})
            efficiency = metrics.get(f'{first_year_key}_efficiency', {})
        else:
            profitability = {}
            liquidity = {}
            efficiency = {}
        
        return {
            'profitability_rating': 'Excellent' if profitability.get('net_profit_margin', 0) > 15 else 
                                   'Good' if profitability.get('net_profit_margin', 0) > 10 else
                                   'Average' if profitability.get('net_profit_margin', 0) > 5 else 'Below Average',
            'liquidity_rating': 'Strong' if liquidity.get('current_ratio', 0) > 1.5 else 'Moderate',
            'efficiency_rating': 'High' if efficiency.get('asset_turnover', 0) > 1.0 else 'Medium',
            'financial_health': 'Healthy' if all([
                profitability.get('net_profit_margin', 0) > 8,
                liquidity.get('current_ratio', 0) > 1.2
            ]) else 'Needs Improvement'
        }
    
    def calculate_break_even(self, fixed_costs: float, variable_cost_per_unit: float, 
                             price_per_unit: float) -> Dict:
        """
        Calculate break-even analysis
        
        Args:
            fixed_costs: Total fixed costs
            variable_cost_per_unit: Variable cost per unit
            price_per_unit: Selling price per unit
            
        Returns:
            Break-even analysis results
        """
        contribution_margin = price_per_unit - variable_cost_per_unit
        break_even_units = fixed_costs / contribution_margin if contribution_margin > 0 else float('inf')
        break_even_revenue = break_even_units * price_per_unit
        
        return {
            'break_even_units': round(break_even_units, 2),
            'break_even_revenue': round(break_even_revenue
