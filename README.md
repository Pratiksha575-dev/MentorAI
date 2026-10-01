# MentorAI 🧠

**Intelligent Mentor-Mentee Project Alignment Engine**

MentorAI is a next-generation EdTech platform that uses Unsupervised Machine Learning, Graph Theory, and local Large Language Models (LLMs) to automatically construct and allocate optimal student project groups to university faculty mentors based on psychometric compatibility.

## 🌟 Key Features

*   **Big Five Personality Profiling:** Replaces tedious manual pairing with mathematical psychometric matching. Mentors and students take a targeted assessment to calculate their Big Five traits (Extraversion, Neuroticism, Agreeableness, Conscientiousness, Openness).
*   **Intelligent Allocation Engine:** A custom scoring algorithm that pairs student groups with faculty based on complimentary traits, shared domains (e.g., Fintech, AI), and clash-prevention mechanisms.
*   **LLM Mentor Briefings (Ollama):** Integrates with a local Llama 3.2 model to automatically generate highly structured coaching briefings. It predicts internal team conflicts before they happen and provides actionable leadership advice for the professor.
*   **Dynamic ML Insights:** Runs real-time **K-Means Clustering** across the entire university database to discover hidden personality archetypes, visualized in an interactive Plotly 3D scatter plot.
*   **The Neural Web (Graph ML):** Uses `networkx` and `pyvis` physics engines to project the university's social fabric. Highly compatible nodes (people) are pulled together by gravity to form distinct "Super-Teams."
*   **Premium Glassmorphic UI:** A beautifully customized Streamlit interface featuring gradient typography, hover-animated trait cards, and a sleek dark mode layout.

---

## 🚀 Getting Started

### 1. Prerequisites
*   **Python 3.10+**
*   **PostgreSQL** (running locally on port 5432)
*   **Ollama** (installed locally with `llama3.2:latest` model pulled)

### 2. Installation & Setup

Clone the repository and install the required dependencies:

```bash
# Clone the repository
git clone https://github.com/Pratiksha575-dev/MentorAI.git
cd MentorAI

# Install Python dependencies
pip install streamlit psycopg2-binary scikit-learn plotly networkx pyvis numpy requests
```

### 3. Database Configuration

1. Open your PostgreSQL terminal (or pgAdmin).
2. Create the database and user:
```sql
CREATE DATABASE connectai;
CREATE USER postgres WITH PASSWORD 'fctd';
GRANT ALL PRIVILEGES ON DATABASE connectai TO postgres;
```
*(Note: If you use a different password or database name, update `config/db.py` accordingly).*

### 4. Seeding the Database

You can manually register users through the UI, but it's much more impressive to start with a populated university dataset.

Run the seed script to automatically inject 5 fully-profiled Faculty Mentors and 15 dynamic Student Groups (with generated AI summaries) directly into the database:

```bash
python seed_v2.py
```

### 5. Running the Application

Launch the Streamlit server:

```bash
python -m streamlit run app.py
```
Navigate to `http://localhost:8501` in your browser. Ensure your local Ollama server is running in the background for the AI Summaries to generate successfully!

---

## 🛠️ Tech Stack
*   **Frontend:** Streamlit, Custom CSS, PyVis, Plotly
*   **Backend:** Python
*   **Database:** PostgreSQL (`psycopg2`)
*   **Machine Learning:** Scikit-Learn (K-Means), NetworkX (Graph Theory)
*   **AI / LLM:** Ollama (Llama 3.2 via local REST API)
