import docx
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = docx.Document()

def add_heading(text, level=1):
    h = doc.add_heading(text, level)
    for run in h.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = docx.shared.RGBColor(0, 0, 0)

def add_para(text, bold=False, align='left'):
    p = doc.add_paragraph()
    if align == 'center':
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align == 'justify':
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.bold = bold
    return p

def add_figure_placeholder(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(f"\n[INSERT IMAGE HERE]\n{text}\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.bold = True
    r.italic = True

# --- PAGE 1: TITLE PAGE ---
add_para("MentorAI – Data Analytics-Based Mentor Allocation and Psychometric Compatibility System\n", bold=True, align='center').runs[0].font.size = Pt(16)
add_para("A Big Data Analytics (BDA) Mini Project Report\n\nSubmitted in partial fulfillment of the requirements of the\nUniversity Of Mumbai\nFor the Degree of\nFourth Year Sem VII of Computer Engineering\n", align='center')
add_para("Submitted By\nAditya Yadav (72)\nPratiksha Zodge (74)\n", align='center')
add_para("Under The Guidance Of\nProf. Vaishali Yeole\n", align='center')
add_figure_placeholder("[INSERT COLLEGE LOGO HERE]")
add_para("Dept. Of Computer Engineering,\nSmt. Indira Gandhi College Of Engineering\nAffiliated to University of Mumbai (2026-2027)", align='center')
doc.add_page_break()

# --- PAGE 2: CERTIFICATE ---
add_heading("CERTIFICATE", level=1)
add_para("This is to certify that the Project Report entitled “MentorAI – Data Analytics Based Mentor Allocation and Psychometric Compatibility System” is a Bonafide work of Aditya Yadav (72), Pratiksha Zodge (74) submitted to the University of Mumbai in partial fulfillment of the requirements for the award of the degree of “Fourth Year Sem VII of Computer Engineering” in the subject of Big Data Analytics.\n\n\n\n………………………………\nProf. Vaishali Yeole\n(Internal Guide)", align='center')
doc.add_page_break()

# --- PAGE 3: INDEX ---
add_heading("INDEX / TABLE OF CONTENTS", level=1)
table = doc.add_table(rows=1, cols=3)
table.style = 'Table Grid'
hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'Sr. No.'
hdr_cells[1].text = 'Particulars'
hdr_cells[2].text = 'Page No.'
index_data = [
    ('1', 'ABSTRACT', '4'),
    ('2', 'OBJECTIVE AND SCOPE', '4'),
    ('3', 'SYSTEM ANALYSIS', '5'),
    ('4', 'SYSTEM DESIGN', '6'),
    ('5', 'DATASET AND DATA ANALYTICS', '8'),
    ('6', 'IMPLEMENTATION', '10'),
    ('7', 'RESULTS AND CONCLUSION', '12'),
    ('8', 'FUTURE SCOPE', '13'),
    ('9', 'REFERENCES', '14')
]
for sr, part, pg in index_data:
    row_cells = table.add_row().cells
    row_cells[0].text = sr
    row_cells[1].text = part
    row_cells[2].text = pg
doc.add_page_break()

# --- PAGE 4: ABSTRACT & OBJECTIVE ---
add_heading("1. ABSTRACT", level=1)
add_para("Assigning students to project groups and faculty mentors is often random, biased, or based purely on grades, ignoring team dynamics. This leads to dysfunctional teams, communication breakdowns and weak project outcomes.", align='justify')
add_para("MentorAI is a data-driven allocation system built on a large public psychometric dataset: the Kaggle Big Five Personality Test dataset (data-final.csv, about 400 MB, roughly one million responses to the 50-item IPIP Big-Five questionnaire). The data is processed with a chunked pandas pipeline that removes null, incomplete and duplicate-IP records, reverse-scores negatively keyed items and normalizes the results to OCEAN domain scores (0–100): Openness, Conscientiousness, Extraversion, Agreeableness and Neuroticism. The Elbow method and Silhouette scores show that the personality space has between k = 3 and k = 5 natural archetypes. In the live platform, K-Means is dynamic: a UI slider lets the professor vary k from 2 to 6.", align='justify')
add_para("A Euclidean-distance (nearest-neighbour style) engine pairs student groups with mentors using domain alignment, mentor capacity and trait-distance. The cohort is also modelled as a similarity graph (edge when distance < 1.5) and shown as a physics-based “Neural Web”. After pairing, a local LLM (Ollama, Llama 3.2) writes a coaching briefing for the mentor with a compatibility score, so no student data leaves the institution’s servers.", align='justify')
add_para("The stack is Python, pandas, NumPy, scikit-learn, NetworkX, PyVis, Plotly, Streamlit, PostgreSQL and Ollama. The prototype was evaluated on 17 student groups (56 students) and 8 mentors. It is an academic prototype: data is processed on a single machine (no Spark or Hadoop), and production use would need validated instruments, outcome tracking, access control and fairness auditing.", align='justify')

add_heading("2. OBJECTIVE AND SCOPE", level=1)
add_heading("2.1 Problem Statement", level=2)
add_para("Project-group and mentor allocation is usually manual or based on heuristics such as GPA, roll number or timestamp. This verifies academic standing but not interpersonal compatibility between group members, or between a group and its assigned faculty mentor. If a volatile personality mix or a mismatched advising style is assigned, the result is often a dysfunctional team, a free-rider dynamic or a stalled project, usually discovered only at midterm or final evaluation when remediation is no longer practical.\nTherefore, a data-driven allocation mechanism is required that can score every student and mentor on a validated personality model, cluster participants into behavioural archetypes, pair groups with mentors who are genuinely compatible with them, and proactively brief the mentor on how best to manage the relationship before the first meeting takes place.", align='justify')

add_heading("2.2 Objectives", level=2)
add_para("• To acquire, clean and analyse the Kaggle Big Five dataset (~400 MB) using a chunked, vectorized pandas pipeline (null/zero/duplicate removal, reverse-scoring, 0–100 normalization).\n• To perform EDA and choose the number of archetypes using the Elbow method and Silhouette scores.\n• To profile students and mentors on the OCEAN model and cluster them with K-Means (adjustable k).\n• To build a constrained allocation engine using Euclidean trait-distance, domain overlap and mentor capacity, with a 0–100 compatibility score.\n• To perform network analysis with a similarity graph and a force-directed “Neural Web”.\n• To generate privacy-preserving mentor briefings with a local LLM (Ollama / Llama 3.2) and deliver everything through a Streamlit dashboard backed by PostgreSQL.", align='justify')

add_heading("2.3 Scope and Need of the Project", level=2)
add_para("The scope covers dataset preprocessing and EDA, OCEAN profiling of students (as groups) and mentors, K-Means clustering, constrained allocation, network analysis, LLM briefings, Plotly 3-D visualization, and PostgreSQL persistence, evaluated on 17 groups (56 students) and 8 mentors. The project reduces dependence on random or GPA-only allocation, gives an auditable quantitative basis for pairings, surfaces friction points before the relationship begins, gives faculty actionable tips without manual interviews, and keeps sensitive psychometric data on local infrastructure.", align='justify')

add_heading("2.4 Methodology", level=2)
add_para("The methodology has two phases. In the offline analytics phase, the raw dataset is read in chunks, cleaned, reverse-scored and normalized; Elbow and Silhouette analysis then identify the natural number of archetypes (k = 3 to 5). In the live platform phase, groups and mentors complete the OCEAN questionnaire, participants are clustered (k from the UI slider), mentors are filtered by domain and capacity, and the pairing with minimum Euclidean trait-distance is selected. A similarity graph is built for network analysis, and the local LLM generates the score and briefing.", align='justify')
add_figure_placeholder("Figure 2.1: Methodology of the MentorAI Allocation System")
doc.add_page_break()

# --- PAGE 5: SYSTEM ANALYSIS ---
add_heading("3. SYSTEM ANALYSIS", level=1)
add_heading("3.1 Existing System", level=2)
add_para("Departments usually assign groups and mentors manually or by alphabetical order, roll number, timestamp or GPA, with the mentor chosen only by subject expertise. Its limitations are:\n• Random or GPA-only grouping pairs volatile personality mixes and ignores mentor advising style.\n• Conflicts are found only at midterm or final evaluation, and there is no auditable basis for a given pairing.\n• Faculty receive no advance briefing, and large psychometric datasets are not used.", align='justify')

add_heading("3.2 Proposed System and Features", level=2)
add_para("MentorAI replaces manual allocation with a data-analytics-driven engine. Its main features are:\n• Dataset analytics: chunked cleaning, reverse-scoring and normalization of the Kaggle OCEAN dataset, with Elbow/Silhouette-based selection of archetypes.\n• Profiling and clustering: OCEAN questionnaire for students and mentors, domain tagging, and dynamic K-Means (k = 2 to 6).\n• Allocation and scoring: Euclidean trait-distance with domain and capacity constraints, and a compatibility score such as 67/100.\n• Network analysis: similarity graph rendered as a force-directed Neural Web with “super-team” groupings.\n• Generative briefing: local Llama 3.2 coaching report with dynamics, friction points and tips.\n• Application layer: Streamlit dashboard, registration, searchable directory, 3-D cluster view and PostgreSQL persistence.", align='justify')

add_heading("3.3 Requirements", level=2)
add_para("Hardware Requirements:\n• Computer/Laptop with minimum 8 GB RAM (16 GB recommended for local LLM inference).\n• Multi-core CPU; GPU optional.\n• Sufficient storage for the PostgreSQL database and the local Llama 3.2 model weights.\n\nSoftware Requirements:\n• Windows/Linux/macOS\n• Python 3.10+\n• Streamlit, scikit-learn, Pandas, NumPy, NetworkX, PyVis, Plotly\n• Ollama with the Llama 3.2 model\n• PostgreSQL and psycopg2-binary\n• Modern web browser", align='justify')
doc.add_page_break()

# --- PAGE 6: SYSTEM DESIGN ---
add_heading("4. SYSTEM DESIGN", level=1)
add_heading("4.1 System Architecture", level=2)
add_para("The architecture is layered: Data Layer (Kaggle dataset, pandas) → Client Layer (Streamlit) → Logic & ML Layer (Pandas/NumPy, K-Means, Euclidean matching) → Inference Layer (Ollama/Llama 3.2) → Visualization Layer (Plotly, NetworkX/PyVis) → Storage Layer (PostgreSQL). The Data Layer cleans and scores the dataset and informs the choice of k; the Logic & ML Layer produces clusters and allocations; the Inference Layer writes the briefings.", align='justify')
add_figure_placeholder("Figure 4.1: System Architecture")

add_heading("4.2 System Workflow", level=2)
add_para("The complete workflow of the system is:\n1. Groups and mentors register with domain and capacity information.\n2. Each participant completes the OCEAN psychometric questionnaire; a 5-D trait vector is computed and stored in PostgreSQL.\n3. An administrator triggers allocation; K-Means clusters participants (k from the slider).\n4. Mentors are filtered by capacity and domain; Euclidean distance selects the best fit.\n5. A compatibility score is computed and the local LLM generates the mentor briefing.\n6. The similarity graph is built, results are saved to PostgreSQL and shown on the dashboard.", align='justify')
add_figure_placeholder("Figure 4.2: Mentor Allocation Workflow")

add_heading("4.3 Psychometric Matching and Compatibility Scoring", level=2)
add_para("Every group and mentor is a 5-dimensional OCEAN vector. The distance between a group’s aggregate vector x and a mentor’s baseline vector y is the Euclidean distance:\nd(x, y) = √ Σ(x_i − y_i)²\n\nLet d_min be the smallest distance among mentors who pass the hard constraints (remaining capacity and domain overlap). The compatibility score is:\nS = 100 × (1 − d_min / d_max)\nwhere d_max is the maximum possible trait-distance across the OCEAN space (approx 8.94). Higher S means closer compatibility.", align='justify')
add_figure_placeholder("Figure 4.3: Allocation Decision and Compatibility Scoring")
doc.add_page_break()

# --- PAGE 8: DATASET AND DATA ANALYTICS ---
add_heading("5. DATASET AND DATA ANALYTICS", level=1)
add_heading("5.1 Dataset Description", level=2)
add_para("The analytics foundation is the Big Five Personality Test dataset (data-final.csv) from Kaggle, collected through an online IPIP Big-Five questionnaire. At about 400 MB it is too large to load comfortably in one pass on a standard laptop, so it is treated as a big-data workload. It contains roughly one million responses to 50 items on a 1–5 scale, 10 per OCEAN trait.", align='justify')

add_heading("5.2 Big Data Handling and Preprocessing", level=2)
add_para("The ~400 MB file was read in chunks with pandas (chunksize) and all transformations were vectorized pandas/NumPy operations rather than row loops. The steps include:\n• Missing data and duplicates: dropped rows with nulls, incomplete tests (items answered 0) and duplicate IP addresses.\n• Reverse-scoring: negatively keyed items were reversed (score → 6 − score) so higher always means more of the trait.\n• Aggregation and normalization: the ten items per trait were aggregated and linearly rescaled from 1–5 to standardized 0–100 domain scores.", align='justify')
add_figure_placeholder("Figure 5.1: Big Data Analytics Pipeline for the OCEAN Dataset")

add_heading("5.3 EDA and Cluster Analysis (K-Means)", level=2)
add_para("K-Means (scikit-learn) is used for unsupervised archetype discovery from the 5-D scores alone. The Elbow method (WCSS) and Silhouette scores showed that the natural number of archetypes lies between k = 3 and k = 5. Because MentorAI is a live platform, k is passed from a UI slider into the model, so the professor can toggle k between 2 and 6 and view macro or micro archetypes in real time.", align='justify')
add_figure_placeholder("Figure 5.2: 3-D Personality Clusters")
add_figure_placeholder("Figure 5.3: Cluster Archetype Centres")

add_heading("5.4 Network Analysis", level=2)
add_para("The cohort is also analysed as a network built with NetworkX. Each participant is a node, and an edge is drawn when the Euclidean distance between two users in the 5-D space is below a strict threshold (e.g., 1.5). On the seeded population, the graph has 64 nodes (8 mentors, 56 students) and 36 compatibility edges, giving a density of ~1.8% and an average degree of about 1.1, so the graph is sparse and links only genuinely similar participants.\nInstead of computing Louvain communities or betweenness centrality, the graph is rendered with a physics-based gravity simulation (PyVis forceAtlas2Based solver): highly connected nodes are pulled together, so visual communities and “Super-Teams” emerge naturally.", align='justify')
add_figure_placeholder("Figure 5.4: Neural Web Similarity Graph")
doc.add_page_break()

# --- PAGE 10: IMPLEMENTATION ---
add_heading("6. IMPLEMENTATION", level=1)
add_heading("6.1 Profiling and Allocation Engine", level=2)
add_para("Every participant is recorded with an advising/working persona including Domain Expertise (Machine Learning, Fintech, etc.) and Advising Traits quantified across OCEAN. The allocation engine balances Hard Constraints (mentor bandwidth limits and domain alignment) and Soft Optimization (minimizing interpersonal friction by matching the group's composite psychometric scores against the mentor's behavioural baseline using trait-distance).", align='justify')

add_heading("6.2 Generative Mentor Briefing (Local LLM)", level=2)
add_para("When matching completes, an inference pipeline runs locally via Ollama. The input context includes the mentor trait-score vector, student project topic, and group OCEAN aggregates. The inference output is a compatibility score (e.g., 67/100), an assessment of mentor-group dynamics, and concrete management directives. Because inference runs on a local Ollama instance hosting Llama 3.2, no sensitive psychometric data is transmitted to an external cloud API.", align='justify')

add_heading("6.3 Streamlit Web Application & PostgreSQL", level=2)
add_para("The Streamlit layer provides the browser-based dashboard. The UI follows a dark, glassmorphic design. It provides a live dashboard, mentor/student registration, a searchable directory, ML Insights (3-D clustering), Neural Web (relationship graph), and a one-click allocation trigger.\nPostgreSQL is selected for structured relational records (profiles, trait scores, allocations). The backend uses psycopg2-binary.", align='justify')

add_heading("6.4 Output", level=2)
add_para("The final system provides the following outputs:\n• Live dashboard with registered-mentor, student-group and total-student counts.\n• 3-D K-Means cluster plot and Archetype radar charts.\n• Compatibility score (e.g., 67/100) for every confirmed allocation.\n• AI-generated mentor briefing with dynamics assessment.\n• Neural Web relationship graph.", align='justify')
add_figure_placeholder("Figure 6.1: MentorAI Dashboard")
add_figure_placeholder("Figure 6.2: AI-Generated Mentor Briefing and Compatibility Score")
doc.add_page_break()

# --- PAGE 12: RESULTS AND CONCLUSION ---
add_heading("7. RESULTS AND CONCLUSION", level=1)
add_heading("7.1 Results", level=2)
add_para("The prototype was evaluated on 17 student groups (56 students) and 8 mentors. The ~400 MB Kaggle dataset was successfully loaded, reverse-scored, and normalized on local hardware using chunked processing. Clustering successfully isolated mentors and student cohorts into distinct groups. Network analysis generated 64 nodes and 36 edges (threshold 1.5). Allocation completed in milliseconds, and Llama 3.2 inference completed in under 3 seconds per allocation.", align='justify')

add_heading("7.2 Key Findings", level=2)
add_para("• A ~400 MB dataset can be cleaned and scored on one machine using chunked pandas and vectorized operations, without a distributed framework.\n• Reverse-scoring and normalization are essential; otherwise the traits are not comparable for distance-based methods.\n• The OCEAN space supports about three to five archetypes.\n• Hard constraints must be applied before distance optimization.\n• A strict similarity threshold gives a sparse, readable network that highlights genuinely similar participants.\n• Local LLM inference (sub-3 seconds) shows privacy-preserving generative AI is highly practical.", align='justify')

add_heading("7.3 Conclusion", level=2)
add_para("MentorAI demonstrates how big-data preprocessing, unsupervised learning, network analysis and a privacy-preserving local LLM can form an end-to-end academic project allocation workflow. The system scores students and mentors on the Big-Five (OCEAN) personality model, clusters participants into behavioural archetypes, optimizes mentor-group pairings under capacity and domain constraints, and generates a proactive coaching briefing for every confirmed pairing.", align='justify')
doc.add_page_break()

# --- PAGE 13: FUTURE SCOPE ---
add_heading("8. FUTURE SCOPE", level=1)
add_para("• Distributed processing: move preprocessing and clustering to Spark or Dask for multi-institution datasets, with streaming ingestion of new submissions.\n• Advanced network analytics: implement formal Louvain communities and betweenness/degree centrality on the similarity graph.\n• Supervised success forecasting: train a Random Forest classifier on historical outcomes to predict project risk at allocation time.\n• Audio-based profiling and RAG: infer OCEAN indicators from speech samples, and let faculty upload briefs and rubrics for milestone-specific LLM guidance.\n• Fairness auditing and longitudinal tracking: audit the algorithm for bias and compare predicted compatibility with real project outcomes.", align='justify')
doc.add_page_break()

# --- PAGE 14: REFERENCES ---
add_heading("9. REFERENCES", level=1)
add_para("1. Big Five Personality Test (data-final.csv), Kaggle dataset – https://www.kaggle.com/datasets/tunguz/big-five-personality-test\n2. Open Psychometrics – Raw Data (IPIP Big-Five responses) – https://openpsychometrics.org/_rawdata/\n3. Python, pandas, NumPy, scikit-learn, NetworkX, PyVis, Plotly and Streamlit documentation.\n4. PostgreSQL and psycopg2 documentation.\n5. Ollama and Meta AI Llama 3 model card.\n6. Costa, P. T., & McCrae, R. R. – NEO-PI-R and NEO-FFI Professional Manual, Psychological Assessment Resources, 1992.\n7. Goldberg, L. R. – The Structure of Phenotypic Personality Traits, American Psychologist, 48(1), 26–34, 1993.\n8. MacQueen, J. – Some Methods for Classification and Analysis of Multivariate Observations, 5th Berkeley Symposium, 1967.\n9. Rousseeuw, P. J. – Silhouettes: A Graphical Aid to the Interpretation and Validation of Cluster Analysis, J. Computational and Applied Mathematics, 20, 53–65, 1987.\n10. Jacomy, M., Venturini, T., Heymann, S., & Bastian, M. – ForceAtlas2, a Continuous Graph Layout Algorithm for Handy Network Visualization, PLoS ONE, 9(6), e98679, 2014.", align='justify')

doc.save('MentorAI_BDA_Full_Report.docx')
print("Full BDA Word Doc saved successfully.")
