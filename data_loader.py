"""
Data Loader Module
Handles CSV loading and initial data inspection
"""

import pandas as pd
import numpy as np
from pathlib import Path

class DataLoader:
    """
    Intelligent data loader with automatic encoding detection and error handling
    """
    
    def __init__(self):
        self.data_info = {}
    
    def load_csv(self, csv_path: str) -> pd.DataFrame:
        """
        Load CSV with automatic encoding detection and error handling
        
        Args:
            csv_path: Path to CSV file
            
        Returns:
            Loaded DataFrame
        """
        csv_path = Path(csv_path)
        
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        
        for encoding in encodings:
            try:
                df = pd.read_csv(csv_path, encoding=encoding)
                print(f"   Loaded with encoding: {encoding}")
                return df
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"   Error with {encoding}: {str(e)}")
                continue
        
        # Last resort: try with error handling
        try:
            df = pd.read_csv(csv_path, encoding='utf-8', encoding_errors='ignore')
            print("   Loaded with error handling (some characters may be lost)")
            return df
        except Exception as e:
            raise Exception(f"Failed to load CSV: {str(e)}")
    
    def get_data_info(self, df: pd.DataFrame) -> dict:
        """
        Get comprehensive information about the dataset
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary with data information
        """
        info = {
            'shape': df.shape,
            'columns': df.columns.tolist(),
            'dtypes': df.dtypes.to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum() / 1024**2,  # MB
            'missing_values': df.isnull().sum().to_dict(),
            'missing_percentage': (df.isnull().sum() / len(df) * 100).to_dict(),
            'numeric_columns': df.select_dtypes(include=[np.number]).columns.tolist(),
            'categorical_columns': df.select_dtypes(include=['object']).columns.tolist(),
            'datetime_columns': df.select_dtypes(include=['datetime64']).columns.tolist(),
        }
        
        # Add basic statistics for numeric columns
        if len(info['numeric_columns']) > 0:
            info['numeric_stats'] = df[info['numeric_columns']].describe().to_dict()
        
        # Add unique counts for categorical columns
        if len(info['categorical_columns']) > 0:
            info['categorical_unique'] = {
                col: df[col].nunique() for col in info['categorical_columns']
            }
        
        self.data_info = info
        return info
