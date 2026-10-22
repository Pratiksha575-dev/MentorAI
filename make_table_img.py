import matplotlib.pyplot as plt
import pandas as pd

data = [
    ['1', 'ABSTRACT', '3'],
    ['2', 'OBJECTIVE AND SCOPE', '3'],
    ['2.1', '  Problem Statement', '3'],
    ['2.2', '  Objectives', '3'],
    ['2.3', '  Scope and Need of the Project', '3'],
    ['2.4', '  Methodology', '4'],
    ['3', 'SYSTEM ANALYSIS', '4'],
    ['3.1', '  Existing System', '4'],
    ['3.2', '  Proposed System and Features', '4'],
    ['3.3', '  Requirements', '4'],
    ['4', 'SYSTEM DESIGN', '5'],
    ['4.1', '  System Architecture', '5'],
    ['4.2', '  System Workflow', '5'],
    ['4.3', '  Psychometric Matching and Compatibility Scoring', '6'],
    ['4.4', '  Technology Used', '6'],
    ['5', 'DATASET AND DATA ANALYTICS', '6'],
    ['5.1', '  Dataset Description', '6'],
    ['5.2', '  Big Data Handling and Preprocessing', '7'],
    ['5.3', '  EDA and Cluster Analysis (K-Means)', '7'],
    ['5.4', '  Network Analysis', '8'],
    ['6', 'IMPLEMENTATION', '8'],
    ['6.1', '  Profiling and Allocation Engine', '8'],
    ['6.2', '  Generative Mentor Briefing (Local LLM)', '8'],
    ['6.3', '  Streamlit Application and PostgreSQL', '9'],
    ['6.4', '  Output', '9'],
    ['7', 'RESULTS AND CONCLUSION', '9'],
    ['7.1', '  Results', '9'],
    ['7.2', '  Key Findings', '9'],
    ['7.3', '  Conclusion', '10'],
    ['8', 'FUTURE SCOPE', '10'],
    ['9', 'REFERENCES', '10']
]

df = pd.DataFrame(data, columns=['Sr. No.', 'Particulars', 'Page No.'])

fig, ax = plt.subplots(figsize=(10, 12))
ax.axis('tight')
ax.axis('off')

table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='left')

table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 1.8)

# Formatting
for (i, j), cell in table.get_celld().items():
    # Header
    if i == 0:
        cell.set_text_props(weight='bold', color='white', ha='center')
        cell.set_facecolor('#2C3E50') # Dark blue/slate
    else:
        # Center align columns 0 and 2
        if j == 0 or j == 2:
            cell.set_text_props(ha='center')
            
        # Alternate row colors for readability
        if i % 2 == 0:
            cell.set_facecolor('#F8F9FA')
        else:
            cell.set_facecolor('white')
            
    # Set specific column widths
    if j == 0:
        cell.set_width(0.12)
    elif j == 1:
        cell.set_width(0.76)
    elif j == 2:
        cell.set_width(0.12)

plt.title('INDEX / TABLE OF CONTENTS', fontweight='bold', fontsize=16, pad=20)
plt.tight_layout()
plt.savefig('index_table.png', bbox_inches='tight', dpi=300)
print('Image saved as index_table.png')
