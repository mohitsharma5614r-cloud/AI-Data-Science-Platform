"""
Feature Engineering Module
Automatically creates new features from existing data
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from sklearn.feature_selection import SelectKBest, f_classif, f_regression, mutual_info_classif, mutual_info_regression

class FeatureEngineer:
    """
    Intelligent feature engineering with automatic feature creation and selection
    """
    
    def __init__(self):
        self.feature_report = {
            'original_features': 0,
            'engineered_features': [],
            'encoded_features': [],
            'selected_features': [],
            'dropped_features': [],
            'interaction_features': [],
            'polynomial_features': [],
            'aggregation_features': [],
            'encoding_details': {},
            'scaling_method': None
        }
        self.encoders = {}
        self.scaler = None
    
    def engineer_features(self, df: pd.DataFrame, target_column: str) -> pd.DataFrame:
        """
        Automatically engineer features
        
        Args:
            df: Cleaned DataFrame
            target_column: Name of target column
            
        Returns:
            DataFrame with engineered features
        """
        df_eng = df.copy()
        self.feature_report['original_features'] = len(df_eng.columns) - 1  # Exclude target
        
        # Separate features and target
        if target_column not in df_eng.columns:
            raise ValueError(f"Target column '{target_column}' not found in DataFrame")
        
        # 1. Create interaction features
        df_eng = self._create_interaction_features(df_eng, target_column)
        
        # 2. Create polynomial features for numeric columns
        df_eng = self._create_polynomial_features(df_eng, target_column)
        
        # 3. Create aggregation features
        df_eng = self._create_aggregation_features(df_eng, target_column)
        
        # 4. Encode categorical variables
        df_eng = self._encode_categorical(df_eng, target_column)
        
        # 5. Scale numeric features
        df_eng = self._scale_features(df_eng, target_column)
        
        # 6. Feature selection (keep most important features)
        df_eng = self._select_features(df_eng, target_column)
        
        # 7. Final cleanup - remove any NaN or infinite values
        df_eng = self._final_cleanup(df_eng)
        
        return df_eng
    
    def _create_interaction_features(self, df: pd.DataFrame, target_column: str) -> pd.DataFrame:
        """
        Create interaction features between numeric columns
        """
        df_eng = df.copy()
        numeric_cols = df_eng.select_dtypes(include=[np.number]).columns.tolist()
        
        # Remove target from numeric columns
        if target_column in numeric_cols:
            numeric_cols.remove(target_column)
        
        # Limit to top 5 numeric columns to avoid explosion
        numeric_cols = numeric_cols[:5]
        
        # Create interactions
        for i, col1 in enumerate(numeric_cols):
            for col2 in numeric_cols[i+1:]:
                # Multiplication
                new_col = f"{col1}_x_{col2}"
                df_eng[new_col] = df_eng[col1] * df_eng[col2]
                self.feature_report['engineered_features'].append(new_col)
                self.feature_report['interaction_features'].append(new_col)
                
                # Division (avoid division by zero)
                new_col = f"{col1}_div_{col2}"
                df_eng[new_col] = df_eng[col1] / (df_eng[col2] + 1e-5)
                self.feature_report['engineered_features'].append(new_col)
                self.feature_report['interaction_features'].append(new_col)
        
        return df_eng
    
    def _create_polynomial_features(self, df: pd.DataFrame, target_column: str) -> pd.DataFrame:
        """
        Create polynomial features (squared, cubed) for numeric columns
        """
        df_eng = df.copy()
        numeric_cols = df_eng.select_dtypes(include=[np.number]).columns.tolist()
        
        # Remove target from numeric columns
        if target_column in numeric_cols:
            numeric_cols.remove(target_column)
        
        # Limit to top 5 numeric columns
        numeric_cols = numeric_cols[:5]
        
        for col in numeric_cols:
            # Squared
            new_col = f"{col}_squared"
            df_eng[new_col] = df_eng[col] ** 2
            self.feature_report['engineered_features'].append(new_col)
            self.feature_report['polynomial_features'].append(new_col)
            
            # Square root (for positive values)
            if (df_eng[col] >= 0).all():
                new_col = f"{col}_sqrt"
                df_eng[new_col] = np.sqrt(df_eng[col])
                self.feature_report['engineered_features'].append(new_col)
                self.feature_report['polynomial_features'].append(new_col)
        
        return df_eng
    
    def _create_aggregation_features(self, df: pd.DataFrame, target_column: str) -> pd.DataFrame:
        """
        Create aggregation features across numeric columns
        """
        df_eng = df.copy()
        numeric_cols = df_eng.select_dtypes(include=[np.number]).columns.tolist()
        
        # Remove target from numeric columns
        if target_column in numeric_cols:
            numeric_cols.remove(target_column)
        
        if len(numeric_cols) >= 2:
            # Sum of all numeric features
            df_eng['numeric_sum'] = df_eng[numeric_cols].sum(axis=1)
            self.feature_report['engineered_features'].append('numeric_sum')
            self.feature_report['aggregation_features'].append('numeric_sum')
            
            # Mean of all numeric features
            df_eng['numeric_mean'] = df_eng[numeric_cols].mean(axis=1)
            self.feature_report['engineered_features'].append('numeric_mean')
            self.feature_report['aggregation_features'].append('numeric_mean')
            
            # Standard deviation
            df_eng['numeric_std'] = df_eng[numeric_cols].std(axis=1)
            self.feature_report['engineered_features'].append('numeric_std')
            self.feature_report['aggregation_features'].append('numeric_std')
        
        return df_eng
    
    def _encode_categorical(self, df: pd.DataFrame, target_column: str) -> pd.DataFrame:
        """
        Encode categorical variables using Label Encoding or One-Hot Encoding
        """
        df_eng = df.copy()
        categorical_cols = df_eng.select_dtypes(include=['object']).columns.tolist()
        
        # Remove target if it's categorical
        if target_column in categorical_cols:
            categorical_cols.remove(target_column)
        
        for col in categorical_cols:
            unique_count = df_eng[col].nunique()
            
            # One-hot encoding for low cardinality (< 10 unique values)
            if unique_count < 10:
                dummies = pd.get_dummies(df_eng[col], prefix=col, drop_first=True)
                df_eng = pd.concat([df_eng, dummies], axis=1)
                df_eng = df_eng.drop(columns=[col])
                self.feature_report['encoded_features'].append(f"{col} (one-hot)")
                self.feature_report['encoding_details'][col] = f"One-hot encoding ({unique_count} categories)"
            
            # Label encoding for high cardinality
            else:
                le = LabelEncoder()
                df_eng[col] = le.fit_transform(df_eng[col].astype(str))
                self.encoders[col] = le
                self.feature_report['encoded_features'].append(f"{col} (label)")
                self.feature_report['encoding_details'][col] = f"Label encoding ({unique_count} categories)"
        
        return df_eng
    
    def _scale_features(self, df: pd.DataFrame, target_column: str) -> pd.DataFrame:
        """
        Scale numeric features using StandardScaler
        """
        df_eng = df.copy()
        
        # Get all numeric columns except target
        numeric_cols = df_eng.select_dtypes(include=[np.number]).columns.tolist()
        if target_column in numeric_cols:
            numeric_cols.remove(target_column)
        
        if len(numeric_cols) > 0:
            scaler = StandardScaler()
            df_eng[numeric_cols] = scaler.fit_transform(df_eng[numeric_cols])
            self.scaler = scaler
            self.feature_report['scaling_method'] = f"StandardScaler on {len(numeric_cols)} features"
        
        return df_eng
    
    def _select_features(self, df: pd.DataFrame, target_column: str, max_features: int = 50) -> pd.DataFrame:
        """
        Select the most important features using statistical tests
        """
        df_eng = df.copy()
        
        # Separate features and target
        X = df_eng.drop(columns=[target_column])
        y = df_eng[target_column]
        
        # If we have fewer features than max, keep all
        if len(X.columns) <= max_features:
            self.feature_report['selected_features'] = X.columns.tolist()
            return df_eng
        
        # Determine if classification or regression
        is_classification = y.nunique() < 20  # Heuristic
        
        # Select appropriate scoring function
        if is_classification:
            # Encode target if it's categorical
            if y.dtype == 'object':
                le = LabelEncoder()
                y = le.fit_transform(y)
            score_func = f_classif
        else:
            score_func = f_regression
        
        # Select K best features
        try:
            selector = SelectKBest(score_func=score_func, k=min(max_features, len(X.columns)))
            X_selected = selector.fit_transform(X, y)
            
            # Get selected feature names
            selected_mask = selector.get_support()
            selected_features = X.columns[selected_mask].tolist()
            dropped_features = X.columns[~selected_mask].tolist()
            
            self.feature_report['selected_features'] = selected_features
            self.feature_report['dropped_features'] = dropped_features
            
            # Create new dataframe with selected features + target
            df_eng = pd.DataFrame(X_selected, columns=selected_features)
            df_eng[target_column] = y
            
            print(f"   Selected {len(selected_features)} best features out of {len(X.columns)}")
        
        except Exception as e:
            print(f"   Feature selection failed: {str(e)}, keeping all features")
            self.feature_report['selected_features'] = X.columns.tolist()
        
        return df_eng
    
    def _final_cleanup(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Final cleanup to ensure no NaN or infinite values
        """
        df_clean = df.copy()
        
        # Replace infinite values
        df_clean = df_clean.replace([np.inf, -np.inf], np.nan)
        
        # Fill NaN values with 0
        df_clean = df_clean.fillna(0)
        
        return df_clean
    
    def get_feature_report(self) -> dict:
        """
        Get the feature engineering report
        """
        return self.feature_report
