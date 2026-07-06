#!/usr/bin/env python
"""
Main execution script for F&B Retail Business Model Analysis
"""
import os
import sys
import argparse
import yaml
import logging
import json
from datetime import datetime
import pandas as pd
import numpy as np

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.market_data_generator import MarketDataGenerator
from data.consumer_data_generator import ConsumerDataGenerator
from data.competitor_data_generator import CompetitorDataGenerator
from analysis.market_analyzer import MarketAnalyzer
from analysis.business_model_analyzer import BusinessModelAnalyzer
from analysis.profitability_analyzer import ProfitabilityAnalyzer
from analysis.consumer_analyzer import ConsumerAnalyzer
from analysis.competitive_analyzer import CompetitiveAnalyzer
from visualization.visualizer import Visualizer
from models.financial_model import FinancialModel
from models.location_model import LocationModel

logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config(config_path='config.yaml'):
    """Load configuration"""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def create_directories():
    """Create necessary directories"""
    dirs = ['output/reports', 'output/figures', 'data/raw', 'data/processed']
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def generate_all_data(config):
    """Generate all synthetic data"""
    logger.info("Generating market data...")
    market_gen = MarketDataGenerator()
    market_data = market_gen.generate_market_size_data(5)
    market_data.to_csv('data/raw/market_data.csv', index=False)
    
    logger.info("Generating consumer data...")
    consumer_gen = ConsumerDataGenerator()
    consumer_data = consumer_gen.generate_consumer_preferences(1000)
    consumer_data.to_csv('data/raw/consumer_data.csv', index=False)
    
    logger.info("Generating competitor data...")
    competitor_gen = CompetitorDataGenerator()
    competitor_data = competitor_gen.generate_competitor_data()
    competitor_data.to_csv('data/raw/competitor_data.csv', index=False)
    
    return market_data, consumer_data, competitor_data

def run_full_analysis(config):
    """Run complete analysis pipeline"""
    logger.info("="*60)
    logger.info("F&B RETAIL BUSINESS MODEL ANALYSIS")
    logger.info("="*60)
    
    # Generate data
    market_data, consumer_data, competitor_data = generate_all_data(config)
    
    # Market Analysis
    logger.info("\n📊 Running Market Analysis...")
    market_analyzer = MarketAnalyzer()
    market_insights = market_analyzer.analyze(market_data)
    
    # Consumer Analysis
    logger.info("\n👥 Running Consumer Analysis...")
    consumer_analyzer = ConsumerAnalyzer()
    consumer_insights = consumer_analyzer.analyze(consumer_data)
    
    # Competitive Analysis
    logger.info("\n🏪 Running Competitive Analysis...")
    competitive_analyzer = CompetitiveAnalyzer()
    competitive_insights = competitive_analyzer.analyze(competitor_data)
    
    # Business Model Analysis
    logger.info("\n📋 Running Business Model Analysis...")
    business_analyzer = BusinessModelAnalyzer()
    business_model = business_analyzer.analyze(market_data, competitor_data)
    
    # Profitability Analysis
    logger.info("\n💰 Running Profitability Analysis...")
    profit_analyzer = ProfitabilityAnalyzer()
    profitability = profit_analyzer.analyze(market_data, consumer_data)
    
    # Financial Modeling
    logger.info("\n📈 Running Financial Modeling...")
    financial_model = FinancialModel()
    financial_projections = financial_model.project(business_model, profitability)
    
    # Location Analysis
    logger.info("\n📍 Running Location Analysis...")
    location_model = LocationModel()
    location_recommendations = location_model.analyze(config)
    
    # Generate Visualizations
    logger.info("\n🎨 Generating Visualizations...")
    visualizer = Visualizer()
    visualizer.create_all_visualizations(market_data, consumer_data, 
                                        competitor_data, profitability)
    
    # Generate Report
    logger.info("\n📄 Generating Report...")
    generate_report(market_insights, consumer_insights, competitive_insights,
                   business_model, profitability, financial_projections,
                   location_recommendations)
    
    logger.info("\n✅ Analysis Complete!")
    logger.info(f"Results saved to 'output/reports/' and 'output/figures/'")
    
    return {
        'market_insights': market_insights,
        'consumer_insights': consumer_insights,
        'competitive_insights': competitive_insights,
        'business_model': business_model,
        'profitability': profitability,
        'financial_projections': financial_projections,
        'location_recommendations': location_recommendations
    }

