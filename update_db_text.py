import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "connectai",
    "user": "postgres",
    "password": "fctd"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

mentor_summaries = {
    "Dr. Alan Turing": "Dr. Turing's approach is deeply analytical and highly structured. Expect rigorous weekly code reviews and a strict adherence to logic. He synergizes best with groups that are highly conscientious and prepared, but may clash with highly neurotic groups who panic easily.",
    "Prof. Ada Lovelace": "Prof. Lovelace is incredibly supportive and visionary. She prefers to focus on the big-picture architecture of a project rather than micromanaging the daily tasks. Highly open and agreeable, she is perfect for creative groups but might not provide enough discipline for unorganized teams.",
    "Dr. Grace Hopper": "Dr. Hopper is hands-on and expects extreme dedication. Her 'no-nonsense' communication style means feedback is direct and immediate. She excels at pushing high-potential groups to their absolute limit, but highly agreeable students may find her intimidating at first.",
    "Dr. John von Neumann": "Dr. von Neumann thrives on complex mathematical problem-solving. He treats mentorship like a collaborative research endeavor. He expects students to be highly independent and intellectually curious, often ignoring groups that need constant hand-holding.",
    "Prof. Margaret Hamilton": "Prof. Hamilton emphasizes robust software engineering practices and extreme reliability. Her management style is deeply organized and preventative. She works perfectly with chaotic, high-neuroticism groups by grounding them in strict protocols."
}

group_dynamic_template = "This group exhibits a fascinating blend of traits. Their high openness suggests they will generate highly creative and innovative solutions, while their average agreeableness means internal debates will be productive but sometimes tense. The primary risk factor is their varied conscientiousness—while some members will push for early deadlines, others might procrastinate, leading to potential conflict around milestone deliveries. If they establish clear roles early on, they have the potential to deliver an outstanding project."

def update_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    for name, summary in mentor_summaries.items():
        cur.execute("UPDATE mentors SET ai_summary = %s WHERE name = %s", (summary, name))
        
    cur.execute("UPDATE student_groups SET ai_group_dynamic = %s", (group_dynamic_template,))
    
    conn.commit()
    cur.close()
    conn.close()
    print("Database updated with realistic summaries!")

if __name__ == '__main__':
    update_db()
