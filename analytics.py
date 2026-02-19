import pandas as pd
import numpy as np
from scipy import stats

class StudentAnalytics:
    """Class for performing student data analytics"""
    
    def get_summary_stats(self, df):
        """Generate summary statistics for the dataset"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        summary = {
            'total_students': len(df),
            'statistics': {},
            'grade_distribution': self._get_grade_distribution(df),
            'performance_categories': self._categorize_performance(df)
        }
        
        # Calculate statistics for numeric columns
        for col in numeric_cols:
            if col in ['math', 'science', 'english', 'history', 'average_grade', 'attendance']:
                summary['statistics'][col] = {
                    'mean': float(df[col].mean()),
                    'median': float(df[col].median()),
                    'std': float(df[col].std()),
                    'min': float(df[col].min()),
                    'max': float(df[col].max()),
                    'q1': float(df[col].quantile(0.25)),
                    'q3': float(df[col].quantile(0.75))
                }
        
        return summary
    
    def _get_grade_distribution(self, df):
        """Calculate grade distribution"""
        if 'average_grade' not in df.columns:
            return {}
        
        bins = [0, 60, 70, 80, 90, 100]
        labels = ['F', 'D', 'C', 'B', 'A']
        df['grade_category'] = pd.cut(df['average_grade'], bins=bins, labels=labels, include_lowest=True)
        
        distribution = df['grade_category'].value_counts().to_dict()
        return {str(k): int(v) for k, v in distribution.items()}
    
    def _categorize_performance(self, df):
        """Categorize students by performance level"""
        if 'average_grade' not in df.columns:
            return {}
        
        categories = {
            'excellent': len(df[df['average_grade'] >= 90]),
            'good': len(df[(df['average_grade'] >= 80) & (df['average_grade'] < 90)]),
            'average': len(df[(df['average_grade'] >= 70) & (df['average_grade'] < 80)]),
            'below_average': len(df[(df['average_grade'] >= 60) & (df['average_grade'] < 70)]),
            'failing': len(df[df['average_grade'] < 60])
        }
        return categories
    
    def get_visualization_data(self, df):
        """Prepare data for various visualizations"""
        viz_data = {}
        
        # Subject-wise average scores
        subject_cols = ['math', 'science', 'english', 'history']
        if all(col in df.columns for col in subject_cols):
            viz_data['subject_averages'] = {
                col: float(df[col].mean()) for col in subject_cols
            }
        
        # Grade distribution for histogram
        if 'average_grade' in df.columns:
            hist, bins = np.histogram(df['average_grade'], bins=10, range=(0, 100))
            viz_data['grade_histogram'] = {
                'counts': hist.tolist(),
                'bins': bins.tolist()
            }
        
        # Attendance vs Performance correlation
        if 'attendance' in df.columns and 'average_grade' in df.columns:
            viz_data['attendance_vs_grade'] = {
                'attendance': df['attendance'].tolist(),
                'grades': df['average_grade'].tolist(),
                'correlation': float(df['attendance'].corr(df['average_grade']))
            }
        
        # Top performers
        if 'average_grade' in df.columns and 'student_id' in df.columns:
            top_10 = df.nlargest(10, 'average_grade')[['student_id', 'name', 'average_grade']]
            viz_data['top_performers'] = top_10.to_dict('records')
        
        # Subject-wise performance distribution
        if all(col in df.columns for col in subject_cols):
            viz_data['subject_distributions'] = {}
            for subject in subject_cols:
                viz_data['subject_distributions'][subject] = {
                    'above_80': int(len(df[df[subject] >= 80])),
                    'between_60_80': int(len(df[(df[subject] >= 60) & (df[subject] < 80)])),
                    'below_60': int(len(df[df[subject] < 60]))
                }
        
        # Study hours vs performance
        if 'study_hours' in df.columns and 'average_grade' in df.columns:
            viz_data['study_hours_impact'] = {
                'study_hours': df['study_hours'].tolist(),
                'grades': df['average_grade'].tolist(),
                'correlation': float(df['study_hours'].corr(df['average_grade']))
            }
        
        return viz_data
    
    def get_student_profile(self, df, student_id):
        """Get detailed profile for a specific student"""
        student = df[df['student_id'] == student_id]
        
        if len(student) == 0:
            return None
        
        student = student.iloc[0]
        subject_cols = ['math', 'science', 'english', 'history']
        
        # Calculate percentile rankings
        profile = {
            'student_id': student_id,
            'name': student.get('name', 'N/A'),
            'grades': {},
            'percentiles': {},
            'strengths': [],
            'weaknesses': []
        }
        
        # Add grade information
        for subject in subject_cols:
            if subject in student:
                grade = float(student[subject])
                profile['grades'][subject] = grade
                percentile = stats.percentileofscore(df[subject], grade)
                profile['percentiles'][subject] = float(percentile)
        
        # Identify strengths and weaknesses
        if profile['grades']:
            avg_grade = np.mean(list(profile['grades'].values()))
            for subject, grade in profile['grades'].items():
                if grade > avg_grade + 5:
                    profile['strengths'].append(subject)
                elif grade < avg_grade - 5:
                    profile['weaknesses'].append(subject)
        
        # Add other metrics
        if 'average_grade' in student:
            profile['overall_average'] = float(student['average_grade'])
            profile['overall_percentile'] = float(stats.percentileofscore(df['average_grade'], student['average_grade']))
        
        if 'attendance' in student:
            profile['attendance'] = float(student['attendance'])
        
        if 'study_hours' in student:
            profile['study_hours'] = float(student['study_hours'])
        
        return profile
    
    def identify_at_risk_students(self, df, threshold=65):
        """Identify students at risk of failing"""
        if 'average_grade' not in df.columns:
            return []
        
        at_risk = df[df['average_grade'] < threshold]
        return at_risk[['student_id', 'name', 'average_grade']].to_dict('records')
    
    def get_correlation_matrix(self, df):
        """Calculate correlation matrix for numeric features"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        corr_matrix = df[numeric_cols].corr()
        
        return corr_matrix.to_dict()
