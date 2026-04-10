from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB directly for index creation
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create unique index on email for users
        db.users.create_index([('email', 1)], unique=True)

        # Sample data
        users = [
            {"name": "Clark Kent", "email": "superman@dc.com", "team": "DC"},
            {"name": "Bruce Wayne", "email": "batman@dc.com", "team": "DC"},
            {"name": "Diana Prince", "email": "wonderwoman@dc.com", "team": "DC"},
            {"name": "Tony Stark", "email": "ironman@marvel.com", "team": "Marvel"},
            {"name": "Steve Rogers", "email": "captain@marvel.com", "team": "Marvel"},
            {"name": "Peter Parker", "email": "spiderman@marvel.com", "team": "Marvel"},
        ]
        teams = [
            {"name": "Marvel", "members": ["Tony Stark", "Steve Rogers", "Peter Parker"]},
            {"name": "DC", "members": ["Clark Kent", "Bruce Wayne", "Diana Prince"]},
        ]
        activities = [
            {"user": "Clark Kent", "activity": "Flight", "duration": 60},
            {"user": "Tony Stark", "activity": "Suit Training", "duration": 45},
            {"user": "Diana Prince", "activity": "Lasso Practice", "duration": 30},
        ]
        leaderboard = [
            {"user": "Clark Kent", "points": 100},
            {"user": "Tony Stark", "points": 90},
            {"user": "Diana Prince", "points": 80},
        ]
        workouts = [
            {"name": "Super Strength", "suggested_for": "DC"},
            {"name": "Web Swing", "suggested_for": "Marvel"},
        ]

        db.users.insert_many(users)
        db.teams.insert_many(teams)
        db.activities.insert_many(activities)
        db.leaderboard.insert_many(leaderboard)
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
