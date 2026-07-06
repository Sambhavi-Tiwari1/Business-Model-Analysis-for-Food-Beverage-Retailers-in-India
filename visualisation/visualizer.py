"""
Visualization tools for F&B Retail Analysis
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class Visualizer:
    """
    Create visualizations for F&B retail analysis
    """
    
    def __init__(self):
        plt.style.use('seaborn-v0_8-darkgrid')
        self.colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E']
    
    def create_all_visualizations(self, market_data: pd.DataFrame,
                                  consumer_data: pd.DataFrame,
                                  competitor_data: pd.DataFrame,
                                  profitability: Dict):
        """Create all visualizations"""
        
        # Market analysis plots
        self.plot_market_growth(market_data, 'output/figures/market_growth.png')
        self.plot_segment_share(market_data, 'output/figures/segment_share.png')
        
        # Consumer analysis plots
        self.plot_consumer_demographics(consumer_data, 'output/figures/consumer_demographics.png')
        self.plot_consumer_preferences(consumer_data, 'output/figures/consumer_preferences.png')
        
        # Profitability plots
        self.plot_cost_breakdown(profitability, 'output/figures/cost_breakdown.png')
        self.plot_profitability_metrics(profitability, 'output/figures/profitability.png')
        
        # Strategic plots
        self.plot_strategic_matrix(profitability, 'output/figures/strategic_matrix.png')
        
        logger.info("All visualizations created successfully")
    
    def plot_market_growth(self, data: pd.DataFrame, save_path: str = None):
        """Plot market growth trends"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        segments = data['segment'].unique()
        for i, segment in enumerate(segments):
            segment_data = data[data['segment'] == segment]
            ax.plot(segment_data['year'], segment_data['market_size_bn'],
                   label=segment, marker='o', color=self.colors[i % len(self.colors)])
        
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Market Size (Billion INR)', fontsize=12)
        ax.set_title('F&B Market Growth by Segment', fontsize=14, fontweight='bold')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_segment_share(self, data: pd.DataFrame, save_path: str = None):
        """Plot market share by segment"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        latest_data = data[data['year'] == data['year'].max()]
        shares = latest_data.set_index('segment')['segment_share']
        
        wedges, texts, autotexts = ax.pie(shares.values, labels=shares.index, 
                                          autopct='%1.1f%%',
                                          colors=self.colors[:len(shares)],
                                          startangle=90)
        
        ax.set_title('Market Share by Segment', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_consumer_demographics(self, data: pd.DataFrame, save_path: str = None):
        """Plot consumer demographics"""
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Age distribution
        age_counts = data['age_group'].value_counts()
        axes[0].bar(age_counts.index, age_counts.values, color=self.colors[0])
        axes[0].set_title('Age Distribution', fontsize=12, fontweight='bold')
        axes[0].set_xlabel('Age Group')
        axes[0].set_ylabel('Count')
        axes[0].tick_params(axis='x', rotation=45)
        
        # Income distribution
        income_counts = data['income_level'].value_counts()
        axes[1].bar(income_counts.index, income_counts.values, color=self.colors[1])
        axes[1].set_title('Income Distribution', fontsize=12, fontweight='bold')
        axes[1].set_xlabel('Income Level')
        axes[1].set_ylabel('Count')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_consumer_preferences(self, data: pd.DataFrame, save_path: str = None):
        """Plot consumer preferences"""
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Top cuisines
        cuisine_counts = {}
        for cuisines in data['top_cuisines']:
            for cuisine in cuisines.split(', '):
                cuisine_counts[cuisine] = cuisine_counts.get(cuisine, 0) + 1
        
        sorted_cuisines = sorted(cuisine_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        cuisines, counts = zip(*sorted_cuisines)
        
        axes[0].barh(cuisines, counts, color=self.colors[2])
        axes[0].set_title('Top Cuisine Preferences', fontsize=12, fontweight='bold')
        axes[0].set_xlabel('Count')
        
        # Preferred channels
        channel_counts = {}
        for channels in data['preferred_channels']:
            for channel in channels.split(', '):
                channel_counts[channel] = channel_counts.get(channel, 0) + 1
        
        sorted_channels = sorted(channel_counts.items(), key=lambda x: x[1], reverse=True)
        channels, counts = zip(*sorted_channels)
        
        axes[1].bar(channels, counts, color=self.colors[3])
        axes[1].set_title('Preferred Channels', fontsize=12, fontweight='bold')
        axes[1].set_xlabel('Channel')
        axes[1].set_ylabel('Count')
        axes[1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_cost_breakdown(self, profitability: Dict, save_path: str = None):
        """Plot cost breakdown"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if 'cost_breakdown' in profitability:
            costs = profitability['cost_breakdown']
        else:
            costs = {
                'Food Cost': 32,
                'Labor Cost': 22,
                'Rent': 12,
                'Marketing': 5,
                'Utilities': 4,
                'Technology': 3,
                'Others': 22
            }
        
        sorted_costs = sorted(costs.items(), key=lambda x: x[1], reverse=True)
        labels, values = zip(*sorted_costs)
        
        bars = ax.bar(labels, values, color=self.colors)
        ax.set_title('Cost Structure Breakdown', fontsize=14, fontweight='bold')
        ax.set_ylabel('Percentage of Revenue (%)')
        ax.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{value:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_profitability_metrics(self, profitability: Dict, save_path: str = None):
        """Plot profitability metrics"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if 'profit_metrics' in profitability:
            metrics = profitability['profit_metrics']
            profit_margins = {
                'Gross Margin': metrics['gross_profit_margin'],
                'Operating Margin': metrics['operating_profit_margin'],
                'Net Margin': metrics['net_profit_margin']
            }
        else:
            profit_margins = {
                'Gross Margin': 65,
                'Operating Margin': 25,
                'Net Margin': 15
            }
        
        bars = ax.bar(profit_margins.keys(), profit_margins.values(), 
                     color=['#2E86AB', '#6A994E', '#F18F01'])
        
        ax.set_title('Profitability Margins', fontsize=14, fontweight='bold')
        ax.set_ylabel('Percentage (%)')
        ax.set_ylim(0, 80)
        
        # Add value labels
        for bar, value in zip(bars, profit_margins.values()):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{value:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_strategic_matrix(self, profitability: Dict, save_path: str = None):
        """Plot strategic recommendation matrix"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        strategies = [
            ('Operational Efficiency', 0.8, 0.7),
            ('Customer Retention', 0.6, 0.8),
            ('Growth Expansion', 0.7, 0.6),
            ('Sustainability', 0.5, 0.5),
            ('Technology Adoption', 0.4, 0.6),
            ('Cost Reduction', 0.9, 0.4)
        ]
        
        for name, x, y in strategies:
            ax.scatter(x, y, s=800, color=self.colors[0], alpha=0.6)
            ax.annotate(name, (x, y), ha='center', va='center', fontsize=9)
        
        ax.set_xlabel('Impact', fontsize=12)
        ax.set_ylabel('Feasibility', fontsize=12)
        ax.set_title('Strategic Recommendation Matrix', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
