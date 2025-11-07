"""
Visualizer Module
Automatically generates comprehensive visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

class Visualizer:
    """
    Automatic visualization generator
    """
    
    def __init__(self, output_dir: str = "visualizations"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.plots = []
    
    def generate_all_plots(self, raw_data: pd.DataFrame, cleaned_data: pd.DataFrame, 
                          engineered_data: pd.DataFrame, target_column: str, 
                          model_results: dict):
        """
        Generate all visualizations
        """
        # 1. Data overview plots
        self._plot_missing_values(raw_data)
        self._plot_data_types(raw_data)
        
        # 2. Target distribution
        self._plot_target_distribution(cleaned_data, target_column)
        
        # 3. Correlation heatmap
        self._plot_correlation_heatmap(cleaned_data, target_column)
        
        # 4. Feature distributions
        self._plot_feature_distributions(cleaned_data, target_column)
        
        # 5. Model comparison
        self._plot_model_comparison(model_results)
        
        # 6. Feature importance
        self._plot_feature_importance(model_results)
        
        # 7. Model performance
        if model_results['is_classification']:
            self._plot_confusion_matrix(model_results)
        else:
            self._plot_regression_results(model_results)
        
        # 8. Prediction vs Actual
        self._plot_predictions(model_results)
        
        print(f"   Generated {len(self.plots)} visualizations")
    
    def _plot_missing_values(self, df: pd.DataFrame):
        """Plot missing values heatmap"""
        plt.figure(figsize=(12, 6))
        missing = df.isnull().sum()
        missing = missing[missing > 0].sort_values(ascending=False)
        
        if len(missing) > 0:
            plt.bar(range(len(missing)), missing.values)
            plt.xticks(range(len(missing)), missing.index, rotation=45, ha='right')
            plt.xlabel('Columns')
            plt.ylabel('Missing Values Count')
            plt.title('Missing Values by Column')
            plt.tight_layout()
            
            filepath = self.output_dir / "01_missing_values.png"
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            self.plots.append(str(filepath))
    
    def _plot_data_types(self, df: pd.DataFrame):
        """Plot data types distribution"""
        plt.figure(figsize=(8, 6))
        dtype_counts = df.dtypes.value_counts()
        
        colors = sns.color_palette("husl", len(dtype_counts))
        plt.pie(dtype_counts.values, labels=dtype_counts.index, autopct='%1.1f%%', colors=colors)
        plt.title('Data Types Distribution')
        plt.tight_layout()
        
        filepath = self.output_dir / "02_data_types.png"
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        self.plots.append(str(filepath))
    
    def _plot_target_distribution(self, df: pd.DataFrame, target_column: str):
        """Plot target variable distribution"""
        plt.figure(figsize=(10, 6))
        
        if df[target_column].dtype in [np.int64, np.float64]:
            # Numeric target - histogram
            plt.hist(df[target_column].dropna(), bins=50, edgecolor='black', alpha=0.7)
            plt.xlabel(target_column)
            plt.ylabel('Frequency')
            plt.title(f'Distribution of {target_column}')
        else:
            # Categorical target - bar plot
            value_counts = df[target_column].value_counts()
            plt.bar(range(len(value_counts)), value_counts.values)
            plt.xticks(range(len(value_counts)), value_counts.index, rotation=45, ha='right')
            plt.xlabel(target_column)
            plt.ylabel('Count')
            plt.title(f'Distribution of {target_column}')
        
        plt.tight_layout()
        filepath = self.output_dir / "03_target_distribution.png"
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        self.plots.append(str(filepath))
    
    def _plot_correlation_heatmap(self, df: pd.DataFrame, target_column: str):
        """Plot correlation heatmap for numeric features"""
        numeric_df = df.select_dtypes(include=[np.number])
        
        if len(numeric_df.columns) > 1:
            plt.figure(figsize=(12, 10))
            
            # Limit to top 20 features for readability
            if len(numeric_df.columns) > 20:
                # Select features most correlated with target
                if target_column in numeric_df.columns:
                    correlations = numeric_df.corr()[target_column].abs().sort_values(ascending=False)
                    top_features = correlations.head(20).index.tolist()
                    numeric_df = numeric_df[top_features]
            
            corr_matrix = numeric_df.corr()
            sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', center=0, 
                       square=True, linewidths=0.5)
            plt.title('Feature Correlation Heatmap')
            plt.tight_layout()
            
            filepath = self.output_dir / "04_correlation_heatmap.png"
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            self.plots.append(str(filepath))
    
    def _plot_feature_distributions(self, df: pd.DataFrame, target_column: str):
        """Plot distributions of top numeric features"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if target_column in numeric_cols:
            numeric_cols.remove(target_column)
        
        # Plot top 6 features
        top_features = numeric_cols[:6]
        
        if len(top_features) > 0:
            fig, axes = plt.subplots(2, 3, figsize=(15, 10))
            axes = axes.flatten()
            
            for idx, col in enumerate(top_features):
                axes[idx].hist(df[col].dropna(), bins=30, edgecolor='black', alpha=0.7)
                axes[idx].set_xlabel(col)
                axes[idx].set_ylabel('Frequency')
                axes[idx].set_title(f'Distribution of {col}')
            
            # Hide unused subplots
            for idx in range(len(top_features), 6):
                axes[idx].axis('off')
            
            plt.tight_layout()
            filepath = self.output_dir / "05_feature_distributions.png"
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            self.plots.append(str(filepath))
    
    def _plot_model_comparison(self, model_results: dict):
        """Plot comparison of all models"""
        all_results = model_results['all_results']
        
        if len(all_results) > 1:
            plt.figure(figsize=(12, 6))
            
            model_names = [r['model_name'] for r in all_results]
            scores = [r['score'] for r in all_results]
            
            colors = ['green' if name == model_results['best_model_name'] else 'skyblue' 
                     for name in model_names]
            
            plt.bar(range(len(model_names)), scores, color=colors)
            plt.xticks(range(len(model_names)), model_names, rotation=45, ha='right')
            plt.ylabel('Score')
            plt.title('Model Performance Comparison')
            plt.axhline(y=model_results['best_score'], color='r', linestyle='--', 
                       label=f"Best: {model_results['best_model_name']}")
            plt.legend()
            plt.tight_layout()
            
            filepath = self.output_dir / "06_model_comparison.png"
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            self.plots.append(str(filepath))
    
    def _plot_feature_importance(self, model_results: dict):
        """Plot feature importance"""
        feature_importance = model_results.get('feature_importance', {})
        
        if feature_importance:
            # Get top 15 features
            top_features = dict(list(feature_importance.items())[:15])
            
            plt.figure(figsize=(10, 8))
            features = list(top_features.keys())
            importances = list(top_features.values())
            
            plt.barh(range(len(features)), importances)
            plt.yticks(range(len(features)), features)
            plt.xlabel('Importance')
            plt.title('Top 15 Feature Importances')
            plt.tight_layout()
            
            filepath = self.output_dir / "07_feature_importance.png"
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            self.plots.append(str(filepath))
    
    def _plot_confusion_matrix(self, model_results: dict):
        """Plot confusion matrix for classification"""
        cm = np.array(model_results['metrics']['confusion_matrix'])
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', square=True)
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.title('Confusion Matrix')
        plt.tight_layout()
        
        filepath = self.output_dir / "08_confusion_matrix.png"
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        self.plots.append(str(filepath))
    
    def _plot_regression_results(self, model_results: dict):
        """Plot regression metrics"""
        metrics = model_results['metrics']
        
        plt.figure(figsize=(10, 6))
        metric_names = ['R² Score', 'RMSE', 'MAE']
        metric_values = [
            metrics['r2_score'],
            metrics['root_mean_squared_error'],
            metrics['mean_absolute_error']
        ]
        
        # Normalize RMSE and MAE for visualization
        max_val = max(metric_values[1:])
        normalized_values = [metric_values[0], 
                           metric_values[1]/max_val, 
                           metric_values[2]/max_val]
        
        plt.bar(metric_names, normalized_values, color=['green', 'orange', 'blue'])
        plt.ylabel('Normalized Score')
        plt.title('Regression Metrics (Normalized)')
        plt.tight_layout()
        
        filepath = self.output_dir / "08_regression_metrics.png"
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        self.plots.append(str(filepath))
    
    def _plot_predictions(self, model_results: dict):
        """Plot predictions vs actual values"""
        y_test = model_results['y_test']
        y_pred = model_results['y_pred']
        
        plt.figure(figsize=(10, 6))
        
        if model_results['is_classification']:
            # For classification, show sample predictions
            sample_size = min(50, len(y_test))
            indices = range(sample_size)
            
            plt.scatter(indices, y_test[:sample_size], label='Actual', alpha=0.6, s=100)
            plt.scatter(indices, y_pred[:sample_size], label='Predicted', alpha=0.6, s=100, marker='x')
            plt.xlabel('Sample Index')
            plt.ylabel('Class')
            plt.title('Predictions vs Actual (Sample)')
            plt.legend()
        else:
            # For regression, scatter plot
            plt.scatter(y_test, y_pred, alpha=0.5)
            plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 
                    'r--', lw=2, label='Perfect Prediction')
            plt.xlabel('Actual Values')
            plt.ylabel('Predicted Values')
            plt.title('Predictions vs Actual Values')
            plt.legend()
        
        plt.tight_layout()
        filepath = self.output_dir / "09_predictions.png"
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        self.plots.append(str(filepath))
