import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

def generate_workout_data(n_users=50, days_back=90):
    """
    Generate sample workout data for multiple users.
    
    Args:
        n_users (int): Number of users to generate data for
        days_back (int): Number of days back to generate data for
    
    Returns:
        pd.DataFrame: Workout data with columns: user_id, date, workout_type, duration, calories, exercises
    """
    np.random.seed(42)
    
    # Generate user IDs
    user_ids = list(range(1, n_users + 1))
    
    # Workout types and their characteristics
    workout_types = {
        'Strength Training': {'duration_range': (45, 90), 'calories_range': (300, 600)},
        'Cardio': {'duration_range': (20, 60), 'calories_range': (200, 500)},
        'HIIT': {'duration_range': (20, 45), 'calories_range': (250, 450)},
        'Yoga': {'duration_range': (30, 90), 'calories_range': (100, 300)},
        'Running': {'duration_range': (20, 120), 'calories_range': (150, 800)},
        'Cycling': {'duration_range': (30, 90), 'calories_range': (200, 600)}
    }
    
    # Exercise libraries for each workout type
    exercise_libraries = {
        'Strength Training': ['Bench Press', 'Squats', 'Deadlifts', 'Pull-ups', 'Dumbbell Rows'],
        'Cardio': ['Treadmill', 'Elliptical', 'Stationary Bike', 'Rowing Machine'],
        'HIIT': ['Burpees', 'Mountain Climbers', 'Jump Squats', 'Push-ups', 'Planks'],
        'Yoga': ['Sun Salutation', 'Warrior Pose', 'Tree Pose', 'Downward Dog', 'Child Pose'],
        'Running': ['Easy Run', 'Tempo Run', 'Interval Training', 'Long Run'],
        'Cycling': ['Indoor Cycling', 'Outdoor Cycling', 'Hill Training', 'Endurance Ride']
    }
    
    data = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    for user_id in user_ids:
        # Generate workout frequency (2-6 workouts per week)
        workouts_per_week = np.random.randint(2, 7)
        total_workouts = int((days_back / 7) * workouts_per_week)
        
        # Generate workout dates
        workout_dates = np.random.choice(
            pd.date_range(start_date, end_date, freq='D'),
            size=total_workouts,
            replace=False
        )
        
        for date in workout_dates:
            # Select workout type
            workout_type = np.random.choice(list(workout_types.keys()))
            workout_info = workout_types[workout_type]
            
            # Generate duration and calories
            duration = np.random.randint(*workout_info['duration_range'])
            calories = np.random.randint(*workout_info['calories_range'])
            
            # Select exercises
            available_exercises = exercise_libraries[workout_type]
            n_exercises = np.random.randint(3, min(8, len(available_exercises) + 1))
            exercises = np.random.choice(available_exercises, size=n_exercises, replace=False)
            
            data.append({
                'user_id': user_id,
                'date': date.strftime('%Y-%m-%d'),
                'workout_type': workout_type,
                'duration_minutes': duration,
                'calories_burned': calories,
                'exercises': list(exercises),
                'timestamp': date.isoformat()
            })
    
    return pd.DataFrame(data)

