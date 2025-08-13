import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
import json
from datetime import datetime

class WorkoutRecommendationModel:
    """
    Machine Learning model for recommending workout plans based on user goals and fitness data.
    This model analyzes user preferences, goals, and current fitness level to suggest optimal workout plans.
    """
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def prepare_sample_data(self):
        """
        Generate sample training data for the workout recommendation model.
        In a real application, this would come from the database.
        """
        np.random.seed(42)
        
        # Sample user data
        n_samples = 1000
        
        # User characteristics
        ages = np.random.randint(18, 65, n_samples)
        fitness_levels = np.random.choice(['beginner', 'intermediate', 'advanced'], n_samples)
        goals = np.random.choice(['weight_loss', 'muscle_gain', 'endurance', 'strength'], n_samples)
        experience_years = np.random.randint(0, 20, n_samples)
        
        # Fitness metrics
        bmi = np.random.normal(25, 5, n_samples)
        weekly_workouts = np.random.randint(1, 7, n_samples)
        avg_workout_duration = np.random.randint(20, 120, n_samples)
        
        # Create features
        data = {
            'age': ages,
            'fitness_level': fitness_levels,
            'goal': goals,
            'experience_years': experience_years,
            'bmi': bmi,
            'weekly_workouts': weekly_workouts,
            'avg_workout_duration': avg_workout_duration
        }
        
        # Generate workout plan recommendations based on features
        recommendations = []
        for i in range(n_samples):
            if goals[i] == 'weight_loss' and bmi[i] > 25:
                if fitness_levels[i] == 'beginner':
                    recommendations.append('cardio_beginner')
                elif fitness_levels[i] == 'intermediate':
                    recommendations.append('cardio_intermediate')
                else:
                    recommendations.append('cardio_advanced')
            elif goals[i] == 'muscle_gain':
                if experience_years[i] < 2:
                    recommendations.append('strength_beginner')
                elif experience_years[i] < 5:
                    recommendations.append('strength_intermediate')
                else:
                    recommendations.append('strength_advanced')
            elif goals[i] == 'endurance':
                if weekly_workouts[i] < 3:
                    recommendations.append('endurance_beginner')
                elif weekly_workouts[i] < 5:
                    recommendations.append('endurance_intermediate')
                else:
                    recommendations.append('endurance_advanced')
            else:  # strength
                if avg_workout_duration[i] < 45:
                    recommendations.append('power_beginner')
                elif avg_workout_duration[i] < 75:
                    recommendations.append('power_intermediate')
                else:
                    recommendations.append('power_advanced')
        
        data['recommended_plan'] = recommendations
        
        return pd.DataFrame(data)
    
    def preprocess_data(self, data):
        """
        Preprocess the data for training.
        """
        # Encode categorical variables
        categorical_columns = ['fitness_level', 'goal', 'recommended_plan']
        
        for col in categorical_columns:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
            data[col] = self.label_encoders[col].fit_transform(data[col])
        
        # Separate features and target
        feature_columns = ['age', 'fitness_level', 'goal', 'experience_years', 
                          'bmi', 'weekly_workouts', 'avg_workout_duration']
        
        X = data[feature_columns]
        y = data['recommended_plan']
        
        # Scale numerical features
        X_scaled = self.scaler.fit_transform(X)
        
        return X_scaled, y
    
    def train(self, data=None):
        """
        Train the workout recommendation model.
        """
        if data is None:
            data = self.prepare_sample_data()
        
        print("Preprocessing data...")
        X, y = self.preprocess_data(data)
        
        print("Splitting data...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        print("Training Random Forest model...")
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Model accuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        self.is_trained = True
        return accuracy
    
    def predict_workout_plan(self, user_data):
        """
        Predict workout plan recommendation for a user.
        
        Args:
            user_data (dict): Dictionary containing user characteristics
                - age: int
                - fitness_level: str ('beginner', 'intermediate', 'advanced')
                - goal: str ('weight_loss', 'muscle_gain', 'endurance', 'strength')
                - experience_years: int
                - bmi: float
                - weekly_workouts: int
                - avg_workout_duration: int
        
        Returns:
            dict: Prediction results with confidence scores
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Prepare user data
        user_df = pd.DataFrame([user_data])
        
        # Encode categorical variables
        for col in ['fitness_level', 'goal']:
            if col in self.label_encoders:
                user_df[col] = self.label_encoders[col].transform(user_df[col])
        
        # Scale features
        feature_columns = ['age', 'fitness_level', 'goal', 'experience_years', 
                          'bmi', 'weekly_workouts', 'avg_workout_duration']
        X_user = self.scaler.transform(user_df[feature_columns])
        
        # Make prediction
        prediction = self.model.predict(X_user)[0]
        probabilities = self.model.predict_proba(X_user)[0]
        
        # Decode prediction
        recommended_plan = self.label_encoders['recommended_plan'].inverse_transform([prediction])[0]
        
        # Get confidence scores for top 3 recommendations
        top_indices = np.argsort(probabilities)[-3:][::-1]
        top_plans = []
        for idx in top_indices:
            plan_name = self.label_encoders['recommended_plan'].inverse_transform([idx])[0]
            confidence = probabilities[idx]
            top_plans.append({
                'plan': plan_name,
                'confidence': float(confidence)
            })
        
        return {
            'recommended_plan': recommended_plan,
            'confidence': float(probabilities[prediction]),
            'top_recommendations': top_plans,
            'timestamp': datetime.now().isoformat()
        }
    
    def save_model(self, filepath):
        """
        Save the trained model and preprocessing objects.
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")
        
        model_data = {
            'model': self.model,
            'label_encoders': self.label_encoders,
            'scaler': self.scaler,
            'is_trained': self.is_trained
        }
        
        joblib.dump(model_data, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """
        Load a previously trained model.
        """
        model_data = joblib.load(filepath)
        
        self.model = model_data['model']
        self.label_encoders = model_data['label_encoders']
        self.scaler = model_data['scaler']
        self.is_trained = model_data['is_trained']
        
        print(f"Model loaded from {filepath}")
    
    def get_feature_importance(self):
        """
        Get feature importance scores from the trained model.
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before getting feature importance")
        
        feature_names = ['age', 'fitness_level', 'goal', 'experience_years', 
                        'bmi', 'weekly_workouts', 'avg_workout_duration']
        
        importance_scores = self.model.feature_importances_
        
        feature_importance = dict(zip(feature_names, importance_scores))
        return dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True))

def main():
    """
    Main function to demonstrate the workout recommendation model.
    """
    print("🏋️ Progress Fitness App - Workout Recommendation Model")
    print("=" * 60)
    
    # Initialize model
    model = WorkoutRecommendationModel()
    
    # Train model
    print("\n📚 Training the model...")
    accuracy = model.train()
    
    # Show feature importance
    print("\n📊 Feature Importance:")
    feature_importance = model.get_feature_importance()
    for feature, importance in feature_importance.items():
        print(f"  {feature}: {importance:.4f}")
    
    # Test predictions
    print("\n🎯 Testing predictions...")
    
    # Sample user 1: Beginner weight loss
    user1 = {
        'age': 28,
        'fitness_level': 'beginner',
        'goal': 'weight_loss',
        'experience_years': 0,
        'bmi': 28.5,
        'weekly_workouts': 2,
        'avg_workout_duration': 30
    }
    
    prediction1 = model.predict_workout_plan(user1)
    print(f"\nUser 1 (Beginner Weight Loss):")
    print(f"  Recommended: {prediction1['recommended_plan']}")
    print(f"  Confidence: {prediction1['confidence']:.2%}")
    
    # Sample user 2: Advanced muscle gain
    user2 = {
        'age': 35,
        'fitness_level': 'advanced',
        'goal': 'muscle_gain',
        'experience_years': 8,
        'bmi': 24.0,
        'weekly_workouts': 5,
        'avg_workout_duration': 90
    }
    
    prediction2 = model.predict_workout_plan(user2)
    print(f"\nUser 2 (Advanced Muscle Gain):")
    print(f"  Recommended: {prediction2['recommended_plan']}")
    print(f"  Confidence: {prediction2['confidence']:.2%}")
    
    # Save model
    print("\n💾 Saving model...")
    model.save_model('workout_recommendation_model.pkl')
    
    print("\n✅ Model training and testing completed!")

if __name__ == "__main__":
    main()

