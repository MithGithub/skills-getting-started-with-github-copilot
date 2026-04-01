"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball": {
        "description": "Team-based basketball games and skill development",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["alex@mergington.edu", "james@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Tennis training and competitive matches",
        "schedule": "Wednesdays and Saturdays, 10:00 AM - 11:30 AM",
        "max_participants": 14,
        "participants": ["nina@mergington.edu"]
    },
    "Drama Club": {
        "description": "Stage performance, acting, and theater production",
        "schedule": "Tuesdays and Thursdays, 4:30 PM - 6:00 PM",
        "max_participants": 25,
        "participants": ["grace@mergington.edu", "jackson@mergington.edu"]
    },
    "Art Studio": {
        "description": "Painting, drawing, and creative visual arts",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["maya@mergington.edu"]
    },
    "Science Club": {
        "description": "Hands-on science experiments and STEM learning",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 22,
        "participants": ["ryan@mergington.edu", "sarah@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop argumentation and public speaking skills",
        "schedule": "Tuesdays and Thursdays, 5:00 PM - 6:30 PM",
        "max_participants": 15,
        "participants": ["lucas@mergington.edu"]
    },
    "Volleyball Club": {
        "description": "Indoor volleyball practice and friendly matches",
        "schedule": "Wednesdays and Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["harper@mergington.edu", "eli@mergington.edu"]
    },
    "Swimming Team": {
        "description": "Lap training and swim meets for competitive swimmers",
        "schedule": "Mondays and Thursdays, 5:00 PM - 6:30 PM",
        "max_participants": 20,
        "participants": ["mason@mergington.edu", "ava@mergington.edu"]
    },
    "Creative Writing Club": {
        "description": "Write stories, poems, and essays with peer feedback",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["ella@mergington.edu", "noah@mergington.edu"]
    },
    "Photography Club": {
        "description": "Explore photography techniques and create visual stories",
        "schedule": "Saturdays, 10:00 AM - 12:00 PM",
        "max_participants": 14,
        "participants": ["clara@mergington.edu"]
    },
    "Robotics Team": {
        "description": "Build robots and solve engineering challenges",
        "schedule": "Wednesdays and Saturdays, 4:30 PM - 6:30 PM",
        "max_participants": 15,
        "participants": ["ben@mergington.edu", "mia@mergington.edu"]
    },
    "History Scholars": {
        "description": "Study history through debates, research, and presentations",
        "schedule": "Mondays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["olivia@mergington.edu", "ethan@mergington.edu"]
    },
    "Track and Field": {
        "description": "Run, jump, and throw in track and field training sessions",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["jack@mergington.edu", "ava@mergington.edu"]
    },
    "Yoga Club": {
        "description": "Flexibility and mindfulness through yoga practice",
        "schedule": "Wednesdays, 5:00 PM - 6:00 PM",
        "max_participants": 18,
        "participants": ["emma@mergington.edu"]
    },
    "Music Ensemble": {
        "description": "Practice instruments together and prepare concerts",
        "schedule": "Mondays and Wednesdays, 5:00 PM - 6:30 PM",
        "max_participants": 20,
        "participants": ["liam@mergington.edu", "isabella@mergington.edu"]
    },
    "Ceramics Workshop": {
        "description": "Hand-building pottery and glazing ceramics",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["olivia@mergington.edu"]
    },
    "Astronomy Society": {
        "description": "Observe the night sky and learn about stars and planets",
        "schedule": "Thursdays, 7:00 PM - 8:30 PM",
        "max_participants": 16,
        "participants": ["noah@mergington.edu"]
    },
    "Environmental Research": {
        "description": "Investigate local ecosystems and conservation science",
        "schedule": "Wednesdays, 4:30 PM - 6:00 PM",
        "max_participants": 18,
        "participants": ["sophia@mergington.edu", "mason@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up")
    
    # Validate activity is not full
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")
    
    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found")

    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
