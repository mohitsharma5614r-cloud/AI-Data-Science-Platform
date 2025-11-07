"""
Autonomous Data Science Agent
Full automated data pipeline with cleaning, feature engineering, AutoML, visualization, and reporting
"""

import os
import sys
from pathlib import Path
import warnings
import numpy as np
warnings.filterwarnings('ignore')

from data_loader import DataLoader
from data_cleaner import DataCleaner
from feature_engineer import FeatureEngineer
from automl_engine import AutoMLEngine
from visualizer import Visualizer
from report_generator import ReportGenerator

class AutonomousDataScienceAgent:
    """
    AI Data Scientist - Fully automated data science pipeline
    """
    
    def __init__(self, csv_path: str, target_column: str = None, output_dir: str = "output"):
        """
        Initialize the Autonomous DS Agent
        
        Args:
            csv_path: Path to CSV file
            target_column: Target column for prediction (auto-detect if None)
            output_dir: Directory to save outputs
        """
        self.csv_path = csv_path
        self.target_column = target_column
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Pipeline components
        self.loader = DataLoader()
        self.cleaner = DataCleaner()
        self.feature_engineer = FeatureEngineer()
        self.automl = AutoMLEngine()
        self.visualizer = Visualizer(output_dir=str(self.output_dir / "visualizations"))
        self.report_gen = ReportGenerator(output_dir=str(self.output_dir))
        
        # Pipeline state
        self.raw_data = None
        self.cleaned_data = None
        self.engineered_data = None
        self.model_results = None
        self.insights = {}
        
    def run(self):
        """
        Execute the full autonomous data science pipeline
        """
        print("Autonomous Data Science Agent Starting...")
        print("=" * 60)
        
        # Step 1: Load Data
        print("\n Step 1: Loading Data...")
        self.raw_data = self.loader.load_csv(self.csv_path)
        self.insights['data_info'] = self.loader.get_data_info(self.raw_data)
        print(f"[OK] Loaded {len(self.raw_data)} rows, {len(self.raw_data.columns)} columns")
        
        # Validate data is suitable for ML
        if len(self.raw_data.columns) < 2:
            raise ValueError("Dataset must have at least 2 columns (features + target)")
        
        if len(self.raw_data) < 10:
            raise ValueError("Dataset must have at least 10 rows for meaningful analysis")
        
        # Check if there's at least one numeric column
        numeric_cols = self.raw_data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            raise ValueError("Dataset must have at least one numeric column for machine learning")
        
        # Step 2: Auto-detect target if not provided
        if self.target_column is None:
            print("\n Auto-detecting target column...")
            self.target_column = self._auto_detect_target()
            print(f"[OK] Target column detected: {self.target_column}")
        
        # Step 3: Clean Data
        print("\n Step 2: Cleaning Data...")
        self.cleaned_data = self.cleaner.clean(self.raw_data)
        self.insights['cleaning_report'] = self.cleaner.get_cleaning_report()
        print(f"[OK] Data cleaned successfully")
        
        # Step 4: Feature Engineering
        print("\n Step 3: Engineering Features...")
        self.engineered_data = self.feature_engineer.engineer_features(
            self.cleaned_data, 
            target_column=self.target_column
        )
        self.insights['feature_report'] = self.feature_engineer.get_feature_report()
        print(f"[OK] Features engineered: {len(self.engineered_data.columns)} total features")
        
        # Step 5: AutoML - Find Best Model
        print("\n Step 4: Running AutoML (Finding Best Model)...")
        self.model_results = self.automl.find_best_model(
            self.engineered_data,
            target_column=self.target_column
        )
        print(f"[OK] Best Model: {self.model_results['best_model_name']}")
        print(f"   Score: {self.model_results['best_score']:.4f}")
        
        # Step 6: Generate Visualizations
        print("\n Step 5: Generating Visualizations...")
        self.visualizer.generate_all_plots(
            raw_data=self.raw_data,
            cleaned_data=self.cleaned_data,
            engineered_data=self.engineered_data,
            target_column=self.target_column,
            model_results=self.model_results
        )
        print(f"[OK] Visualizations saved to {self.visualizer.output_dir}")
        
        # Step 7: Generate PDF Report
        print("\n Step 6: Generating PDF Report...")
        report_path = self.report_gen.generate_report(
            csv_path=self.csv_path,
            insights=self.insights,
            model_results=self.model_results,
            visualizations_dir=self.visualizer.output_dir
        )
        print(f"[OK] Report saved to {report_path}")
        
        print("\n" + "=" * 60)
        print(" Autonomous Data Science Pipeline Completed!")
        print(f" All outputs saved to: {self.output_dir}")
        print("=" * 60)
        
        return {
            'report_path': report_path,
            'model_results': self.model_results,
            'output_dir': str(self.output_dir)
        }
    
    def _auto_detect_target(self):
        """
        Automatically detect the target column
        Heuristics: Column with reasonable cardinality, common names, or last column
        """
        columns = self.raw_data.columns.tolist()
        
        # Check for common target names first (exact match or word boundary)
        target_keywords = ['target', 'label', 'class', 'output', 'prediction', 'churn', 'outcome', 'attrition']
        for col in columns:
            col_lower = col.lower()
            # Check for exact match or keyword at word boundaries
            if col_lower in target_keywords or any(keyword == col_lower for keyword in target_keywords):
                if self._is_valid_target(col):
                    return col
            # Also check if column ends with these keywords
            if any(col_lower.endswith('_' + keyword) or col_lower.endswith(keyword) for keyword in target_keywords):
                if self._is_valid_target(col):
                    return col
        
        # Find columns with reasonable cardinality for classification
        # (not too many unique values, not all unique)
        for col in reversed(columns):  # Start from end
            if self._is_valid_target(col):
                return col
        
        # No valid target found - raise error with helpful message
        raise ValueError(
            "Cannot auto-detect a valid target column. All columns appear to be IDs or have too many unique values. "
            "Please specify the target column explicitly using --target parameter. "
            f"Available columns: {', '.join(columns)}"
        )
    
    def _is_valid_target(self, column: str) -> bool:
        """
        Check if a column is suitable as a target for ML
        """
        col_data = self.raw_data[column]
        n_unique = col_data.nunique()
        n_rows = len(col_data)
        
        # Skip ID-like columns (too many unique values)
        if n_unique > n_rows * 0.8:  # More than 80% unique
            return False
        
        # Skip columns with only 1 unique value
        if n_unique < 2:
            return False
        
        # Skip text columns that look like IDs, URLs, emails
        if col_data.dtype == 'object':
            sample = str(col_data.iloc[0]) if len(col_data) > 0 else ""
            if any(pattern in sample.lower() for pattern in ['http://', 'https://', '@', '.com', 'www.']):
                return False
        
        return True


def main():
    """
    Main entry point for the Autonomous DS Agent
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Autonomous Data Science Agent')
    parser.add_argument('csv_path', type=str, help='Path to CSV file')
    parser.add_argument('--target', type=str, default=None, help='Target column name (auto-detect if not provided)')
    parser.add_argument('--output', type=str, default='output', help='Output directory')
    
    args = parser.parse_args()
    
    # Create and run agent
    agent = AutonomousDataScienceAgent(
        csv_path=args.csv_path,
        target_column=args.target,
        output_dir=args.output
    )
    
    results = agent.run()
    
    print(f"\n Done! Check your report at: {results['report_path']}")


if __name__ == "__main__":
    main()
