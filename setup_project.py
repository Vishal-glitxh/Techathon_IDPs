import os

# Define the project structure and file contents
files = {
    "data/roles.csv": """Role,Leadership,Technical,Communication
Manager,5,3,4
Team Lead,4,4,4
Senior Engineer,2,5,3""",
    
    "data/employees.csv": """Employee_ID,Experience_Years,Leadership,Technical,Communication,Performance_Score
1,3,2,4,3,3
2,7,4,5,4,5
3,1,2,2,3,2
4,10,5,3,4,4
5,4,3,4,3,3
6,6,4,4,3,4
7,2,2,3,2,2
8,5,3,5,4,4
9,8,4,4,5,5
10,3,2,3,3,3
11,12,5,5,4,5
12,4,3,3,2,3
13,5,4,4,4,4
14,2,2,5,3,4
15,7,3,4,5,4
16,1,2,2,2,2
17,9,5,4,4,5
18,3,3,3,3,3
19,6,4,5,3,4
20,4,2,4,4,3
21,5,3,3,3,3
22,8,5,4,5,5
23,2,2,3,2,2
24,10,4,5,4,5
25,3,2,4,3,3
26,7,5,3,4,4
27,1,2,2,3,2
28,4,3,4,3,3
29,6,4,4,4,4
30,2,2,5,3,3
31,5,3,3,2,3
32,9,5,5,5,5
33,3,2,3,3,3
34,11,4,4,4,4
35,4,3,4,2,3
36,7,4,5,4,5
37,1,2,2,2,2
38,5,3,4,3,3
39,8,5,4,5,5
40,3,2,3,3,3
41,6,4,4,4,4
42,4,3,5,3,4
43,2,2,4,2,3
44,10,5,5,4,5
45,3,2,3,3,2
46,7,4,4,5,4
47,1,2,2,3,2
48,5,3,4,3,3
49,9,5,5,4,5
50,4,2,3,2,3""",

    "src/gap_analysis.py": """import pandas as pd
import numpy as np

def perform_gap_analysis(employees_path, roles_path):
    # Load CSVs
    employees = pd.read_csv(employees_path)
    roles = pd.read_csv(roles_path)
    
    # Assign random role to each employee
    role_names = roles['Role'].tolist()
    np.random.seed(42)  # For reproducibility
    employees['Assigned_Role'] = np.random.choice(role_names, size=len(employees))
    
    # Merge roles data for requirement comparison
    df = employees.merge(roles, left_on='Assigned_Role', right_on='Role', suffixes=('', '_Req'))
    
    # Calculate gaps: max(0, role - employee)
    df['Leadership_Gap'] = (df['Leadership_Req'] - df['Leadership']).clip(lower=0)
    df['Technical_Gap'] = (df['Technical_Req'] - df['Technical']).clip(lower=0)
    df['Communication_Gap'] = (df['Communication_Req'] - df['Communication']).clip(lower=0)
    
    # Weighted score: 0.4 * leadership + 0.3 * technical + 0.3 * communication
    df['Weighted_Score'] = (0.4 * df['Leadership'] + 
                            0.3 * df['Technical'] + 
                            0.3 * df['Communication'])
    
    return df""",

    "src/recommendation.py": """def get_recommendations(df):
    recommendations = {}
    for _, row in df.iterrows():
        emp_id = row['Employee_ID']
        rec_list = []
        
        # Recommendation rules based on gaps
        if row['Leadership_Gap'] > 1:
            rec_list.append("Leadership Training")
        if row['Technical_Gap'] > 1:
            rec_list.append("Technical Course")
        if row['Communication_Gap'] > 1:
            rec_list.append("Communication Workshop")
        
        if not rec_list:
            rec_list.append("Maintain current performance")
            
        recommendations[emp_id] = rec_list
    return recommendations""",

    "main.py": """import pandas as pd
from src.gap_analysis import perform_gap_analysis
from src.recommendation import get_recommendations
import os

def main():
    emp_path = 'data/employees.csv'
    roles_path = 'data/roles.csv'
    
    if not os.path.exists(emp_path) or not os.path.exists(roles_path):
        print("Error: Required CSV files not found in data/ directory.")
        return

    # Run Analysis
    results_df = perform_gap_analysis(emp_path, roles_path)
    
    # Get Recommendations
    recs = get_recommendations(results_df)
    
    # Format results for display
    results_df['Recommendations'] = results_df['Employee_ID'].map(lambda x: ", ".join(recs[x]))
    
    print("\\n" + "="*60)
    print("INTELLIGENT IDP RECOMMENDATION SYSTEM - SUMMARY REPORT")
    print("="*60)
    print(results_df[['Employee_ID', 'Assigned_Role', 'Weighted_Score', 'Recommendations']].head(15))
    print("\\n... and 35 more records processed successfully.")

if __name__ == "__main__":
    main()""",

    "app.py": """import streamlit as st
import pandas as pd
from src.gap_analysis import perform_gap_analysis
from src.recommendation import get_recommendations

st.set_page_config(page_title="IDP Recommendation Engine", layout="wide")

st.title("🎯 Intelligent IDP Recommendation System")
st.markdown("Automated Career Path Analysis and Skill Gap Recommendations")

emp_path = 'data/employees.csv'
roles_path = 'data/roles.csv'

try:
    # Process Data
    df = perform_gap_analysis(emp_path, roles_path)
    recs = get_recommendations(df)
    df['Recommendations'] = df['Employee_ID'].map(lambda x: ", ".join(recs[x]))

    # Sidebar Filters
    st.sidebar.header("Filters")
    selected_role = st.sidebar.multiselect("Filter by Role", options=df['Assigned_Role'].unique(), default=df['Assigned_Role'].unique())
    
    filtered_df = df[df['Assigned_Role'].isin(selected_role)]

    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Employees", len(filtered_df))
    col2.metric("Avg. Weighted Score", round(filtered_df['Weighted_Score'].mean(), 2))
    col3.metric("Critical Gaps Identified", (filtered_df[['Leadership_Gap', 'Technical_Gap', 'Communication_Gap']] > 1).any(axis=1).sum())

    # Main Table
    st.subheader("Employee Performance and Gap Analysis")
    display_cols = ['Employee_ID', 'Assigned_Role', 'Experience_Years', 'Leadership_Gap', 'Technical_Gap', 'Communication_Gap', 'Weighted_Score']
    st.dataframe(filtered_df[display_cols], use_container_width=True)

    # Recommendations Table
    st.subheader("Personalized Development Recommendations")
    st.table(filtered_df[['Employee_ID', 'Assigned_Role', 'Recommendations']])

except Exception as e:
    st.error(f"Initialization Error: {e}")
    st.info("Please ensure 'data/employees.csv' and 'data/roles.csv' are present and properly formatted.")"""
}

def setup():
    print("Creating project structure...")
    for file_path, content in files.items():
        # Create directories if they don't exist
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        # Write the file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created: {file_path}")
    
    print("\\nSetup complete! To run the project:")
    print("1. Install dependencies: pip install pandas streamlit")
    print("2. Run CLI: python main.py")
    print("3. Run UI: streamlit run app.py")

if __name__ == "__main__":
    setup()
