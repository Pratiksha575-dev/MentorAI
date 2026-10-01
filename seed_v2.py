import json
import random
from database import save_mentor, save_student_group, save_student, init_db

# 5 Mentors
MENTORS = [
    {"name": "Dr. Alan Turing", "domains": ["Machine Learning", "Fintech"], "traits": [2.5, 3.0, 4.0, 4.8, 4.9]},
    {"name": "Prof. Ada Lovelace", "domains": ["Web Development", "Education"], "traits": [4.0, 2.0, 4.5, 4.5, 5.0]},
    {"name": "Dr. Grace Hopper", "domains": ["App Development", "Cybersecurity"], "traits": [4.5, 1.5, 3.5, 5.0, 3.5]},
    {"name": "Dr. John von Neumann", "domains": ["Data Science", "Gaming"], "traits": [4.2, 2.5, 3.0, 4.7, 4.8]},
    {"name": "Prof. Margaret Hamilton", "domains": ["Cloud Computing", "Healthcare"], "traits": [3.5, 2.0, 4.8, 4.9, 4.2]}
]

# 15 Group Topics
TOPICS = [
    "AI-powered Medical Chatbot (Healthcare, NLP)",
    "Blockchain for Education Credentials (Education)",
    "Cloud Infrastructure for E-commerce",
    "Predictive Policing (Data Science)",
    "Gamified Learning Platform (Gaming, Education)",
    "Mobile Banking App (Fintech, App Dev)",
    "Cybersecurity Threat Detector (Cybersecurity, ML)",
    "AR Navigation System (App Dev, Computer Vision)",
    "Automated Stock Trader (Fintech, ML)",
    "Telehealth Portal (Web Dev, Healthcare)",
    "Smart Grid IoT (Cloud Computing)",
    "Data Viz Dashboard (Web Dev, Data Science)",
    "VR Fitness Game (Gaming, Healthcare)",
    "Fake News Detector (NLP, Web Dev)",
    "Serverless Voting System (Cloud, Cybersecurity)"
]

def generate_random_traits():
    return {
        "Extraversion": round(random.uniform(1.0, 5.0), 1),
        "Neuroticism": round(random.uniform(1.0, 5.0), 1),
        "Agreeableness": round(random.uniform(1.0, 5.0), 1),
        "Conscientiousness": round(random.uniform(1.0, 5.0), 1),
        "Openness": round(random.uniform(1.0, 5.0), 1)
    }

def run_seed():
    init_db()
    
    print("Seeding 5 Mentors...")
    for m in MENTORS:
        traits = {"Extraversion": m["traits"][0], "Neuroticism": m["traits"][1], "Agreeableness": m["traits"][2], "Conscientiousness": m["traits"][3], "Openness": m["traits"][4]}
        save_mentor(m["name"], m["domains"], traits, f"Generated AI Summary for {m['name']}.")
        
    print("Seeding 15 Groups...")
    for i in range(15):
        g_name = f"Group {chr(65+i)}"
        g_topic = TOPICS[i]
        
        # Create 3-4 students per group
        num_students = random.randint(3, 4)
        students = []
        for j in range(num_students):
            s_name = f"Student_{i}_{j}"
            s_traits = generate_random_traits()
            students.append({"name": s_name, "traits": s_traits})
            
        # Aggregate
        avg_traits = {}
        for trait in ["Extraversion", "Neuroticism", "Agreeableness", "Conscientiousness", "Openness"]:
            avg_traits[trait] = round(sum(s["traits"][trait] for s in students) / len(students), 1)
            
        g_id = save_student_group(g_name, g_topic, avg_traits, f"Generated Group Dynamic for {g_name}.")
        for s in students:
            save_student(g_id, s["name"], s["traits"], "Assigned Role")
            
    print("v2 Database seeded with 5 Mentors and 15 Groups!")

if __name__ == "__main__":
    run_seed()
