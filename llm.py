import requests
import json
import streamlit as st

URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:latest"

def ask_ollama(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(URL, json=payload)
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama: {e}")
        return "AI analysis is currently unavailable. Please ensure Ollama is running locally."

def generate_mentor_summary(name, domains, traits):
    prompt = f'''
You are an expert psychological profiler analyzing a university faculty mentor for a project allocation system.
Name: {name}
Interested Domains: {', '.join(domains)}
Advising Traits (out of 5):
Extraversion: {traits.get('Extraversion', 0):.2f}/5
Neuroticism: {traits.get('Neuroticism', 0):.2f}/5
Agreeableness: {traits.get('Agreeableness', 0):.2f}/5
Conscientiousness: {traits.get('Conscientiousness', 0):.2f}/5
Openness: {traits.get('Openness', 0):.2f}/5

Write a highly detailed, comprehensive profile (at least 3-4 paragraphs) of their expected mentorship style. 
Include:
1. Their core communication and management style.
2. How they handle missed deadlines and student failures.
3. The type of student groups they will synergize with perfectly.
4. The type of student groups they will likely clash with.
Return plain text formatted nicely with markdown.
'''
    return ask_ollama(prompt)

def generate_group_dynamic(group_name, topic, students):
    students_info = ""
    for s in students:
        t = s['traits'] if 'traits' in s else s
        students_info += f"- {s['name']}: Extraversion {t.get('Extraversion',0):.1f}, Neuroticism {t.get('Neuroticism',0):.1f}, Agreeableness {t.get('Agreeableness',0):.1f}, Conscientiousness {t.get('Conscientiousness',0):.1f}, Openness {t.get('Openness',0):.1f}\n"

    prompt = f'''
You are an expert organizational psychologist analyzing a student project group.
Group Name: {group_name}
Project Topic: {topic}
Members and their traits (out of 5):
{students_info}

Write a deeply insightful, highly detailed analysis (4-5 paragraphs) of this team's dynamic.
Include:
1. An overall assessment of the team's strengths and weaknesses based on their combined traits.
2. Specific role assignments for EVERY individual member based on their unique traits (e.g., who is the Project Manager, who is the Creative Lead, who is the Debugger). Explain WHY.
3. A detailed prediction of a specific internal conflict they might face midway through the project, and how they can resolve it.
Return plain text formatted nicely with markdown.
'''
    return ask_ollama(prompt)

def generate_mentor_briefing(mentor, group):
    prompt = f'''
You are a senior mentorship coach advising a faculty mentor on how to handle their newly assigned student group.
Mentor Name: {mentor['name']}
Mentor Traits: E:{mentor['extraversion']:.1f}, N:{mentor['neuroticism']:.1f}, A:{mentor['agreeableness']:.1f}, C:{mentor['conscientiousness']:.1f}, O:{mentor['openness']:.1f}

Group Name: {group['name']}
Project Topic: {group['project_topic']}
Aggregated Group Traits: E:{group['extraversion']:.1f}, N:{group['neuroticism']:.1f}, A:{group['agreeableness']:.1f}, C:{group['conscientiousness']:.1f}, O:{group['openness']:.1f}

Provide a CONCISE, highly structured strategic coaching briefing directly addressing the mentor.
Format your response exactly like this:

### Mentor-Group Dynamic
[One very brief paragraph explaining how their specific traits complement or clash with the group]

### Actionable Tips
- **[Tip 1]:** [1 sentence advice]
- **[Tip 2]:** [1 sentence advice]
- **[Tip 3]:** [1 sentence advice]

Return plain text formatted nicely with markdown. DO NOT write long essays. Keep it punchy and short.
'''
    return ask_ollama(prompt)