def generate_report(market_insights, consumer_insights, competitive_insights,
                   business_model, profitability, financial_projections,
                   location_recommendations):
    """Generate comprehensive report"""
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'market_analysis': market_insights,
        'consumer_analysis': consumer_insights,
        'competitive_analysis': competitive_insights,
        'business_model': business_model,
        'profitability': profitability,
        'financial_projections': financial_projections,
        'location_recommendations': location_recommendations,
        'strategic_recommendations': generate_strategic_recommendations(
            market_insights, consumer_insights, competitive_insights,
            business_model, profitability
        )
    }
    
    # Save as JSON
    with open('output/reports/full_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    # Save as CSV summary
    summary_data = {
        'Metric': ['Market Size', 'Growth Rate', 'Consumer Spending', 
                   'Avg Profit Margin', 'Location Score', 'Recommendation Priority'],
        'Value': [
            market_insights.get('total_market_size', 'N/A'),
            market_insights.get('avg_growth_rate', 'N/A'),
            consumer_insights.get('avg_spending', 'N/A'),
            profitability.get('avg_profit_margin', 'N/A'),
            location_recommendations.get('avg_score', 'N/A'),
            'High'
        ]
    }
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv('output/reports/summary_report.csv', index=False)
    
    logger.info("Report generated successfully")

def generate_strategic_recommendations(market_insights, consumer_insights,
                                      competitive_insights, business_model,
                                      profitability):
    """Generate strategic recommendations"""
    recommendations = {
        'operational_efficiency': [
            'Implement cloud kitchen model for cost reduction (25% savings)',
            'Adopt AI-based inventory management to reduce waste by 20%',
            'Integrate POS with inventory tracking for real-time management',
            'Optimize supplier relationships for better pricing'
        ],
        'customer_retention': [
            'Launch tiered loyalty program with personalized rewards',
            'Implement AI-based personalization for recommendations',
            'Create community engagement through events and social media',
            'Develop mobile app with order tracking and offers'
        ],
        'growth_expansion': [
            'Focus on office districts and food courts for new locations',
            'Optimize delivery platform presence (Swiggy, Zomato)',
            'Explore cloud kitchen model for delivery-only operations',
            'Consider franchise model for faster expansion'
        ],
        'sustainability': [
            'Reduce single-use plastics and implement eco-friendly packaging',
            'Source local ingredients to support community and reduce costs',
            'Implement food waste reduction programs',
            'Adopt energy-efficient equipment and practices'
        ]
    }
    return recommendations

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='F&B Retail Business Model Analysis')
    parser.add_argument('--full', action='store_true', help='Run full analysis')
    parser.add_argument('--market', action='store_true', help='Run market analysis only')
    parser.add_argument('--consumer', action='store_true', help='Run consumer analysis only')
    parser.add_argument('--profitability', action='store_true', help='Run profitability analysis only')
    parser.add_argument('--strategic', action='store_true', help='Generate strategic recommendations only')
    parser.add_argument('--report', action='store_true', help='Generate report only')
    parser.add_argument('--config', type=str, default='config.yaml', help='Config file path')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode')
    
    args = parser.parse_args()
    config = load_config(args.config)
    create_directories()
    
    if args.interactive:
        interactive_mode()
    elif args.full:
        run_full_analysis(config)
    elif args.market:
        run_market_analysis(config)
    elif args.consumer:
        run_consumer_analysis(config)
    elif args.profitability:
        run_profitability_analysis(config)
    elif args.strategic:
        generate_strategic_recommendations_only(config)
    elif args.report:
        generate_report_only()
    else:
        parser.print_help()

def interactive_mode():
    """Interactive CLI mode"""
    print("\n" + "="*60)
    print("🍽️ F&B RETAIL BUSINESS MODEL ANALYZER")
    print("="*60 + "\n")
    
    print("1. Run Full Analysis")
    print("2. Run Market Analysis Only")
    print("3. Run Consumer Analysis Only")
    print("4. Run Profitability Analysis Only")
    print("5. Generate Strategic Recommendations")
    print("6. View Results")
    print("7. Exit")
    
    choice = input("\nSelect option (1-7): ")
    
    config = load_config()
    
    if choice == '1':
        run_full_analysis(config)
    elif choice == '2':
        run_market_analysis(config)
    elif choice == '3':
        run_consumer_analysis(config)
    elif choice == '4':
        run_profitability_analysis(config)
    elif choice == '5':
        generate_strategic_recommendations_only(config)
    elif choice == '6':
        view_results()
    else:
        print("Exiting...")

def view_results():
    """View analysis results"""
    try:
        with open('output/reports/full_report.json', 'r') as f:
            report = json.load(f)
        
        print("\n" + "="*60)
        print("📊 ANALYSIS RESULTS")
        print("="*60)
        
        print(f"\n📈 Market Overview:")
        print(f"  • Total Market Size: {report['market_analysis'].get('total_market_size', 'N/A')}")
        print(f"  • Growth Rate: {report['market_analysis'].get('avg_growth_rate', 'N/A')}")
        
        print(f"\n👥 Consumer Insights:")
        print(f"  • Avg Spending: {report['consumer_analysis'].get('avg_spending', 'N/A')}")
        print(f"  • Top Segments: {report['consumer_analysis'].get('top_segments', 'N/A')}")
        
        print(f"\n💰 Profitability:")
        print(f"  • Avg Profit Margin: {report['profitability'].get('avg_profit_margin', 'N/A')}")
        print(f"  • Cost Breakdown: {report['profitability'].get('cost_breakdown', 'N/A')}")
        
        print(f"\n💡 Strategic Recommendations:")
        for category, recommendations in report['strategic_recommendations'].items():
            print(f"\n  {category.replace('_', ' ').title()}:")
            for rec in recommendations[:3]:
                print(f"    • {rec}")
                
    except FileNotFoundError:
        print("No results found. Please run the analysis first.")

if __name__ == "__main__":
    main()
