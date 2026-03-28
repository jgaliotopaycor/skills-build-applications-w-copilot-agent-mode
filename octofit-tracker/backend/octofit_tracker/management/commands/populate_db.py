from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection
from djongo import models

from octofit_tracker import settings

from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']

        # Clear collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email
        db.users.create_index([('email', 1)], unique=True)

        # Sample users (superheroes)
        users = [
            {"name": "Clark Kent", "email": "superman@dc.com", "team": "dc"},
            {"name": "Bruce Wayne", "email": "batman@dc.com", "team": "dc"},
            {"name": "Diana Prince", "email": "wonderwoman@dc.com", "team": "dc"},
            {"name": "Tony Stark", "email": "ironman@marvel.com", "team": "marvel"},
            {"name": "Steve Rogers", "email": "captainamerica@marvel.com", "team": "marvel"},
            {"name": "Natasha Romanoff", "email": "blackwidow@marvel.com", "team": "marvel"},
        ]
        db.users.insert_many(users)

        # Teams
        teams = [
            {"name": "marvel", "members": [u["email"] for u in users if u["team"] == "marvel"]},
            {"name": "dc", "members": [u["email"] for u in users if u["team"] == "dc"]},
        ]
        db.teams.insert_many(teams)

        # Activities
        activities = [
            {"user_email": "superman@dc.com", "activity": "Flight", "duration": 60},
            {"user_email": "batman@dc.com", "activity": "Martial Arts", "duration": 45},
            {"user_email": "wonderwoman@dc.com", "activity": "Lasso Training", "duration": 30},
            {"user_email": "ironman@marvel.com", "activity": "Suit Test", "duration": 50},
            {"user_email": "captainamerica@marvel.com", "activity": "Shield Throw", "duration": 40},
            {"user_email": "blackwidow@marvel.com", "activity": "Espionage", "duration": 35},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {"team": "marvel", "points": 125},
            {"team": "dc", "points": 135},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {"name": "Super Strength", "suggested_for": ["superman@dc.com", "wonderwoman@dc.com"]},
            {"name": "Tech Training", "suggested_for": ["ironman@marvel.com", "batman@dc.com"]},
            {"name": "Agility Drills", "suggested_for": ["blackwidow@marvel.com", "captainamerica@marvel.com"]},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
