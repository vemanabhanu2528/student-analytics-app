import pandas as pd
import numpy as np
from datetime import datetime
import os
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.chart import BarChart, PieChart, Reference
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

class ReportGenerator:
    """Generate reports in Excel and PDF formats"""
    
    def __init__(self):
        self.output_dir = 'reports'
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs('temp_charts', exist_ok=True)
    
    def generate_excel_report(self, df):
        """Generate comprehensive Excel report with multiple sheets"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = os.path.join(self.output_dir, f'student_analytics_{timestamp}.xlsx')
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # Sheet 1: Raw Data
            df.to_excel(writer, sheet_name='Student Data', index=False)
            
            # Sheet 2: Summary Statistics
            self._create_summary_sheet(df, writer)
            
            # Sheet 3: Subject Analysis
            self._create_subject_analysis_sheet(df, writer)
            
            # Sheet 4: Performance Categories
            self._create_performance_sheet(df, writer)
            
            # Format the workbook
            workbook = writer.book
            self._format_excel_sheets(workbook)
        
        return filepath
    
    def _create_summary_sheet(self, df, writer):
        """Create summary statistics sheet"""
        summary_data = []
        
        # Overall statistics
        summary_data.append(['OVERALL STATISTICS', ''])
        summary_data.append(['Total Students', len(df)])
        
        if 'average_grade' in df.columns:
            summary_data.append(['Average Grade', f"{df['average_grade'].mean():.2f}"])
            summary_data.append(['Median Grade', f"{df['average_grade'].median():.2f}"])
            summary_data.append(['Highest Grade', f"{df['average_grade'].max():.2f}"])
            summary_data.append(['Lowest Grade', f"{df['average_grade'].min():.2f}"])
        
        summary_data.append(['', ''])
        summary_data.append(['SUBJECT AVERAGES', ''])
        
        # Subject averages
        subject_cols = ['math', 'science', 'english', 'history']
        for subject in subject_cols:
            if subject in df.columns:
                summary_data.append([subject.capitalize(), f"{df[subject].mean():.2f}"])
        
        summary_df = pd.DataFrame(summary_data, columns=['Metric', 'Value'])
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
    
    def _create_subject_analysis_sheet(self, df, writer):
        """Create subject-wise analysis sheet"""
        subject_cols = ['math', 'science', 'english', 'history']
        analysis_data = []
        
        for subject in subject_cols:
            if subject in df.columns:
                analysis_data.append({
                    'Subject': subject.capitalize(),
                    'Mean': f"{df[subject].mean():.2f}",
                    'Median': f"{df[subject].median():.2f}",
                    'Std Dev': f"{df[subject].std():.2f}",
                    'Min': df[subject].min(),
                    'Max': df[subject].max(),
                    'Above 80': len(df[df[subject] >= 80]),
                    'Below 60': len(df[df[subject] < 60])
                })
        
        analysis_df = pd.DataFrame(analysis_data)
        analysis_df.to_excel(writer, sheet_name='Subject Analysis', index=False)
    
    def _create_performance_sheet(self, df, writer):
        """Create performance categories sheet"""
        if 'average_grade' not in df.columns:
            return
        
        # Categorize students
        excellent = df[df['average_grade'] >= 90]
        good = df[(df['average_grade'] >= 80) & (df['average_grade'] < 90)]
        average = df[(df['average_grade'] >= 70) & (df['average_grade'] < 80)]
        below_avg = df[(df['average_grade'] >= 60) & (df['average_grade'] < 70)]
        failing = df[df['average_grade'] < 60]
        
        # Create summary
        perf_data = [
            ['Category', 'Count', 'Percentage'],
            ['Excellent (90+)', len(excellent), f"{len(excellent)/len(df)*100:.1f}%"],
            ['Good (80-89)', len(good), f"{len(good)/len(df)*100:.1f}%"],
            ['Average (70-79)', len(average), f"{len(average)/len(df)*100:.1f}%"],
            ['Below Average (60-69)', len(below_avg), f"{len(below_avg)/len(df)*100:.1f}%"],
            ['Failing (<60)', len(failing), f"{len(failing)/len(df)*100:.1f}%"]
        ]
        
        perf_df = pd.DataFrame(perf_data[1:], columns=perf_data[0])
        perf_df.to_excel(writer, sheet_name='Performance Categories', index=False)
    
    def _format_excel_sheets(self, workbook):
        """Apply formatting to Excel sheets"""
        header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
        header_font = Font(bold=True, color='FFFFFF')
        
        for sheet in workbook.worksheets:
            for cell in sheet[1]:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal='center')
    
    def generate_pdf_report(self, df):
        """Generate comprehensive PDF report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = os.path.join(self.output_dir, f'student_analytics_{timestamp}.pdf')
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#366092'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#366092'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Title
        story.append(Paragraph('Student Performance Analytics Report', title_style))
        story.append(Paragraph(f'Generated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}', styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Executive Summary
        story.append(Paragraph('Executive Summary', heading_style))
        summary_text = f"""
        This report provides a comprehensive analysis of student performance data for {len(df)} students.
        The analysis includes overall performance metrics, subject-wise breakdowns, and predictive insights
        to identify at-risk students and areas for improvement.
        """
        story.append(Paragraph(summary_text, styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Overall Statistics
        story.append(Paragraph('Overall Statistics', heading_style))
        stats_data = self._prepare_stats_table(df)
        stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#366092')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(stats_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Subject Analysis
        story.append(Paragraph('Subject-wise Performance', heading_style))
        subject_data = self._prepare_subject_table(df)
        subject_table = Table(subject_data)
        subject_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#366092')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(subject_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Add charts
        chart_files = self._generate_charts(df)
        if chart_files:
            story.append(PageBreak())
            story.append(Paragraph('Visual Analysis', heading_style))
            for chart_file in chart_files:
                if os.path.exists(chart_file):
                    img = Image(chart_file, width=6*inch, height=4*inch)
                    story.append(img)
                    story.append(Spacer(1, 0.2*inch))
        
        # Performance Distribution
        story.append(PageBreak())
        story.append(Paragraph('Performance Distribution', heading_style))
        perf_data = self._prepare_performance_table(df)
        perf_table = Table(perf_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        perf_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#366092')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(perf_table)
        
        # Build PDF
        doc.build(story)
        
        # Cleanup temporary chart files
        for chart_file in chart_files:
            if os.path.exists(chart_file):
                os.remove(chart_file)
        
        return filepath
    
    def _prepare_stats_table(self, df):
        """Prepare statistics table data for PDF"""
        data = [['Metric', 'Value']]
        data.append(['Total Students', str(len(df))])
        
        if 'average_grade' in df.columns:
            data.append(['Average Grade', f"{df['average_grade'].mean():.2f}"])
            data.append(['Median Grade', f"{df['average_grade'].median():.2f}"])
            data.append(['Standard Deviation', f"{df['average_grade'].std():.2f}"])
        
        if 'attendance' in df.columns:
            data.append(['Average Attendance', f"{df['attendance'].mean():.1f}%"])
        
        return data
    
    def _prepare_subject_table(self, df):
        """Prepare subject analysis table for PDF"""
        subject_cols = ['math', 'science', 'english', 'history']
        data = [['Subject', 'Mean', 'Median', 'Std Dev', 'Above 80%', 'Below 60%']]
        
        for subject in subject_cols:
            if subject in df.columns:
                data.append([
                    subject.capitalize(),
                    f"{df[subject].mean():.2f}",
                    f"{df[subject].median():.2f}",
                    f"{df[subject].std():.2f}",
                    str(len(df[df[subject] >= 80])),
                    str(len(df[df[subject] < 60]))
                ])
        
        return data
    
    def _prepare_performance_table(self, df):
        """Prepare performance distribution table for PDF"""
        if 'average_grade' not in df.columns:
            return [['Category', 'Count', 'Percentage']]
        
        total = len(df)
        data = [['Performance Category', 'Student Count', 'Percentage']]
        
        categories = [
            ('Excellent (90+)', df['average_grade'] >= 90),
            ('Good (80-89)', (df['average_grade'] >= 80) & (df['average_grade'] < 90)),
            ('Average (70-79)', (df['average_grade'] >= 70) & (df['average_grade'] < 80)),
            ('Below Average (60-69)', (df['average_grade'] >= 60) & (df['average_grade'] < 70)),
            ('Failing (<60)', df['average_grade'] < 60)
        ]
        
        for category, condition in categories:
            count = len(df[condition])
            percentage = f"{count/total*100:.1f}%"
            data.append([category, str(count), percentage])
        
        return data
    
    def _generate_charts(self, df):
        """Generate charts for PDF report"""
        chart_files = []
        
        try:
            # Chart 1: Subject averages
            subject_cols = ['math', 'science', 'english', 'history']
            if all(col in df.columns for col in subject_cols):
                fig, ax = plt.subplots(figsize=(10, 6))
                averages = [df[col].mean() for col in subject_cols]
                ax.bar(subject_cols, averages, color='#366092')
                ax.set_ylabel('Average Score')
                ax.set_title('Subject-wise Average Performance')
                ax.set_ylim(0, 100)
                chart_file = 'temp_charts/subject_averages.png'
                plt.savefig(chart_file, bbox_inches='tight', dpi=100)
                plt.close()
                chart_files.append(chart_file)
            
            # Chart 2: Grade distribution
            if 'average_grade' in df.columns:
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.hist(df['average_grade'], bins=20, color='#4CAF50', edgecolor='black')
                ax.set_xlabel('Grade')
                ax.set_ylabel('Number of Students')
                ax.set_title('Grade Distribution')
                chart_file = 'temp_charts/grade_distribution.png'
                plt.savefig(chart_file, bbox_inches='tight', dpi=100)
                plt.close()
                chart_files.append(chart_file)
        
        except Exception as e:
            print(f"Error generating charts: {e}")
        
        return chart_files
