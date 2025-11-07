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
        recommendations = self._generate_recommendations(model_results)
        elements.append(Paragraph(recommendations, self.styles['Normal']))
        
        # Build PDF
        doc.build(elements)
        
        return str(report_path)
    
    def _generate_executive_summary(self, insights: dict, model_results: dict) -> str:
        """Generate executive summary"""
        data_info = insights['data_info']
        
        task_type = "Classification" if model_results['is_classification'] else "Regression"
        best_model = model_results['best_model_name']
        best_score = model_results['best_score']
        
        summary = f"""
        This report presents a comprehensive automated data science analysis. 
        The dataset contains <b>{data_info['shape'][0]:,}</b> rows and <b>{data_info['shape'][1]}</b> columns.
        After automated data cleaning and feature engineering, a <b>{task_type}</b> task was identified.
        Multiple machine learning models were trained and evaluated. The best performing model is 
        <b>{best_model}</b> with a score of <b>{best_score:.4f}</b>.
        """
        
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
        
        # Columns dropped
        if cleaning_report['columns_dropped']:
            dropped_text = f"<b>Columns Dropped:</b> {len(cleaning_report['columns_dropped'])} columns"
            elements.append(Paragraph(dropped_text, self.styles['Normal']))
        
        return elements
    
    def _generate_feature_report(self, feature_report: dict) -> list:
        """Generate feature engineering report"""
        elements = []
        
        stats_text = f"""
        <b>Original Features:</b> {feature_report['original_features']}<br/>
        <b>Engineered Features:</b> {len(feature_report['engineered_features'])}<br/>
        <b>Encoded Features:</b> {len(feature_report['encoded_features'])}<br/>
        <b>Final Selected Features:</b> {len(feature_report['selected_features'])}
        """
        elements.append(Paragraph(stats_text, self.styles['Normal']))
        
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
            if key != 'confusion_matrix':
                if isinstance(value, float):
                    metrics_text += f"• {key.replace('_', ' ').title()}: {value:.4f}<br/>"
                else:
                    metrics_text += f"• {key.replace('_', ' ').title()}: {value}<br/>"
        
        elements.append(Paragraph(metrics_text, self.styles['Normal']))
        
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
                    # Add image title
                    img_name = img_path.stem.replace('_', ' ').title()
                    elements.append(Paragraph(img_name, self.styles['SubsectionHeading']))
                    
                    # Add image (resize to fit page)
                    img = Image(str(img_path), width=6*inch, height=4*inch)
                    elements.append(img)
                    elements.append(Spacer(1, 20))
                    
                    # Page break after every 2 images
                    if len(elements) % 6 == 0:
                        elements.append(PageBreak())
                
                except Exception as e:
                    print(f"   Warning: Could not add image {img_path}: {str(e)}")
        
        return elements
    
    def _generate_recommendations(self, model_results: dict) -> str:
        """Generate recommendations based on results"""
        score = model_results['best_score']
        
        recommendations = "<b>Key Recommendations:</b><br/><br/>"
        
        # Performance-based recommendations
        if score > 0.9:
            recommendations += "• ✅ Excellent model performance! The model is ready for deployment.<br/>"
        elif score > 0.8:
            recommendations += "• ✓ Good model performance. Consider fine-tuning hyperparameters for improvement.<br/>"
        elif score > 0.7:
            recommendations += "• ⚠ Moderate performance. Consider collecting more data or engineering additional features.<br/>"
        else:
            recommendations += "• ⚠ Low performance. Review data quality and consider alternative approaches.<br/>"
        
        recommendations += "<br/>"
        recommendations += "• 📊 Regularly monitor model performance on new data.<br/>"
        recommendations += "• 🔄 Retrain the model periodically with fresh data.<br/>"
        recommendations += "• 🧪 Conduct A/B testing before full deployment.<br/>"
        recommendations += "• 📈 Track key metrics and set up alerts for performance degradation.<br/>"
        
        return recommendations