def generate_user_profiles(n_users=50):
    """
    Generate sample user profiles with fitness characteristics.
    
    Args:
        n_users (int): Number of users to generate profiles for
    
    Returns:
        pd.DataFrame: User profiles with fitness characteristics
    """
    np.random.seed(42)
    
    # Age distribution (18-65)
    ages = np.random.normal(35, 12, n_users)
    ages = np.clip(ages, 18, 65).astype(int)
    
    # Gender distribution
    genders = np.random.choice(['Male', 'Female'], n_users, p=[0.6, 0.4])
    
    # Fitness levels
    fitness_levels = np.random.choice(['beginner', 'intermediate', 'advanced'], n_users, p=[0.4, 0.4, 0.2])
    
    # Goals
    goals = np.random.choice(['weight_loss', 'muscle_gain', 'endurance', 'strength', 'general_fitness'], n_users)
    
    # Experience years
    experience_years = np.random.exponential(3, n_users)
    experience_years = np.clip(experience_years, 0, 20).astype(int)
    
    # BMI distribution
    bmi = np.random.normal(24, 4, n_users)
    bmi = np.clip(bmi, 18, 35)
    
    # Weekly workout frequency
    weekly_workouts = np.random.poisson(3.5, n_users)
    weekly_workouts = np.clip(weekly_workouts, 1, 7)
    
    # Average workout duration
    avg_workout_duration = np.random.normal(45, 20, n_users)
    avg_workout_duration = np.clip(avg_workout_duration, 20, 120).astype(int)
    
    data = []
    for i in range(n_users):
        data.append({
            'user_id': i + 1,
            'age': ages[i],
            'gender': genders[i],
            'fitness_level': fitness_levels[i],
            'goal': goals[i],
            'experience_years': experience_years[i],
            'bmi': round(bmi[i], 1),
            'weekly_workouts': weekly_workouts[i],
            'avg_workout_duration': avg_workout_duration[i],
            'created_at': datetime.now().isoformat()
        })
    
    return pd.DataFrame(data)

def generate_equipment_usage_data(n_equipment=20, days_back=30):
    """
    Generate sample equipment usage data.
    
    Args:
        n_equipment (int): Number of equipment items
        days_back (int): Number of days back to generate data for
    
    Returns:
        pd.DataFrame: Equipment usage data
    """
    np.random.seed(42)
    
    # Equipment types
    equipment_types = [
        'Treadmill', 'Elliptical', 'Stationary Bike', 'Rowing Machine',
        'Bench Press', 'Squat Rack', 'Cable Machine', 'Dumbbells',
        'Pull-up Bar', 'Dip Bars', 'Leg Press', 'Lat Pulldown'
    ]
    
    # Generate equipment data
    equipment_data = []
    for i in range(n_equipment):
        equipment_type = np.random.choice(equipment_types)
        location = np.random.choice(['Cardio Area', 'Weight Room', 'Functional Area'])
        
        equipment_data.append({
            'equipment_id': i + 1,
            'equipment_name': f"{equipment_type} #{i+1}",
            'equipment_type': equipment_type,
            'location': location,
            'condition': np.random.choice(['available', 'maintenance', 'out_of_order'], p=[0.8, 0.15, 0.05])
        })
    
    # Generate usage data
    usage_data = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    for equipment in equipment_data:
        # Generate usage frequency based on equipment type
        if 'Cardio' in equipment['equipment_type']:
            daily_usage = np.random.poisson(15)  # High usage for cardio
        elif 'Weight' in equipment['equipment_type']:
            daily_usage = np.random.poisson(8)   # Medium usage for weights
        else:
            daily_usage = np.random.poisson(5)   # Lower usage for others
        
        # Generate usage records
        for day in pd.date_range(start_date, end_date, freq='D'):
            if np.random.random() < 0.7:  # 70% chance of being used each day
                n_sessions = np.random.poisson(daily_usage)
                for _ in range(n_sessions):
                    usage_data.append({
                        'equipment_id': equipment['equipment_id'],
                        'date': day.strftime('%Y-%m-%d'),
                        'usage_duration_minutes': np.random.randint(10, 60),
                        'user_id': np.random.randint(1, 51),
                        'timestamp': day.isoformat()
                    })
    
    return pd.DataFrame(equipment_data), pd.DataFrame(usage_data)

