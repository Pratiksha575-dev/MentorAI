import json
from database import save_profile, init_db

# Mock Data
mentors = [
    {
        "name": "Dr. Alan Turing",
        "role": "mentor",
        "interests": ["Machine Learning", "Mathematics", "History"],
        "traits": {"Extraversion": 2.5, "Neuroticism": 3.0, "Agreeableness": 4.0, "Conscientiousness": 4.8, "Openness": 4.9},
        "cluster": 0
    },
    {
        "name": "Prof. Ada Lovelace",
        "role": "mentor",
        "interests": ["Software Engineering", "Art", "Poetry"],
        "traits": {"Extraversion": 4.0, "Neuroticism": 2.0, "Agreeableness": 4.5, "Conscientiousness": 4.5, "Openness": 5.0},
        "cluster": 1
    }
]

mentees = [
    {
        "name": "Group Alpha (The Hackers)",
        "role": "mentee",
        "interests": ["Machine Learning", "Hackathons"],
        "traits": {"Extraversion": 4.5, "Neuroticism": 4.0, "Agreeableness": 3.5, "Conscientiousness": 2.0, "Openness": 4.5},
        "cluster": 2
    },
    {
        "name": "Group Beta (The Planners)",
        "role": "mentee",
        "interests": ["Software Engineering", "Project Management"],
        "traits": {"Extraversion": 3.0, "Neuroticism": 2.0, "Agreeableness": 4.0, "Conscientiousness": 4.8, "Openness": 3.0},
        "cluster": 3
    },
    {
        "name": "Group Gamma (The Creatives)",
        "role": "mentee",
        "interests": ["Art", "Design", "Mathematics"],
        "traits": {"Extraversion": 3.5, "Neuroticism": 3.5, "Agreeableness": 4.5, "Conscientiousness": 2.5, "Openness": 4.8},
        "cluster": 0
    }
]

def run_seed():
    init_db()
    for m in mentors:
        save_profile(**m)
        print(f"Saved mentor {m['name']}")
    for m in mentees:
        save_profile(**m)
        print(f"Saved mentee {m['name']}")
    print("Database seeded!")

if __name__ == "__main__":
    run_seed()
