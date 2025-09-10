#!/usr/bin/env python3
"""
Volunteer Performance Analysis Tool
==================================

This script analyzes volunteer datasets to help determine promotion criteria
for the 'active member' role based on various performance metrics.
"""

import pandas as pd
import json
from typing import Dict, List
import statistics

class VolunteerAnalyzer:
    """Analyze volunteer performance data to suggest promotion criteria"""
    
    def __init__(self, csv_file: str = None, json_file: str = None, score_filter: str = 'all', min_score: float = None):
        """Initialize analyzer with data from CSV or JSON file"""
        if csv_file:
            self.df = pd.read_csv(csv_file)
        elif json_file:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.df = pd.json_normalize(data)
        else:
            raise ValueError("Must provide either csv_file or json_file")
        
        # Store original dataset for reference
        self.original_df = self.df.copy()
        self.score_filter = score_filter
        self.min_score = min_score
        
        # Apply score filtering
        self._apply_score_filter()
    
    def _apply_score_filter(self):
        """Apply score filtering based on user preferences"""
        if self.score_filter == 'above' and self.min_score is not None:
            self.df = self.df[self.df['Total_Score'] >= self.min_score]
            print(f"📊 Filtering: Analyzing only volunteers with scores >= {self.min_score}")
        elif self.score_filter == 'all':
            print(f"📊 Filtering: Analyzing ALL volunteers (no score filtering)")
        
        if len(self.df) == 0:
            print("⚠️  WARNING: No volunteers match the specified score filter criteria!")
            print("    Consider adjusting your filter settings.")
        else:
            filtered_count = len(self.df)
            original_count = len(self.original_df)
            percentage = (filtered_count / original_count) * 100
            print(f"📈 Dataset: {filtered_count} volunteers selected ({percentage:.1f}% of original {original_count})")
        
        print("="*70)
    
    def basic_statistics(self):
        """Generate basic statistics about the dataset"""
        print("=== Basic Dataset Statistics ===")
        print(f"Total volunteers: {len(self.df)}")
        print(f"\nScore Statistics:")
        print(f"  Mean: {self.df['Total_Score'].mean():.2f}")
        print(f"  Median: {self.df['Total_Score'].median():.2f}")
        print(f"  Std Dev: {self.df['Total_Score'].std():.2f}")
        print(f"  Min: {self.df['Total_Score'].min()}")
        print(f"  Max: {self.df['Total_Score'].max()}")
        
        print(f"\nTasks Completed Statistics:")
        print(f"  Mean: {self.df['Tasks_Completed'].mean():.2f}")
        print(f"  Median: {self.df['Tasks_Completed'].median():.2f}")
        print(f"  Min: {self.df['Tasks_Completed'].min()}")
        print(f"  Max: {self.df['Tasks_Completed'].max()}")
        
        print(f"\nAverage Mark Statistics:")
        print(f"  Mean: {self.df['Average_Mark'].mean():.2f}")
        print(f"  Median: {self.df['Average_Mark'].median():.2f}")
        print(f"  Min: {self.df['Average_Mark'].min():.2f}")
        print(f"  Max: {self.df['Average_Mark'].max():.2f}")
        
        print(f"\nAverage Rating Statistics:")
        print(f"  Mean: {self.df['Average_Rating'].mean():.2f}")
        print(f"  Median: {self.df['Average_Rating'].median():.2f}")
        print(f"  Min: {self.df['Average_Rating'].min():.2f}")
        print(f"  Max: {self.df['Average_Rating'].max():.2f}")
    
    def percentile_analysis(self):
        """Analyze performance using percentiles"""
        print("\n=== Percentile Analysis ===")
        
        # Score percentiles
        percentiles = [10, 25, 50, 75, 90, 95]
        print("Total Score Percentiles:")
        for p in percentiles:
            value = self.df['Total_Score'].quantile(p/100)
            print(f"  {p}th percentile: {value:.1f}")
        
        # Average mark percentiles
        print("\nAverage Mark Percentiles:")
        for p in percentiles:
            value = self.df['Average_Mark'].quantile(p/100)
            print(f"  {p}th percentile: {value:.2f}")
        
        # Average rating percentiles
        print("\nAverage Rating Percentiles:")
        for p in percentiles:
            value = self.df['Average_Rating'].quantile(p/100)
            print(f"  {p}th percentile: {value:.2f}")
        
        # Tasks completed percentiles
        print("\nTasks Completed Percentiles:")
        for p in percentiles:
            value = self.df['Tasks_Completed'].quantile(p/100)
            print(f"  {p}th percentile: {value:.0f}")
    
    def show_promotion_thresholds(self, target_percentile: float = 10.0):
        """
        Show score threshold for promoting volunteers to 'active volunteer' status
        
        Args:
            target_percentile: Target percentage of volunteers to promote (e.g., 10.0 for top 10%)
        """
        # Calculate the score threshold based on target percentile
        score_threshold_percentile = (100 - target_percentile) / 100
        score_threshold = self.df['Total_Score'].quantile(score_threshold_percentile)
        
        # Calculate how many volunteers would qualify
        qualified_count = len(self.df[self.df['Total_Score'] >= score_threshold])
        actual_percentage = (qualified_count / len(self.df)) * 100
        
        print(f"\n=== Promotion Threshold Analysis ===")
        print(f"Target: Top {target_percentile}% of volunteers")
        print(f"Score Threshold: ≥ {score_threshold:.0f}")
        print(f"Volunteers Promoted: {qualified_count} ({actual_percentage:.1f}%)")
        print(f"Expected: ~{len(self.df) * (target_percentile/100):.0f} volunteers")
        
        return {
            'threshold': score_threshold,
            'promoted_count': qualified_count,
            'actual_percentage': actual_percentage
        }
    
    def compare_promotion_percentiles(self, target_percentile: float = 15.0, common_percentiles: list = None):
        """
        Compare chosen percentile with common promotion percentiles and median/mean thresholds
        
        Args:
            target_percentile: Your chosen percentile (e.g., 15.0 for top 15%)
            common_percentiles: List of common percentiles to compare against (default: [10, 25, 50])
        """
        if common_percentiles is None:
            common_percentiles = [10, 25, 50]
        
        print(f"\n=== Promotion Percentile Comparison ===")
        print(f"Comparing your choice (top {target_percentile}%) with common thresholds")
        
        # Calculate thresholds and counts for all percentiles
        results = {}
        all_percentiles = [target_percentile] + [p for p in common_percentiles if p != target_percentile]
        
        for percentile in all_percentiles:
            threshold_percentile = (100 - percentile) / 100
            threshold = self.df['Total_Score'].quantile(threshold_percentile)
            count = len(self.df[self.df['Total_Score'] >= threshold])
            actual_pct = (count / len(self.df)) * 100
            
            results[percentile] = {
                'threshold': threshold,
                'count': count,
                'actual_percentage': actual_pct
            }
        
        # Calculate median and mean thresholds
        median_threshold = self.df['Total_Score'].median()
        mean_threshold = self.df['Total_Score'].mean()
        
        median_count = len(self.df[self.df['Total_Score'] >= median_threshold])
        mean_count = len(self.df[self.df['Total_Score'] >= mean_threshold])
        
        median_pct = (median_count / len(self.df)) * 100
        mean_pct = (mean_count / len(self.df)) * 100
        
        # Display comparison table
        print(f"\n📊 Threshold Comparison:")
        print(f"{'Method':<20} {'Threshold':<12} {'Promoted':<10} {'Percentage':<12}")
        print("-" * 55)
        
        # Show target percentile first
        target_result = results[target_percentile]
        print(f"{'Top ' + str(target_percentile) + '% ✅':<20} "
              f"{target_result['threshold']:<12.0f} "
              f"{target_result['count']:<10} "
              f"{target_result['actual_percentage']:<12.1f}%")
        
        # Show common percentiles
        for pct in common_percentiles:
            if pct != target_percentile:
                result = results[pct]
                print(f"{'Top ' + str(pct) + '%':<20} "
                      f"{result['threshold']:<12.0f} "
                      f"{result['count']:<10} "
                      f"{result['actual_percentage']:<12.1f}%")
        
        # Show median and mean
        print("-" * 55)
        print(f"{'Median Score':<20} "
              f"{median_threshold:<12.0f} "
              f"{median_count:<10} "
              f"{median_pct:<12.1f}%")
        print(f"{'Mean Score':<20} "
              f"{mean_threshold:<12.0f} "
              f"{mean_count:<10} "
              f"{mean_pct:<12.1f}%")
        
        # Analysis
        print(f"\n💡 Analysis:")
        target_count = results[target_percentile]['count']
        
        # Compare with common percentiles
        for pct in common_percentiles:
            if pct != target_percentile:
                diff = target_count - results[pct]['count']
                if diff > 0:
                    print(f"   • Your choice promotes {diff} MORE volunteers than top {pct}%")
                elif diff < 0:
                    print(f"   • Your choice promotes {abs(diff)} FEWER volunteers than top {pct}%")
                else:
                    print(f"   • Your choice promotes the SAME number as top {pct}%")
        
        # Compare with median/mean
        median_diff = target_count - median_count
        mean_diff = target_count - mean_count
        
        if median_diff > 0:
            print(f"   • Your choice promotes {median_diff} MORE volunteers than median threshold")
        else:
            print(f"   • Your choice promotes {abs(median_diff)} FEWER volunteers than median threshold")
            
        if mean_diff > 0:
            print(f"   • Your choice promotes {mean_diff} MORE volunteers than mean threshold")
        else:
            print(f"   • Your choice promotes {abs(mean_diff)} FEWER volunteers than mean threshold")
        
        return results
    
    def test_score_threshold(self, min_score: float, show_volunteers: bool = True):
        """Test how many volunteers would qualify with score-only criteria"""
        qualified = self.df[self.df['Total_Score'] >= min_score]
        
        percentage = (len(qualified) / len(self.df)) * 100
        
        print(f"\n=== Testing Score Threshold ===")
        print(f"Criteria: Score ≥ {min_score}")
        print(f"Qualified volunteers: {len(qualified)} ({percentage:.1f}%)")
        
        qualified_sorted = None
        if len(qualified) > 0:
            qualified_sorted = qualified.sort_values('Total_Score', ascending=False)
            if show_volunteers:
                print("\nQualified volunteers for 'Active Volunteer' promotion:")
                for _, volunteer in qualified_sorted.iterrows():
                    print(f"  {volunteer['Name']}: Score={volunteer['Total_Score']}")
        else:
            print("No volunteers meet this criteria. Consider lowering the threshold.")
        
        return {
            'qualified_count': len(qualified),
            'percentage': percentage,
            'qualified_volunteers': qualified_sorted
        }
    
    def suggest_promotion_criteria(self, target_percentile: float = 10.0):
        """
        Suggest score-based promotion criteria (simplified version)
        
        Args:
            target_percentile: Target percentage of volunteers to promote (e.g., 10.0 for top 10%)
        """
        print(f"\n=== Promotion Criteria Suggestion ===")
        
        # Show the threshold for the target percentile
        result = self.show_promotion_thresholds(target_percentile)
        
        # Compare with common percentiles
        self.compare_promotion_percentiles(target_percentile)
        
        return result

    
    def performance_correlation(self):
        """Analyze correlation between different performance metrics"""
        print("\n=== Performance Correlations ===")
        correlations = self.df[['Total_Score', 'Average_Mark', 'Average_Rating', 'Tasks_Completed']].corr()
        print(correlations.round(3))

