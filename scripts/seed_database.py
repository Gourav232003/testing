#!/usr/bin/env python3
"""
Database seeding script for EcoFarm Quest
This script populates the database with initial data for courses, achievements, and sample users.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add the parent directory to the path so we can import our models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.course import Course, Lesson, Quiz
from models.community import Achievement
from models.user import User

# Load environment variables
load_dotenv()

def seed_courses():
    """Seed the database with sample courses"""
    print("🌱 Seeding courses...")
    
    courses_data = [
        {
            'title': 'Smart Irrigation Mastery',
            'description': 'Learn advanced irrigation techniques for optimal water usage and sustainable farming practices.',
            'category': 'water',
            'duration': '3 hours',
            'difficulty': 3,
            'thumbnail': '🌊',
            'color': '#2196F3',
            'certificate': 'Water Management Expert',
            'learning_objectives': [
                'Understand different irrigation systems',
                'Learn water conservation techniques',
                'Master smart irrigation scheduling',
                'Implement sustainable water management'
            ],
            'prerequisites': ['Basic farming knowledge']
        },
        {
            'title': 'Soil Health Fundamentals',
            'description': 'Master soil testing, composting, and nutrient management for healthy crops.',
            'category': 'soil',
            'duration': '4 hours',
            'difficulty': 2,
            'thumbnail': '🌱',
            'color': '#4CAF50',
            'certificate': 'Soil Guardian',
            'learning_objectives': [
                'Learn soil composition and structure',
                'Master soil testing techniques',
                'Understand composting methods',
                'Implement nutrient management'
            ],
            'prerequisites': []
        },
        {
            'title': 'Integrated Pest Management',
            'description': 'Natural and biological pest control methods for sustainable agriculture.',
            'category': 'pest',
            'duration': '2.5 hours',
            'difficulty': 3,
            'thumbnail': '🐛',
            'color': '#FF5722',
            'certificate': 'Pest Control Specialist',
            'learning_objectives': [
                'Identify common pests and diseases',
                'Learn biological control methods',
                'Master integrated pest management',
                'Implement sustainable pest control'
            ],
            'prerequisites': ['Basic plant knowledge']
        },
        {
            'title': 'Organic Farming Practices',
            'description': 'Complete guide to organic and sustainable farming methods.',
            'category': 'sustainable',
            'duration': '5 hours',
            'difficulty': 4,
            'thumbnail': '🌿',
            'color': '#8BC34A',
            'certificate': 'Organic Farming Master',
            'learning_objectives': [
                'Understand organic farming principles',
                'Learn organic certification process',
                'Master organic pest control',
                'Implement sustainable farming practices'
            ],
            'prerequisites': ['Soil Health Fundamentals', 'Integrated Pest Management']
        },
        {
            'title': 'Crop Rotation Strategies',
            'description': 'Maximize yield through strategic crop rotation and soil management.',
            'category': 'soil',
            'duration': '2 hours',
            'difficulty': 2,
            'thumbnail': '🔄',
            'color': '#9C27B0',
            'certificate': 'Rotation Expert',
            'learning_objectives': [
                'Learn crop rotation principles',
                'Plan effective rotation cycles',
                'Understand soil nutrient cycling',
                'Implement sustainable rotation'
            ],
            'prerequisites': ['Soil Health Fundamentals']
        }
    ]
    
    for course_data in courses_data:
        course = Course(**course_data)
        course.save()
        print(f"  ✅ Created course: {course.title}")
        
        # Create sample lessons for each course
        create_sample_lessons(course.id, course.title)
        
        # Create sample quiz for each course
        create_sample_quiz(course.id, course.title)

def create_sample_lessons(course_id, course_title):
    """Create sample lessons for a course"""
    lesson_templates = [
        {
            'title': f'Introduction to {course_title}',
            'content': f'Welcome to {course_title}! In this comprehensive course, you will learn the fundamentals and advanced techniques.',
            'lesson_type': 'text',
            'duration': 15,
            'order': 1
        },
        {
            'title': f'{course_title} - Basic Concepts',
            'content': 'Learn the basic concepts and principles that form the foundation of this subject.',
            'lesson_type': 'text',
            'duration': 20,
            'order': 2
        },
        {
            'title': f'{course_title} - Practical Applications',
            'content': 'Discover how to apply these concepts in real-world farming scenarios.',
            'lesson_type': 'interactive',
            'duration': 25,
            'order': 3
        },
        {
            'title': f'{course_title} - Best Practices',
            'content': 'Master the best practices and expert tips for optimal results.',
            'lesson_type': 'text',
            'duration': 20,
            'order': 4
        },
        {
            'title': f'{course_title} - Case Studies',
            'content': 'Explore real-world case studies and success stories from farmers.',
            'lesson_type': 'text',
            'duration': 15,
            'order': 5
        }
    ]
    
    for lesson_data in lesson_templates:
        lesson = Lesson(
            course_id=course_id,
            **lesson_data
        )
        lesson.save()

def create_sample_quiz(course_id, course_title):
    """Create sample quiz for a course"""
    quiz = Quiz(
        course_id=course_id,
        title=f'{course_title} - Final Assessment',
        description=f'Test your knowledge of {course_title} with this comprehensive quiz.',
        questions=[
            {
                'question': f'What is the primary benefit of {course_title.lower()}?',
                'question_type': 'multiple_choice',
                'options': [
                    'Increased crop yield',
                    'Reduced water usage',
                    'Better soil health',
                    'All of the above'
                ],
                'correct_answer': 3,
                'explanation': 'All of the above benefits are achieved through proper implementation.',
                'points': 1,
                'order': 1
            },
            {
                'question': f'Which factor is most important in {course_title.lower()}?',
                'question_type': 'multiple_choice',
                'options': [
                    'Timing',
                    'Equipment',
                    'Weather',
                    'Soil conditions'
                ],
                'correct_answer': 0,
                'explanation': 'Timing is crucial for optimal results in farming practices.',
                'points': 1,
                'order': 2
            }
        ],
        passing_score=70,
        time_limit=30,
        max_attempts=3
    )
    quiz.save()

def seed_achievements():
    """Seed the database with achievements"""
    print("🏆 Seeding achievements...")
    
    achievements_data = [
        # Learning Achievements
        {
            'name': 'Knowledge Seeker',
            'description': 'Complete your first course',
            'icon': '📚',
            'category': 'Learning Achievements',
            'requirement': {'type': 'courses_completed', 'value': 1},
            'points': 10
        },
        {
            'name': 'Course Master',
            'description': 'Complete 3 courses',
            'icon': '🎓',
            'category': 'Learning Achievements',
            'requirement': {'type': 'courses_completed', 'value': 3},
            'points': 25
        },
        {
            'name': 'Learning Champion',
            'description': 'Complete 10 courses',
            'icon': '👑',
            'category': 'Learning Achievements',
            'requirement': {'type': 'courses_completed', 'value': 10},
            'points': 100
        },
        {
            'name': 'Quiz Master',
            'description': 'Score 100% on 5 quizzes',
            'icon': '🎯',
            'category': 'Learning Achievements',
            'requirement': {'type': 'perfect_quizzes', 'value': 5},
            'points': 50
        },
        
        # Community Achievements
        {
            'name': 'Helpful Farmer',
            'description': 'Help 10 fellow farmers',
            'icon': '🤝',
            'category': 'Community Achievements',
            'requirement': {'type': 'helpful_actions', 'value': 10},
            'points': 30
        },
        {
            'name': 'Discussion Leader',
            'description': 'Start 5 meaningful discussions',
            'icon': '💬',
            'category': 'Community Achievements',
            'requirement': {'type': 'discussions_started', 'value': 5},
            'points': 20
        },
        {
            'name': 'Community Champion',
            'description': 'Get 100 likes on your posts',
            'icon': '❤️',
            'category': 'Community Achievements',
            'requirement': {'type': 'total_likes', 'value': 100},
            'points': 40
        },
        
        # Progress Achievements
        {
            'name': 'Consistent Learner',
            'description': 'Maintain 7-day learning streak',
            'icon': '🔥',
            'category': 'Progress Achievements',
            'requirement': {'type': 'learning_streak', 'value': 7},
            'points': 25
        },
        {
            'name': 'Knowledge Collector',
            'description': 'Earn 1000 knowledge points',
            'icon': '⭐',
            'category': 'Progress Achievements',
            'requirement': {'type': 'knowledge_points', 'value': 1000},
            'points': 50
        },
        {
            'name': 'Level Master',
            'description': 'Reach level 10',
            'icon': '🌟',
            'category': 'Progress Achievements',
            'requirement': {'type': 'level', 'value': 10},
            'points': 75
        },
        
        # Special Achievements
        {
            'name': 'Early Bird',
            'description': 'Complete a course within 24 hours of enrollment',
            'icon': '🐦',
            'category': 'Special Achievements',
            'requirement': {'type': 'fast_completion', 'value': 1},
            'points': 15
        },
        {
            'name': 'Night Owl',
            'description': 'Study between 10 PM and 6 AM',
            'icon': '🦉',
            'category': 'Special Achievements',
            'requirement': {'type': 'night_study', 'value': 5},
            'points': 20
        },
        {
            'name': 'Weekend Warrior',
            'description': 'Complete 5 lessons on weekends',
            'icon': '⚔️',
            'category': 'Special Achievements',
            'requirement': {'type': 'weekend_lessons', 'value': 5},
            'points': 30
        }
    ]
    
    for achievement_data in achievements_data:
        achievement = Achievement(**achievement_data)
        achievement.save()
        print(f"  ✅ Created achievement: {achievement.name}")

def seed_sample_users():
    """Seed the database with sample users"""
    print("👥 Seeding sample users...")
    
    sample_users = [
        {
            'name': 'Rajesh Kumar',
            'email': 'rajesh@example.com',
            'password': 'password123',
            'phone': '+91 98765 43210',
            'location': 'Green Valley Village',
            'farm_size': '8 acres',
            'primary_crops': ['Rice', 'Wheat', 'Vegetables'],
            'farming_experience': '20 years',
            'water_source': 'canal',
            'avatar': {'emoji': '🐄', 'name': 'Gau Mata', 'type': 'Dairy Specialist'}
        },
        {
            'name': 'Priya Devi',
            'email': 'priya@example.com',
            'password': 'password123',
            'phone': '+91 98765 43211',
            'location': 'Sunrise Farm',
            'farm_size': '5 acres',
            'primary_crops': ['Tomatoes', 'Chilies', 'Onions'],
            'farming_experience': '15 years',
            'water_source': 'borewell',
            'avatar': {'emoji': '🐔', 'name': 'Murgi', 'type': 'Poultry Expert'}
        },
        {
            'name': 'Anil Singh',
            'email': 'anil@example.com',
            'password': 'password123',
            'phone': '+91 98765 43212',
            'location': 'Eco Fields',
            'farm_size': '12 acres',
            'primary_crops': ['Sugarcane', 'Cotton', 'Pulses'],
            'farming_experience': '25 years',
            'water_source': 'river',
            'avatar': {'emoji': '🐐', 'name': 'Bakri', 'type': 'Livestock Guardian'}
        }
    ]
    
    for user_data in sample_users:
        # Check if user already exists
        if not User.find_by_email(user_data['email']):
            user = User(
                name=user_data['name'],
                email=user_data['email'],
                password=User.hash_password(user_data['password']),
                phone=user_data['phone'],
                location=user_data['location'],
                farm_size=user_data['farm_size'],
                primary_crops=user_data['primary_crops'],
                farming_experience=user_data['farming_experience'],
                water_source=user_data['water_source'],
                avatar=user_data['avatar'],
                is_verified=True
            )
            user.save()
            print(f"  ✅ Created user: {user.name}")
        else:
            print(f"  ⚠️  User already exists: {user_data['name']}")

def main():
    """Main seeding function"""
    print("🌱 Starting EcoFarm Quest database seeding...")
    print("=" * 50)
    
    try:
        # Seed courses and lessons
        seed_courses()
        print()
        
        # Seed achievements
        seed_achievements()
        print()
        
        # Seed sample users
        seed_sample_users()
        print()
        
        print("=" * 50)
        print("✅ Database seeding completed successfully!")
        print("🌱 EcoFarm Quest is ready to use!")
        
    except Exception as e:
        print(f"❌ Error during seeding: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()


