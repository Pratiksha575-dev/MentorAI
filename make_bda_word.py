import docx
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = docx.Document()

# Styles
style = doc.styles['Normal']
font = style.font
font.name = 'Times New Roman'
font.size = Pt(12)

# --- COVER PAGE ---
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run('MentorAI – Data Analytics and Psychometric Network System\n')
run.bold = True
run.font.size = Pt(16)

subtitle = doc.add_paragraph('A Big Data Analytics (BDA) Mini Project Report\n\nSubmitted in partial fulfillment of the requirements of the\nUniversity of Mumbai\nFor the Degree of\nFourth Year Sem VII of Computer Engineering\n\n')
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph('Submitted By:\nAditya Yadav (72)\nPratiksha Zodge (74)\n').alignment = WD_ALIGN_PARAGRAPH.CENTER
doc.add_paragraph('Under The Guidance Of:\nProf. Vaishali Yeole\n').alignment = WD_ALIGN_PARAGRAPH.CENTER
doc.add_paragraph('Dept. Of Computer Engineering,\nSmt. Indira Gandhi College Of Engineering\nAffiliated to University of Mumbai (2026-2027)\n').alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_page_break()

# --- SECTIONS ---
sections = {
    '1. ABSTRACT': '''Assigning students to project groups and faculty mentors is conventionally random or based purely on academic grades, ignoring team dynamics. This project, MentorAI, introduces a data-driven allocation system heavily rooted in Data Analytics and Network Analysis. Built on a large public psychometric dataset (the 400 MB Kaggle Big Five Personality Test dataset containing ~1 million responses), the system utilizes an optimized data pipeline.

Using chunked Pandas operations to simulate big data processing on local hardware, the pipeline cleans null values, removes duplicate IP records, reverse-scores negatively keyed items, and normalizes the results into standard OCEAN domain scores (0–100). Exploratory Data Analysis (EDA) utilizing the Elbow method and Silhouette scores determined the optimal number of personality archetypes (k=3 to 5). 

The core of the system models the university cohort as a Similarity Graph. Network Analysis is performed by drawing edges between participants whose Euclidean trait-distance falls below a strict threshold, visualizing "super-teams" through a force-directed physics engine (PyVis). Finally, an allocation algorithm pairs groups with mentors under capacity constraints, while a local LLM (Llama 3.2) generates privacy-preserving coaching briefings based on the data vectors. The prototype successfully demonstrates the application of data analytics, clustering, and network topology in educational administration.''',

    '2. OBJECTIVE AND SCOPE': '''2.1 Problem Statement
Traditional project allocation lacks a quantitative, data-driven foundation. High-dimensional psychometric data is rarely utilized in academic team formation due to the complexity of processing and analyzing such datasets. A data analytics mechanism is required to ingest large psychometric datasets, perform exploratory clustering, model the cohort as a network graph, and generate optimized mentor-mentee pairings.

2.2 Objectives
- To acquire, clean, and analyze a ~400 MB psychometric dataset using memory-efficient (chunked) vector operations.
- To perform EDA and determine the optimal number of personality archetypes using the Elbow method (WCSS) and Silhouette scores.
- To cluster students and mentors using K-Means (with an adjustable k parameter).
- To model cohort dynamics using Network Analysis, constructing a similarity graph based on Euclidean distance thresholds.
- To build a constrained allocation engine using trait-distance, domain overlap, and mentor capacity.
- To generate privacy-preserving mentor briefings using a local LLM (Ollama) based on the analyzed data.

2.3 Scope
The scope encompasses dataset preprocessing, OCEAN profiling, unsupervised K-Means clustering, network graph generation, and LLM-assisted decision making. While the project uses standard scientific Python libraries (Pandas, Scikit-learn) on a sample dataset rather than distributed frameworks (Hadoop/Spark), it rigorously applies BDA concepts such as chunked data ingestion, anomaly removal, clustering, and graph analysis.''',

    '3. SYSTEM ANALYSIS & DESIGN': '''3.1 Existing vs Proposed System
Existing systems rely on manual sorting or simple heuristics (GPA, roll numbers). They fail to leverage available behavioral data, leading to mismatched advising styles and team friction.
The proposed system replaces manual allocation with a Data Analytics pipeline. It profiles users, clusters them via K-Means, analyzes their relational topology via NetworkX, and optimizes pairings mathematically.

3.2 System Architecture
- Data Layer: Kaggle OCEAN Dataset, Pandas chunked loading, cleaning, and normalization.
- Analytics Layer: NumPy and Scikit-Learn for K-Means clustering and Euclidean distance optimization.
- Network Layer: NetworkX and PyVis for similarity graph construction and physics-based rendering.
- Inference Layer: Ollama (Llama 3.2) for generative coaching insights based on the numerical trait vectors.
- UI & Storage Layer: Streamlit dashboard and PostgreSQL relational database.''',

    '4. DATASET AND DATA ANALYTICS (CORE BDA PIPELINE)': '''4.1 Dataset Description
The foundation of the analytics pipeline is the Kaggle Big Five Personality Test dataset (data-final.csv). At ~400 MB and containing roughly one million responses to 50 IPIP items, it serves as an excellent sample dataset for high-dimensional data processing.

4.2 Data Handling and Preprocessing
To handle the dataset efficiently on local hardware without memory exhaustion, the pipeline utilizes Pandas chunksize reading. The preprocessing steps include:
- Anomaly Detection & Removal: Dropping rows with nulls, incomplete tests (0 values), and duplicate IP addresses.
- Reverse-Scoring: Negatively keyed items (e.g., "I get stressed easily") are mathematically reversed so that higher scores consistently represent higher trait presence.
- Normalization: The 50 items are aggregated into 5 macro-traits (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism) and normalized to a 0–100 scale for unified distance calculations.

4.3 Exploratory Data Analysis (EDA) & Clustering
Unsupervised machine learning (K-Means) was applied to the 5-dimensional OCEAN space.
- The Elbow Method (tracking Within-Cluster Sum of Squares) and Silhouette Scores were calculated to identify the natural grouping of personalities, revealing optimal clusters at k=3 to k=5.
- In the live system, the K-Means algorithm dynamically recalculates based on a user-defined slider (k=2 to 6), allowing administrators to explore macro and micro behavioral archetypes in real-time.

4.4 Network Analysis & Graph Modeling
The cohort is modeled as a complex network to analyze relational dynamics:
- Nodes: Represent students and mentors.
- Edges: Formed based on a strict Similarity Threshold. If the Euclidean distance between two nodes in the 5D trait space is < 1.5, an edge is drawn.
- Network Topology: On the test cohort (64 nodes), the graph generated ~36 compatibility edges. This results in a sparse graph (density ≈ 1.8%, average degree ≈ 1.1), ensuring that edges only represent highly significant similarities.
- Visualization: Instead of static centrality layouts, a force-directed physics engine (PyVis forceAtlas2Based solver) simulates gravity, physically pulling connected nodes together to naturally reveal "Super-Team" communities without requiring explicit Louvain community detection algorithms.''',

    '5. IMPLEMENTATION & RESULTS': '''5.1 Allocation Engine
The allocation engine acts as a constraint satisfaction and optimization algorithm. It first applies hard constraints (mentor capacity limits and domain overlap). It then performs a Nearest-Neighbor style Euclidean distance check to find the mentor whose behavioral baseline is mathematically closest to the student group's aggregate trait vector.

5.2 Local LLM Integration
To maintain data privacy, the numeric trait vectors are passed to a locally hosted Large Language Model (Llama 3.2 via Ollama). The LLM translates the raw psychometric distance data into a qualitative coaching briefing, predicting friction points and offering management tips.

5.3 Results
- Pipeline Efficiency: The chunked Pandas pipeline successfully cleaned and normalized the ~400 MB dataset without memory overflow.
- Clustering: K-Means reliably isolated distinct behavioral archetypes without spatial overlap.
- Network Graph: The strict Euclidean threshold successfully filtered out weak connections, resulting in a highly interpretable similarity network.
- Inference: Local LLM generation completed in under 3 seconds per allocation, proving that on-premises AI is viable for this workload.''',

    '6. CONCLUSION & FUTURE SCOPE': '''6.1 Conclusion
MentorAI successfully demonstrates the application of Data Analytics, Machine Learning, and Network Analysis in an educational context. By processing a large psychometric dataset through a rigorous cleaning, clustering, and graphing pipeline, the system replaces arbitrary allocation with mathematically optimized, explainable pairings.

6.2 Future Scope
- Distributed Processing: Migrating the Pandas pipeline to Apache Spark or Dask to handle multi-gigabyte datasets across institutional clusters.
- Advanced Network Metrics: Implementing formal graph algorithms like Louvain community detection, Betweenness Centrality, and Eigenvector Centrality to identify key influencer students.
- Supervised Forecasting: Training a Random Forest classifier on historical graduation outcomes to predict project success rates at the time of allocation.'''
}

for heading, text in sections.items():
    doc.add_heading(heading, level=1)
    for p in text.split('\n\n'):
        doc.add_paragraph(p)

doc.save('MentorAI_BDA_Report.docx')
print("BDA Word Doc saved successfully.")