def main():
    """Analyze volunteer datasets with CLI argument support"""
    import argparse
    import os
    
    parser = argparse.ArgumentParser(
        description="Analyze volunteer performance data to determine promotion criteria",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python volunteer_analyzer.py                           # Analyze volunteers.csv (top 10%)
  python volunteer_analyzer.py volunteers.csv           # Analyze specific CSV file (top 10%)
  python volunteer_analyzer.py --json data.json         # Analyze JSON file (top 10%)
  python volunteer_analyzer.py --above 50               # Analyze only scores >= 50 (top 10%)
  python volunteer_analyzer.py --percentile 25          # Target top 25% for promotion
  python volunteer_analyzer.py --percentile 15          # Target top 15% for promotion
  python volunteer_analyzer.py volunteers.csv --above 30 --percentile 20  # Custom analysis
        """
    )
    
    parser.add_argument(
        'dataset', 
        nargs='?', 
        default='volunteers.csv',
        help='Dataset file to analyze (default: volunteers.csv)'
    )
    
    parser.add_argument(
        '--json', 
        action='store_true',
        help='Treat the dataset file as JSON instead of CSV'
    )
    
    # Score filtering options
    parser.add_argument(
        '--above',
        type=float,
        metavar='SCORE',
        help='Analyze only volunteers with total scores >= SCORE'
    )
    
    # Promotion criteria options
    parser.add_argument(
        '--percentile',
        type=float,
        default=10.0,
        metavar='PCT',
        help='Target percentile for promotion (e.g., 10.0 for top 10%%) (default: 10.0)'
    )
    
    
    args = parser.parse_args()
    
    # Check if the specified file exists
    if not os.path.exists(args.dataset):
        print(f"Error: Dataset file '{args.dataset}' not found.")
        if args.dataset == 'volunteers.csv':
            print("Run the dataset generator first to create sample data:")
            print("  python volunteer_dataset_generator.py")
        return
    
    # Determine score filtering options
    score_filter = 'all'
    min_score = None
    
    if args.above is not None:
        score_filter = 'above'
        min_score = args.above
    
    # Determine file type and create analyzer
    try:
        if args.json:
            print(f"Analyzing {args.dataset} (JSON format) for Active Volunteer Promotion Criteria")
            analyzer = VolunteerAnalyzer(json_file=args.dataset, score_filter=score_filter, min_score=min_score)
        else:
            print(f"Analyzing {args.dataset} (CSV format) for Active Volunteer Promotion Criteria")
            analyzer = VolunteerAnalyzer(csv_file=args.dataset, score_filter=score_filter, min_score=min_score)
        
        # Check if we have data to analyze after filtering
        if len(analyzer.df) == 0:
            print("\n❌ No volunteers match the specified criteria. Analysis cannot proceed.")
            print("💡 Try adjusting your filter settings or use a different dataset.")
            return
        
        # Run full analysis
        analyzer.basic_statistics()
        analyzer.percentile_analysis()
        
        # Run promotion criteria analysis
        analyzer.suggest_promotion_criteria(target_percentile=args.percentile)
        
        analyzer.performance_correlation()
        
        # Test a custom score threshold example
        print(f"\n" + "="*60)
        print("CUSTOM SCORE THRESHOLD TEST EXAMPLE")
        print("="*60)
        analyzer.test_score_threshold(min_score=40, show_volunteers=False)
        
    except Exception as e:
        print(f"Error analyzing dataset: {e}")
        print("Make sure the file format is correct and contains the required columns:")
        print("  CSV: Name, Total_Score, Tasks_Completed, Average_Mark, Average_Rating")

if __name__ == "__main__":
    main()
