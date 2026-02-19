import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
import joblib
import os

class PerformancePredictor:
    """Machine Learning model for predicting student performance"""
    
    def __init__(self):
        self.regression_model = None
        self.classification_model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_columns = ['math', 'science', 'english', 'history', 'attendance', 'study_hours']
        self.model_accuracy = {}
    
    def prepare_features(self, df):
        """Prepare features for ML model"""
        # Select relevant features
        available_features = [col for col in self.feature_columns if col in df.columns]
        
        if len(available_features) < 3:
            raise ValueError("Insufficient features for prediction")
        
        X = df[available_features].copy()
        
        # Handle missing values
        X = X.fillna(X.mean())
        
        return X, available_features
    
    def train(self, df):
        """Train the ML models"""
        # Prepare features
        X, feature_cols = self.prepare_features(df)
        
        # Calculate average grade if not present
        if 'average_grade' not in df.columns:
            subject_cols = [col for col in ['math', 'science', 'english', 'history'] if col in df.columns]
            df['average_grade'] = df[subject_cols].mean(axis=1)
        
        y_regression = df['average_grade']
        
        # Create classification target (Pass/Fail)
        y_classification = (df['average_grade'] >= 60).astype(int)
        
        # Split data
        X_train, X_test, y_reg_train, y_reg_test = train_test_split(
            X, y_regression, test_size=0.2, random_state=42
        )
        _, _, y_clf_train, y_clf_test = train_test_split(
            X, y_classification, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train regression model (predict grade)
        self.regression_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        self.regression_model.fit(X_train_scaled, y_reg_train)
        
        # Train classification model (predict pass/fail)
        self.classification_model = GradientBoostingClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=42
        )
        self.classification_model.fit(X_train_scaled, y_clf_train)
        
        # Evaluate models
        reg_pred = self.regression_model.predict(X_test_scaled)
        clf_pred = self.classification_model.predict(X_test_scaled)
        
        self.model_accuracy = {
            'regression_r2': float(r2_score(y_reg_test, reg_pred)),
            'regression_rmse': float(np.sqrt(mean_squared_error(y_reg_test, reg_pred))),
            'classification_accuracy': float(accuracy_score(y_clf_test, clf_pred))
        }
        
        self.is_trained = True
        self.trained_features = feature_cols
        
        return self.model_accuracy
    
    def predict_grade(self, student_features):
        """Predict grade for a single student"""
        if not self.is_trained:
            raise ValueError("Model not trained yet")
        
        # Prepare features
        features = np.array([student_features[col] for col in self.trained_features]).reshape(1, -1)
        features_scaled = self.scaler.transform(features)
        
        # Predict
        predicted_grade = self.regression_model.predict(features_scaled)[0]
        pass_probability = self.classification_model.predict_proba(features_scaled)[0][1]
        
        return {
            'predicted_grade': float(predicted_grade),
            'pass_probability': float(pass_probability),
            'will_pass': pass_probability >= 0.5
        }
    
    def predict_all(self, df):
        """Predict performance for all students"""
        if not self.is_trained:
            self.train(df)
        
        X, _ = self.prepare_features(df)
        X_scaled = self.scaler.transform(X)
        
        # Make predictions
        predicted_grades = self.regression_model.predict(X_scaled)
        pass_probabilities = self.classification_model.predict_proba(X_scaled)[:, 1]
        
        # Combine with student IDs
        predictions = []
        for i, row in df.iterrows():
            pred = {
                'student_id': row.get('student_id', f'Student_{i}'),
                'name': row.get('name', 'N/A'),
                'current_grade': float(row.get('average_grade', 0)),
                'predicted_grade': float(predicted_grades[i]),
                'pass_probability': float(pass_probabilities[i]),
                'improvement_needed': float(max(0, 60 - predicted_grades[i])),
                'risk_level': self._categorize_risk(pass_probabilities[i])
            }
            predictions.append(pred)
        
        return predictions
    
    def _categorize_risk(self, pass_probability):
        """Categorize student risk level"""
        if pass_probability >= 0.8:
            return 'Low'
        elif pass_probability >= 0.6:
            return 'Medium'
        else:
            return 'High'
    
    def get_feature_importance(self):
        """Get feature importance from the regression model"""
        if not self.is_trained:
            return {}
        
        importance = dict(zip(
            self.trained_features,
            [float(x) for x in self.regression_model.feature_importances_]
        ))
        
        # Sort by importance
        return dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))
    
    def get_accuracy(self):
        """Return model accuracy metrics"""
        return self.model_accuracy
    
    def save_model(self, filepath='models/'):
        """Save trained model to disk"""
        if not self.is_trained:
            raise ValueError("No model to save")
        
        os.makedirs(filepath, exist_ok=True)
        joblib.dump(self.regression_model, os.path.join(filepath, 'regression_model.pkl'))
        joblib.dump(self.classification_model, os.path.join(filepath, 'classification_model.pkl'))
        joblib.dump(self.scaler, os.path.join(filepath, 'scaler.pkl'))
    
    def load_model(self, filepath='models/'):
        """Load trained model from disk"""
        self.regression_model = joblib.load(os.path.join(filepath, 'regression_model.pkl'))
        self.classification_model = joblib.load(os.path.join(filepath, 'classification_model.pkl'))
        self.scaler = joblib.load(os.path.join(filepath, 'scaler.pkl'))
        self.is_trained = True
    
    def reset(self):
        """Reset the model"""
        self.regression_model = None
        self.classification_model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.model_accuracy = {}
