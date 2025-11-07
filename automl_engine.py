"""
AutoML Engine Module
Automatically selects and trains the best machine learning model
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, 
    mean_squared_error, mean_absolute_error, r2_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)

# Classification models
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

# Regression models
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor

import warnings
warnings.filterwarnings('ignore')

class AutoMLEngine:
    """
    Automatic Machine Learning Engine
    Tries multiple models and selects the best one
    """
    
    def __init__(self, test_size: float = 0.2, random_state: int = 42):
        self.test_size = test_size
        self.random_state = random_state
        self.best_model = None
        self.best_model_name = None
        self.best_score = None
        self.is_classification = None
        self.label_encoder = None
        self.X_test_stored = None  # Store for ROC curve calculation
        
    def find_best_model(self, df: pd.DataFrame, target_column: str) -> dict:
        """
        Automatically find the best model for the dataset
        
        Args:
            df: Engineered DataFrame
            target_column: Name of target column
            
        Returns:
            Dictionary with model results
        """
        # Separate features and target
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        # Determine if classification or regression
        self.is_classification = self._is_classification_task(y)
        
        # Encode target if classification with categorical labels
        if self.is_classification and y.dtype == 'object':
            self.label_encoder = LabelEncoder()
            y = self.label_encoder.fit_transform(y)
        
        # Check for NaN or infinite values
        if X.isnull().any().any():
            print(f"   Warning: Found NaN values in features. Filling with 0...")
            X = X.fillna(0)
        
        # Check for infinite values only in numeric columns
        numeric_cols = X.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            if np.isinf(X[numeric_cols].values).any():
                print(f"   Warning: Found infinite values in features. Replacing with large values...")
                X[numeric_cols] = X[numeric_cols].replace([np.inf, -np.inf], [1e10, -1e10])
        
        # Split data (stratified for classification if possible)
        if self.is_classification:
            # Check if stratification is possible
            # Convert to pandas Series if it's a numpy array
            if isinstance(y, np.ndarray):
                y_series = pd.Series(y)
            else:
                y_series = y
            
            min_class_count = y_series.value_counts().min()
            if min_class_count >= 2:
                # Safe to use stratified split
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=self.test_size, random_state=self.random_state, stratify=y
                )
                print(f"   Using stratified split (min class count: {min_class_count})")
            else:
                # Fall back to regular split
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=self.test_size, random_state=self.random_state
                )
                print(f"   Warning: Class with only {min_class_count} sample(s) - using regular split")
        else:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=self.test_size, random_state=self.random_state
            )
        
        # Store X_test for later use (ROC curve)
        self.X_test_stored = X_test
        
        print(f"   Task type: {'Classification' if self.is_classification else 'Regression'}")
        print(f"   Training samples: {len(X_train)}, Test samples: {len(X_test)}")
        
        # Get models to try
        models = self._get_models()
        
        # Train and evaluate each model
        results = []
        for name, model in models.items():
            try:
                print(f"   Training {name}...", end=' ')
                
                # Train model
                model.fit(X_train, y_train)
                
                # Predict
                y_pred = model.predict(X_test)
                
                # Evaluate
                if self.is_classification:
                    score = accuracy_score(y_test, y_pred)
                    metric_name = "Accuracy"
                else:
                    score = r2_score(y_test, y_pred)
                    metric_name = "R² Score"
                
                results.append({
                    'model_name': name,
                    'model': model,
                    'score': score,
                    'y_pred': y_pred
                })
                
                print(f"{metric_name}: {score:.4f}")
                
            except Exception as e:
                print(f"Failed - {type(e).__name__}: {str(e)[:100]}")
                continue
        
        # Select best model
        if not results:
            raise Exception("No models were successfully trained")
        
        best_result = max(results, key=lambda x: x['score'])
        self.best_model = best_result['model']
        self.best_model_name = best_result['model_name']
        self.best_score = best_result['score']
        
        # Get detailed metrics for best model
        y_pred_best = best_result['y_pred']
        
        if self.is_classification:
            metrics = self._get_classification_metrics(y_test, y_pred_best)
        else:
            metrics = self._get_regression_metrics(y_test, y_pred_best)
        
        # Feature importance (if available)
        feature_importance = self._get_feature_importance(X.columns)
        
        return {
            'best_model_name': self.best_model_name,
            'best_score': self.best_score,
            'best_model': self.best_model,
            'is_classification': self.is_classification,
            'all_results': results,
            'metrics': metrics,
            'feature_importance': feature_importance,
            'X_test': X_test,
            'y_test': y_test,
            'y_pred': y_pred_best,
            'label_encoder': self.label_encoder
        }
    
    def _is_classification_task(self, y: pd.Series) -> bool:
        """
        Determine if the task is classification or regression
        """
        # If target is object/string, it's classification
        if y.dtype == 'object':
            return True
        
        # If number of unique values is small, it's classification
        unique_count = y.nunique()
        if unique_count < 20:
            return True
        
        # Otherwise, it's regression
        return False
    
    def _get_models(self) -> dict:
        """
        Get dictionary of models to try
        """
        if self.is_classification:
            return {
                'Random Forest': RandomForestClassifier(n_estimators=100, random_state=self.random_state, n_jobs=-1),
                'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=self.random_state),
                'Logistic Regression': LogisticRegression(max_iter=1000, random_state=self.random_state),
                'Decision Tree': DecisionTreeClassifier(random_state=self.random_state),
                'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5),
                'Naive Bayes': GaussianNB(),
                'AdaBoost': AdaBoostClassifier(n_estimators=100, random_state=self.random_state)
            }
        else:
            return {
                'Random Forest': RandomForestRegressor(n_estimators=100, random_state=self.random_state, n_jobs=-1),
                'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=self.random_state),
                'Linear Regression': LinearRegression(),
                'Ridge Regression': Ridge(random_state=self.random_state),
                'Lasso Regression': Lasso(random_state=self.random_state),
                'Decision Tree': DecisionTreeRegressor(random_state=self.random_state),
                'K-Nearest Neighbors': KNeighborsRegressor(n_neighbors=5),
                'AdaBoost': AdaBoostRegressor(n_estimators=100, random_state=self.random_state)
            }
    
    def _get_classification_metrics(self, y_test, y_pred) -> dict:
        """
        Get detailed classification metrics
        """
        # Handle multi-class vs binary
        n_classes = len(np.unique(y_test))
        average = 'binary' if n_classes == 2 else 'weighted'
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average=average, zero_division=0),
            'recall': recall_score(y_test, y_pred, average=average, zero_division=0),
            'f1_score': f1_score(y_test, y_pred, average=average, zero_division=0),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }
        
        # Add ROC AUC for binary classification
        if n_classes == 2:
            try:
                # Get probability predictions if available
                if hasattr(self.best_model, 'predict_proba'):
                    y_proba = self.best_model.predict_proba(self.X_test_stored)[:, 1]
                    metrics['roc_auc'] = roc_auc_score(y_test, y_proba)
                    fpr, tpr, thresholds = roc_curve(y_test, y_proba)
                    metrics['roc_curve'] = {
                        'fpr': fpr.tolist(),
                        'tpr': tpr.tolist()
                    }
                else:
                    metrics['roc_auc'] = roc_auc_score(y_test, y_pred)
            except:
                metrics['roc_auc'] = None
        
        return metrics
    
    def _get_regression_metrics(self, y_test, y_pred) -> dict:
        """
        Get detailed regression metrics
        """
        return {
            'r2_score': r2_score(y_test, y_pred),
            'mean_squared_error': mean_squared_error(y_test, y_pred),
            'root_mean_squared_error': np.sqrt(mean_squared_error(y_test, y_pred)),
            'mean_absolute_error': mean_absolute_error(y_test, y_pred)
        }
    
    def _get_feature_importance(self, feature_names) -> dict:
        """
        Get feature importance if available
        """
        if hasattr(self.best_model, 'feature_importances_'):
            importances = self.best_model.feature_importances_
            feature_importance = dict(zip(feature_names, importances))
            # Sort by importance
            feature_importance = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True))
            return feature_importance
        elif hasattr(self.best_model, 'coef_'):
            # For linear models
            importances = np.abs(self.best_model.coef_)
            if len(importances.shape) > 1:
                importances = importances[0]
            feature_importance = dict(zip(feature_names, importances))
            feature_importance = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True))
            return feature_importance
        else:
            return {}
