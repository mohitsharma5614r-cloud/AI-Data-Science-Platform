"""
Report Generator Module
Generates comprehensive PDF reports with all findings
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
from pathlib import Path
import json

class ReportGenerator:
    """
    Automatic PDF report generator
    """
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section heading
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2ca02c'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Subsection heading
        self.styles.add(ParagraphStyle(
            name='SubsectionHeading',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#ff7f0e'),
            spaceAfter=10,
            fontName='Helvetica-Bold'
        ))
    
    def generate_report(self, csv_path: str, insights: dict, 
                       model_results: dict, visualizations_dir: str) -> str:
        """
        Generate comprehensive PDF report
        
        Args:
            csv_path: Path to original CSV
            insights: Dictionary with all insights
            model_results: Model training results
            visualizations_dir: Directory with visualization images
            
        Returns:
            Path to generated PDF report
        """
        # Create PDF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.output_dir / f"data_science_report_{timestamp}.pdf"
        
        doc = SimpleDocTemplate(
            str(report_path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Title
        elements.append(Paragraph("🤖 Autonomous Data Science Report", self.styles['CustomTitle']))
        elements.append(Spacer(1, 12))
        
        # Metadata
        metadata_text = f"""
        <b>Generated:</b> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}<br/>
        <b>Dataset:</b> {Path(csv_path).name}<br/>
        <b>Status:</b> <font color="green">✓ Analysis Complete</font>
        """
        elements.append(Paragraph(metadata_text, self.styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Executive Summary
        elements.append(Paragraph("📊 Executive Summary", self.styles['SectionHeading']))
        summary = self._generate_executive_summary(insights, model_results)
        elements.append(Paragraph(summary, self.styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Dataset Summary Table
        elements.append(Paragraph("📊 Dataset Summary", self.styles['SectionHeading']))
        summary_table = self._generate_dataset_summary_table(insights['data_info'])
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
        
        # Data Overview
        elements.append(Paragraph("📂 Data Overview", self.styles['SectionHeading']))
        data_overview = self._generate_data_overview(insights['data_info'])
        for item in data_overview:
            elements.append(item)
            elements.append(Spacer(1, 10))
        
        # Data Cleaning Report
        elements.append(PageBreak())
        elements.append(Paragraph("🧹 Data Cleaning Report", self.styles['SectionHeading']))
        cleaning_report = self._generate_cleaning_report(insights['cleaning_report'])
        for item in cleaning_report:
            elements.append(item)
            elements.append(Spacer(1, 10))
        
        # Feature Engineering Report
        elements.append(Paragraph("⚙️ Feature Engineering Report", self.styles['SectionHeading']))
        feature_report = self._generate_feature_report(insights['feature_report'])
        for item in feature_report:
            elements.append(item)
            elements.append(Spacer(1, 10))
        
        # Model Performance
        elements.append(PageBreak())
        elements.append(Paragraph("🤖 Model Performance", self.styles['SectionHeading']))
        model_report = self._generate_model_report(model_results)
        for item in model_report:
            elements.append(item)
            elements.append(Spacer(1, 10))
        
        # Visualizations
        elements.append(PageBreak())
        elements.append(Paragraph("📈 Visualizations", self.styles['SectionHeading']))
        viz_elements = self._add_visualizations(visualizations_dir)
        for item in viz_elements:
            elements.append(item)
        
        # Recommendations
        elements.append(PageBreak())
        elements.append(Paragraph("💡 Recommendations", self.styles['SectionHeading']))
        recommendations = self._generate_recommendations(model_results, insights)
        elements.append(Paragraph(recommendations, self.styles['Normal']))
        
        # Build PDF
        doc.build(elements)
        
        return str(report_path)
    
    def _generate_dataset_summary_table(self, data_info: dict) -> Table:
        """Generate dataset summary table"""
        data = [
            ['Metric', 'Value'],
            ['Total Rows', f"{data_info['shape'][0]:,}"],
            ['Total Columns', f"{data_info['shape'][1]}"],
            ['Numeric Columns', f"{len(data_info['numeric_columns'])}"],
            ['Categorical Columns', f"{len(data_info['categorical_columns'])}"],
            ['Memory Usage', f"{data_info['memory_usage']:.2f} MB"],
            ['Missing Cells', f"{sum(data_info['missing_values'].values()):,}"],
            ['Duplicate Rows', '0']  # Will be updated from cleaning report
        ]
        
        table = Table(data, colWidths=[3*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2a5298')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        return table
    
    def _generate_executive_summary(self, insights: dict, model_results: dict) -> str:
        """Generate enhanced executive summary with key insights"""
        data_info = insights['data_info']
        cleaning_report = insights['cleaning_report']
        feature_report = insights['feature_report']
        
        task_type = "Classification" if model_results['is_classification'] else "Regression"
        best_model = model_results['best_model_name']
        best_score = model_results['best_score']
        
        # Calculate key metrics
        num_numeric = len(data_info['numeric_columns'])
        num_categorical = len(data_info['categorical_columns'])
        total_missing = sum(data_info['missing_values'].values())
        missing_pct = (total_missing / (data_info['shape'][0] * data_info['shape'][1])) * 100 if data_info['shape'][0] > 0 else 0
        
        summary = f"""
        This report presents a comprehensive automated data science analysis performed on 
        <b>{data_info['shape'][0]:,}</b> rows and <b>{data_info['shape'][1]}</b> columns of data.
        <br/><br/>
        <b>Dataset Overview:</b><br/>
        • Numeric Features: {num_numeric}<br/>
        • Categorical Features: {num_categorical}<br/>
        • Missing Values: {total_missing:,} cells ({missing_pct:.2f}%)<br/>
        • Duplicate Rows Removed: {cleaning_report['duplicates_removed']}<br/>
        • Columns Dropped: {len(cleaning_report['columns_dropped'])}<br/>
        <br/>
        <b>Analysis Results:</b><br/>
        • Task Type: <b>{task_type}</b><br/>
        • Models Evaluated: <b>{len(model_results['all_results'])}</b><br/>
        • Best Model: <b>{best_model}</b><br/>
        • Performance Score: <b>{best_score:.4f}</b><br/>
        • Features Engineered: <b>{len(feature_report['engineered_features'])}</b><br/>
        • Final Features Selected: <b>{len(feature_report['selected_features'])}</b><br/>
        <br/>
        <b>Key Insights:</b><br/>
        """
        
        # Add specific insights
        if best_score > 0.9:
            summary += "• ✅ Excellent model performance achieved - ready for deployment<br/>"
        elif best_score > 0.8:
            summary += "• ✓ Good model performance - minor tuning recommended<br/>"
        else:
            summary += "• ⚠ Model performance needs improvement - see recommendations<br/>"
        
        if total_missing > data_info['shape'][0] * data_info['shape'][1] * 0.1:
            summary += "• ⚠ Significant missing values detected and handled<br/>"
        
        if num_categorical > num_numeric * 2:
            summary += f"• 📊 Dataset is heavily categorical ({num_categorical} vs {num_numeric} numeric)<br/>"
        
        return summary
    
    def _generate_data_overview(self, data_info: dict) -> list:
        """Generate data overview section"""
        elements = []
        
        # Basic statistics
        stats_text = f"""
        <b>Dataset Shape:</b> {data_info['shape'][0]:,} rows × {data_info['shape'][1]} columns<br/>
        <b>Memory Usage:</b> {data_info['memory_usage']:.2f} MB<br/>
        <b>Numeric Columns:</b> {len(data_info['numeric_columns'])}<br/>
        <b>Categorical Columns:</b> {len(data_info['categorical_columns'])}
        """
        elements.append(Paragraph(stats_text, self.styles['Normal']))
        
        # Missing values summary
        missing_values = data_info['missing_values']
        total_missing = sum(missing_values.values())
        
        if total_missing > 0:
            elements.append(Paragraph("<b>Missing Values:</b>", self.styles['SubsectionHeading']))
            missing_text = f"Total missing values: {total_missing:,}<br/>"
            
            # Show top 5 columns with missing values
            missing_sorted = sorted(missing_values.items(), key=lambda x: x[1], reverse=True)
            for col, count in missing_sorted[:5]:
                if count > 0:
                    pct = (count / data_info['shape'][0]) * 100
                    missing_text += f"• {col}: {count} ({pct:.1f}%)<br/>"
            
            elements.append(Paragraph(missing_text, self.styles['Normal']))
        
        return elements
    
    def _generate_cleaning_report(self, cleaning_report: dict) -> list:
        """Generate cleaning report section"""
        elements = []
        
        # Duplicates
        duplicates = cleaning_report['duplicates_removed']
        dup_text = f"<b>Duplicate Rows Removed:</b> {duplicates}"
        elements.append(Paragraph(dup_text, self.styles['Normal']))
        
        # Missing values handled
        if cleaning_report['missing_values_handled']:
            elements.append(Paragraph("<b>Missing Values Handled:</b>", self.styles['SubsectionHeading']))
            mv_text = ""
            for col, method in list(cleaning_report['missing_values_handled'].items())[:10]:
                mv_text += f"• {col}: {method}<br/>"
            elements.append(Paragraph(mv_text, self.styles['Normal']))
        
        # Outliers
        if cleaning_report['outliers_handled']:
            elements.append(Paragraph("<b>Outliers Handled:</b>", self.styles['SubsectionHeading']))
            outlier_text = ""
            for col, info in list(cleaning_report['outliers_handled'].items())[:10]:
                outlier_text += f"• {col}: {info}<br/>"
            elements.append(Paragraph(outlier_text, self.styles['Normal']))
        
        # Columns dropped with reasons
        if cleaning_report['columns_dropped']:
            elements.append(Paragraph(f"<b>Columns Dropped:</b> {len(cleaning_report['columns_dropped'])} columns", 
                                    self.styles['SubsectionHeading']))
            
            # Show detailed reasons if available
            if 'columns_dropped_reasons' in cleaning_report and cleaning_report['columns_dropped_reasons']:
                dropped_text = ""
                for col, reason in cleaning_report['columns_dropped_reasons'].items():
                    dropped_text += f"• <b>{col}</b>: {reason}<br/>"
                elements.append(Paragraph(dropped_text, self.styles['Normal']))
            else:
                # Fallback to just list
                dropped_text = ", ".join(cleaning_report['columns_dropped'])
                elements.append(Paragraph(dropped_text, self.styles['Normal']))
        
        return elements
    
    def _generate_feature_report(self, feature_report: dict) -> list:
        """Generate feature engineering report"""
        elements = []
        
        stats_text = f"""
        <b>Original Features:</b> {feature_report['original_features']}<br/>
        <b>Interaction Features Created:</b> {len(feature_report.get('interaction_features', []))}<br/>
        <b>Polynomial Features Created:</b> {len(feature_report.get('polynomial_features', []))}<br/>
        <b>Aggregation Features Created:</b> {len(feature_report.get('aggregation_features', []))}<br/>
        <b>Total Engineered Features:</b> {len(feature_report['engineered_features'])}<br/>
        <b>Encoded Features:</b> {len(feature_report['encoded_features'])}<br/>
        <b>Final Selected Features:</b> {len(feature_report['selected_features'])}
        """
        elements.append(Paragraph(stats_text, self.styles['Normal']))
        
        # Encoding details
        if 'encoding_details' in feature_report and feature_report['encoding_details']:
            elements.append(Paragraph("<b>Encoding Details:</b>", self.styles['SubsectionHeading']))
            encoding_text = ""
            for col, method in list(feature_report['encoding_details'].items())[:10]:
                encoding_text += f"• <b>{col}</b>: {method}<br/>"
            elements.append(Paragraph(encoding_text, self.styles['Normal']))
        
        # Scaling method
        if 'scaling_method' in feature_report and feature_report['scaling_method']:
            scaling_text = f"<b>Scaling:</b> {feature_report['scaling_method']}"
            elements.append(Paragraph(scaling_text, self.styles['Normal']))
        
        return elements
    
    def _generate_model_report(self, model_results: dict) -> list:
        """Generate model performance report"""
        elements = []
        
        # Best model info
        best_model_text = f"""
        <b>Best Model:</b> {model_results['best_model_name']}<br/>
        <b>Task Type:</b> {"Classification" if model_results['is_classification'] else "Regression"}<br/>
        <b>Performance Score:</b> {model_results['best_score']:.4f}
        """
        elements.append(Paragraph(best_model_text, self.styles['Normal']))
        
        # Detailed metrics
        elements.append(Paragraph("<b>Detailed Metrics:</b>", self.styles['SubsectionHeading']))
        metrics = model_results['metrics']
        
        metrics_text = ""
        for key, value in metrics.items():
            if key not in ['confusion_matrix', 'roc_curve']:
                if isinstance(value, float):
                    metrics_text += f"• {key.replace('_', ' ').title()}: {value:.4f}<br/>"
                else:
                    metrics_text += f"• {key.replace('_', ' ').title()}: {value}<br/>"
        
        elements.append(Paragraph(metrics_text, self.styles['Normal']))
        
        # Add ROC AUC if available
        if 'roc_auc' in metrics and metrics['roc_auc'] is not None:
            roc_text = f"<b>ROC AUC Score:</b> {metrics['roc_auc']:.4f}"
            elements.append(Paragraph(roc_text, self.styles['Normal']))
        
        # Model comparison table
        if len(model_results['all_results']) > 1:
            elements.append(Paragraph("<b>All Models Comparison:</b>", self.styles['SubsectionHeading']))
            
            table_data = [['Model', 'Score']]
            for result in sorted(model_results['all_results'], key=lambda x: x['score'], reverse=True):
                table_data.append([result['model_name'], f"{result['score']:.4f}"])
            
            table = Table(table_data, colWidths=[3*inch, 1.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
        
        return elements
    
    def _add_visualizations(self, visualizations_dir: str) -> list:
        """Add visualization images to report"""
        elements = []
        viz_dir = Path(visualizations_dir)
        
        if viz_dir.exists():
            image_files = sorted(viz_dir.glob("*.png"))
            
            for img_path in image_files:
                try:
                    # Add image title with better formatting
                    img_name = img_path.stem.replace('_', ' ').replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').strip().title()
                    elements.append(Paragraph(f"<b>{img_name}</b>", self.styles['SubsectionHeading']))
                    elements.append(Spacer(1, 10))
                    
                    # Add image with better sizing (maintain aspect ratio)
                    img = Image(str(img_path), width=6.5*inch, height=4.5*inch, kind='proportional')
                    elements.append(img)
                    elements.append(Spacer(1, 15))
                    
                    # Page break after every 2 images for better layout
                    if len(elements) % 6 == 0:
                        elements.append(PageBreak())
                
                except Exception as e:
                    print(f"   Warning: Could not add image {img_path}: {str(e)}")
        
        return elements
    
    def _generate_recommendations(self, model_results: dict, insights: dict) -> str:
        """Generate dataset-specific recommendations based on results"""
        score = model_results['best_score']
        data_info = insights['data_info']
        cleaning_report = insights['cleaning_report']
        feature_report = insights['feature_report']
        
        recommendations = "<b>Dataset-Specific Recommendations:</b><br/><br/>"
        
        # Performance-based recommendations
        if score > 0.9:
            recommendations += "• ✅ <b>Excellent model performance!</b> The model is ready for deployment.<br/>"
        elif score > 0.8:
            recommendations += "• ✓ <b>Good model performance.</b> Consider fine-tuning hyperparameters for improvement.<br/>"
        elif score > 0.7:
            recommendations += "• ⚠ <b>Moderate performance.</b> Consider collecting more data or engineering additional features.<br/>"
        else:
            recommendations += "• ⚠ <b>Low performance.</b> Review data quality and consider alternative approaches.<br/>"
        
        recommendations += "<br/>"
        
        # Data quality recommendations
        total_rows = data_info['shape'][0]
        if total_rows < 100:
            recommendations += "• 📊 <b>Small dataset detected.</b> Consider collecting more data for better model generalization.<br/>"
        
        # Missing values recommendations
        total_missing = sum(data_info['missing_values'].values())
        if total_missing > total_rows * 0.1:
            recommendations += "• 🔍 <b>Significant missing values detected.</b> Consider advanced imputation techniques or data collection improvements.<br/>"
        
        # Feature engineering recommendations
        num_numeric = len(data_info['numeric_columns'])
        num_categorical = len(data_info['categorical_columns'])
        
        if num_categorical > num_numeric * 2:
            recommendations += f"• 🏷️ <b>High categorical features ({num_categorical} categorical vs {num_numeric} numeric).</b> Consider using CatBoost or LightGBM for better performance.<br/>"
        
        if num_numeric == 1:
            recommendations += "• ⚠ <b>Only 1 numeric column available.</b> Model performance may be limited. Consider feature engineering or collecting more features.<br/>"
        
        # Class imbalance check (for classification)
        if model_results['is_classification'] and 'confusion_matrix' in model_results['metrics']:
            cm = model_results['metrics']['confusion_matrix']
            if len(cm) == 2:  # Binary classification
                class_0 = sum(cm[0])
                class_1 = sum(cm[1])
                imbalance_ratio = max(class_0, class_1) / (min(class_0, class_1) + 1)
                if imbalance_ratio > 3:
                    recommendations += f"• ⚖️ <b>Class imbalance detected (ratio: {imbalance_ratio:.1f}:1).</b> Consider using SMOTE, class weights, or ensemble methods.<br/>"
        
        # Dropped columns recommendations
        if len(cleaning_report['columns_dropped']) > data_info['shape'][1] * 0.3:
            recommendations += f"• 🗑️ <b>Many columns dropped ({len(cleaning_report['columns_dropped'])} columns).</b> Review data collection process to reduce missing/useless columns.<br/>"
        
        recommendations += "<br/><b>General Best Practices:</b><br/>"
        recommendations += "• 📊 Regularly monitor model performance on new data.<br/>"
        recommendations += "• 🔄 Retrain the model periodically with fresh data (recommended: monthly).<br/>"
        recommendations += "• 🧪 Conduct A/B testing before full deployment.<br/>"
        recommendations += "• 📈 Track key metrics and set up alerts for performance degradation.<br/>"
        recommendations += "• 🔒 Implement data validation pipelines to ensure data quality.<br/>"
        
        return recommendations
