"""
Data Cleaner Module
Automatically cleans data: handles missing values, outliers, duplicates, etc.
"""

import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer, KNNImputer
from scipy import stats

class DataCleaner:
    """
    Intelligent data cleaner with automatic cleaning strategies
    """
    
    def __init__(self):
        self.cleaning_report = {
            'duplicates_removed': 0,
            'missing_values_handled': {},
            'outliers_handled': {},
            'columns_dropped': [],
            'columns_dropped_reasons': {},  # New: detailed reasons
            'transformations': []
        }
    
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Automatically clean the dataset
        
        Args:
            df: Raw DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        df_clean = df.copy()
        
        # 1. Remove duplicates
        df_clean = self._remove_duplicates(df_clean)
        
        # 2. Handle missing values
        df_clean = self._handle_missing_values(df_clean)
        
        # 3. Handle outliers in numeric columns
        df_clean = self._handle_outliers(df_clean)
        
        # 4. Drop columns with too many missing values or single unique value
        df_clean = self._drop_useless_columns(df_clean)
        
        # 5. Fix data types
        df_clean = self._fix_data_types(df_clean)
        
        # 6. Clean text columns
        df_clean = self._clean_text_columns(df_clean)
        
        return df_clean
    
    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate rows"""
        initial_rows = len(df)
        df_clean = df.drop_duplicates()
        duplicates_removed = initial_rows - len(df_clean)
        self.cleaning_report['duplicates_removed'] = duplicates_removed
        
        if duplicates_removed > 0:
            print(f"   Removed {duplicates_removed} duplicate rows")
        
        return df_clean
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Intelligently handle missing values based on column type and missing percentage
        """
        df_clean = df.copy()
        
        for col in df_clean.columns:
            missing_count = df_clean[col].isnull().sum()
            missing_pct = (missing_count / len(df_clean)) * 100
            
            if missing_count == 0:
                continue
            
            # Strategy based on missing percentage
            if missing_pct > 50:
                # Too many missing values - will be dropped later
                self.cleaning_report['missing_values_handled'][col] = f"Too many missing ({missing_pct:.1f}%)"
                continue
            
            # Numeric columns
            if df_clean[col].dtype in [np.int64, np.float64]:
                if missing_pct < 5:
                    # Use median for small missing percentages
                    df_clean[col].fillna(df_clean[col].median(), inplace=True)
                    self.cleaning_report['missing_values_handled'][col] = "Filled with median"
                else:
                    # Use KNN imputation for larger missing percentages
                    try:
                        imputer = KNNImputer(n_neighbors=5)
                        df_clean[col] = imputer.fit_transform(df_clean[[col]])
                        self.cleaning_report['missing_values_handled'][col] = "KNN imputation"
                    except:
                        # Fallback to median
                        df_clean[col].fillna(df_clean[col].median(), inplace=True)
                        self.cleaning_report['missing_values_handled'][col] = "Filled with median (fallback)"
            
            # Categorical columns
            else:
                # Use mode (most frequent value)
                mode_value = df_clean[col].mode()
                if len(mode_value) > 0:
                    df_clean[col].fillna(mode_value[0], inplace=True)
                    self.cleaning_report['missing_values_handled'][col] = "Filled with mode"
                else:
                    df_clean[col].fillna("Unknown", inplace=True)
                    self.cleaning_report['missing_values_handled'][col] = "Filled with 'Unknown'"
        
        return df_clean
    
    def _handle_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle outliers using IQR method for numeric columns
        """
        df_clean = df.copy()
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 3 * IQR
            upper_bound = Q3 + 3 * IQR
            
            outliers_count = ((df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)).sum()
            
            if outliers_count > 0:
                # Cap outliers instead of removing them
                df_clean[col] = df_clean[col].clip(lower=lower_bound, upper=upper_bound)
                self.cleaning_report['outliers_handled'][col] = f"Capped {outliers_count} outliers"
        
        return df_clean
    
    def _drop_useless_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Drop columns that are not useful for modeling
        """
        df_clean = df.copy()
        columns_to_drop = []
        drop_reasons = {}
        
        for col in df_clean.columns:
            # Drop if too many missing values (>50%)
            missing_pct = (df_clean[col].isnull().sum() / len(df_clean)) * 100
            if missing_pct > 50:
                columns_to_drop.append(col)
                drop_reasons[col] = f"Too many missing values ({missing_pct:.1f}%)"
                continue
            
            # Drop if only one unique value
            if df_clean[col].nunique() == 1:
                columns_to_drop.append(col)
                drop_reasons[col] = "Single unique value (constant column)"
                continue
            
            # Drop if all values are unique (likely an ID column)
            if df_clean[col].nunique() == len(df_clean):
                # Exception: don't drop if it's numeric and might be useful
                if df_clean[col].dtype not in [np.int64, np.float64]:
                    columns_to_drop.append(col)
                    drop_reasons[col] = "All unique values (likely ID column)"
        
        if columns_to_drop:
            df_clean = df_clean.drop(columns=columns_to_drop)
            self.cleaning_report['columns_dropped'] = columns_to_drop
            self.cleaning_report['columns_dropped_reasons'] = drop_reasons
            print(f"   Dropped {len(columns_to_drop)} useless columns: {columns_to_drop}")
        
        return df_clean
    
    def _fix_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Automatically fix data types
        """
        df_clean = df.copy()
        
        for col in df_clean.columns:
            # Try to convert object columns to numeric if possible
            if df_clean[col].dtype == 'object':
                try:
                    df_clean[col] = pd.to_numeric(df_clean[col])
                    self.cleaning_report['transformations'].append(f"{col}: object -> numeric")
                except:
                    pass
        
        return df_clean
    
    def _clean_text_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean text columns: strip whitespace, handle case
        """
        df_clean = df.copy()
        text_cols = df_clean.select_dtypes(include=['object']).columns
        
        for col in text_cols:
            # Strip whitespace
            df_clean[col] = df_clean[col].astype(str).str.strip()
            
            # Replace empty strings with NaN
            df_clean[col] = df_clean[col].replace('', np.nan)
        
        return df_clean
    
    def get_cleaning_report(self) -> dict:
        """
        Get the cleaning report
        """
        return self.cleaning_report
