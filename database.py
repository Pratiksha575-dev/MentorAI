import psycopg2
import json

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "connectai",
    "user": "postgres",
    "password": "fctd"
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # DO NOT DROP TABLES!
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mentors (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            domains JSONB DEFAULT '[]'::jsonb,
            extraversion REAL,
            neuroticism REAL,
            agreeableness REAL,
            conscientiousness REAL,
            openness REAL,
            ai_summary TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_groups (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            project_topic VARCHAR(255) NOT NULL,
            extraversion REAL,
            neuroticism REAL,
            agreeableness REAL,
            conscientiousness REAL,
            openness REAL,
            ai_group_dynamic TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            group_id INTEGER REFERENCES student_groups(id) ON DELETE CASCADE,
            name VARCHAR(100) NOT NULL,
            extraversion REAL,
            neuroticism REAL,
            agreeableness REAL,
            conscientiousness REAL,
            openness REAL,
            ai_role_description TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    conn.commit()
    cursor.close()
    conn.close()

# --- MENTORS ---
def save_mentor(name, domains, traits, ai_summary=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO mentors (name, domains, extraversion, neuroticism, agreeableness, conscientiousness, openness, ai_summary)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
    ''', (name, json.dumps(domains), traits.get('Extraversion',0), traits.get('Neuroticism',0), traits.get('Agreeableness',0), traits.get('Conscientiousness',0), traits.get('Openness',0), ai_summary))
    m_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return m_id

def get_all_mentors():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, domains, extraversion, neuroticism, agreeableness, conscientiousness, openness, ai_summary FROM mentors;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"id": r[0], "name": r[1], "domains": r[2], "extraversion": r[3], "neuroticism": r[4], "agreeableness": r[5], "conscientiousness": r[6], "openness": r[7], "ai_summary": r[8]} for r in rows]

# --- STUDENT GROUPS ---
def save_student_group(name, project_topic, traits, ai_group_dynamic=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO student_groups (name, project_topic, extraversion, neuroticism, agreeableness, conscientiousness, openness, ai_group_dynamic)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
    ''', (name, project_topic, traits.get('Extraversion',0), traits.get('Neuroticism',0), traits.get('Agreeableness',0), traits.get('Conscientiousness',0), traits.get('Openness',0), ai_group_dynamic))
    g_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return g_id

def get_all_groups():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, project_topic, extraversion, neuroticism, agreeableness, conscientiousness, openness, ai_group_dynamic FROM student_groups;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"id": r[0], "name": r[1], "project_topic": r[2], "extraversion": r[3], "neuroticism": r[4], "agreeableness": r[5], "conscientiousness": r[6], "openness": r[7], "ai_group_dynamic": r[8]} for r in rows]

# --- STUDENTS ---
def save_student(group_id, name, traits, ai_role=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO students (group_id, name, extraversion, neuroticism, agreeableness, conscientiousness, openness, ai_role_description)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
    ''', (group_id, name, traits.get('Extraversion',0), traits.get('Neuroticism',0), traits.get('Agreeableness',0), traits.get('Conscientiousness',0), traits.get('Openness',0), ai_role))
    s_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return s_id

def get_students_by_group(group_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, extraversion, neuroticism, agreeableness, conscientiousness, openness, ai_role_description FROM students WHERE group_id = %s;", (group_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"id": r[0], "name": r[1], "extraversion": r[2], "neuroticism": r[3], "agreeableness": r[4], "conscientiousness": r[5], "openness": r[6], "ai_role_description": r[7]} for r in rows]