def generate_progress_data(n_users=50, weeks=12):
    """
    Generate sample progress tracking data.
    
    Args:
        n_users (int): Number of users
        weeks (int): Number of weeks to track
    
    Returns:
        pd.DataFrame: Progress data with weekly measurements
    """
    np.random.seed(42)
    
    data = []
    end_date = datetime.now()
    
    for user_id in range(1, n_users + 1):
        # Generate starting measurements
        starting_weight = np.random.normal(70, 15)  # kg
        starting_body_fat = np.random.normal(20, 8)  # %
        starting_muscle_mass = np.random.normal(45, 10)  # kg
        
        for week in range(weeks):
            week_date = end_date - timedelta(weeks=weeks-week-1)
            
            # Simulate progress based on consistency
            consistency = np.random.random()  # 0-1 scale
            
            # Weight changes (slight variations)
            weight_change = np.random.normal(0, 0.5) * consistency
            current_weight = starting_weight + weight_change
            
            # Body fat changes
            fat_change = np.random.normal(-0.2, 0.3) * consistency
            current_body_fat = max(8, starting_body_fat + fat_change)
            
            # Muscle mass changes
            muscle_change = np.random.normal(0.1, 0.2) * consistency
            current_muscle_mass = starting_muscle_mass + muscle_change
            
            data.append({
                'user_id': user_id,
                'week': week + 1,
                'date': week_date.strftime('%Y-%m-%d'),
                'weight_kg': round(current_weight, 1),
                'body_fat_percent': round(current_body_fat, 1),
                'muscle_mass_kg': round(current_muscle_mass, 1),
                'consistency_score': round(consistency, 2),
                'notes': f"Week {week + 1} progress tracking"
            })
    
    return pd.DataFrame(data)

def save_datasets():
    """
    Generate and save all sample datasets.
    """
    print("🏋️ Generating sample fitness datasets...")
    
    # Generate datasets
    print("📊 Generating workout data...")
    workout_df = generate_workout_data(n_users=50, days_back=90)
    
    print("👥 Generating user profiles...")
    users_df = generate_user_profiles(n_users=50)
    
    print("🏋️ Generating equipment data...")
    equipment_df, usage_df = generate_equipment_usage_data(n_equipment=20, days_back=30)
    
    print("📈 Generating progress data...")
    progress_df = generate_progress_data(n_users=50, weeks=12)
    
    # Save datasets
    print("💾 Saving datasets...")
    
    # Save as CSV
    workout_df.to_csv('datasets/workout_data.csv', index=False)
    users_df.to_csv('datasets/user_profiles.csv', index=False)
    equipment_df.to_csv('datasets/equipment_data.csv', index=False)
    usage_df.to_csv('datasets/equipment_usage.csv', index=False)
    progress_df.to_csv('datasets/progress_data.csv', index=False)
    
    # Save as JSON for API consumption
    workout_df.to_json('datasets/workout_data.json', orient='records', indent=2)
    users_df.to_json('datasets/user_profiles.json', orient='records', indent=2)
    equipment_df.to_json('datasets/equipment_data.json', orient='records', indent=2)
    usage_df.to_json('datasets/equipment_usage.json', orient='records', indent=2)
    progress_df.to_json('datasets/progress_data.json', orient='records', indent=2)
    
    # Create dataset summary
    summary = {
        'datasets_generated': {
            'workout_data': {
                'rows': len(workout_df),
                'columns': list(workout_df.columns),
                'file': 'workout_data.csv'
            },
            'user_profiles': {
                'rows': len(users_df),
                'columns': list(users_df.columns),
                'file': 'user_profiles.csv'
            },
            'equipment_data': {
                'rows': len(equipment_df),
                'columns': list(equipment_df.columns),
                'file': 'equipment_data.csv'
            },
            'equipment_usage': {
                'rows': len(usage_df),
                'columns': list(usage_df.columns),
                'file': 'equipment_usage.csv'
            },
            'progress_data': {
                'rows': len(progress_df),
                'columns': list(progress_df.columns),
                'file': 'progress_data.csv'
            }
        },
        'generated_at': datetime.now().isoformat(),
        'total_records': len(workout_df) + len(users_df) + len(equipment_df) + len(usage_df) + len(progress_df)
    }
    
    with open('datasets/dataset_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("✅ All datasets generated and saved successfully!")
    print(f"📊 Total records generated: {summary['total_records']}")
    
    return summary

if __name__ == "__main__":
    summary = save_datasets()
    print("\n📋 Dataset Summary:")
    print(json.dumps(summary, indent=2))

