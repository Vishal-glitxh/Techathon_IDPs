import pandas as pd
import numpy as np

def perform_gap_analysis(employees_path, roles_path):
    # Load CSVs with forced string IDs for robustness
    try:
        employees = pd.read_csv(employees_path, dtype={'Employee_ID': str})
        roles = pd.read_csv(roles_path)
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()
    
    # Clean column names (strip whitespace)
    employees.columns = [col.strip() for col in employees.columns]
    roles.columns = [col.strip() for col in roles.columns]
    
    # Ensure mandatory columns exist
    mandatory_emp = ['Employee_ID', 'Leadership', 'Technical', 'Communication', 'Performance_Score']
    for col in mandatory_emp:
        if col not in employees.columns:
            employees[col] = 0 if col != 'Employee_ID' else "N/A"
    
    # Standardize 'Name' column if it exists under a different variation
    name_variations = ['Name', 'Full Name', 'Employee Name', 'Employee_Name', 'Full_Name']
    found_name_col = None
    for col in employees.columns:
        if col.title() in name_variations or col.upper() in [v.upper() for v in name_variations]:
            found_name_col = col
            break
    
    if found_name_col:
        employees = employees.rename(columns={found_name_col: 'Name'})
    else:
        # If no name column is found, use Employee_ID as Name for display consistency
        employees['Name'] = employees['Employee_ID'].astype(str)
    
    # Assign random role to each employee if not already assigned
    if 'Assigned_Role' not in employees.columns:
        role_names = roles['Role'].tolist()
        if role_names:
            np.random.seed(42)  # For reproducibility
            employees['Assigned_Role'] = np.random.choice(role_names, size=len(employees))
        else:
            employees['Assigned_Role'] = "Unknown"
    
    # Merge roles data for requirement comparison
    df = employees.merge(roles, left_on='Assigned_Role', right_on='Role', suffixes=('', '_Req'))
    
    # Calculate gaps: max(0, role - employee)
    for skill in ['Leadership', 'Technical', 'Communication']:
        req_col = f'{skill}_Req'
        if req_col not in df.columns: df[req_col] = 3 # Default req
        df[f'{skill}_Gap'] = (df[req_col] - df[skill]).clip(lower=0)
    
    # Weighted score: 0.4 * leadership + 0.3 * technical + 0.3 * communication
    df['Weighted_Score'] = (0.4 * df['Leadership'].fillna(0) + 
                            0.3 * df['Technical'].fillna(0) + 
                            0.3 * df['Communication'].fillna(0))

    # 9-Box Matrix Calculation
    def get_nine_box(row):
        perf = float(row.get('Performance_Score', 0))
        pot = float(row.get('Potential_Score', row['Weighted_Score']))
        
        if pot >= 4:
            if perf >= 4: return ("Star", "Executive Track / Job Rotation")
            if perf >= 2.5: return ("Future Star", "Mentorship / High-Visibility Projects")
            return ("Rough Diamond", "Strategic Assignments / Performance Coaching")
        elif pot >= 2.5:
            if perf >= 4: return ("High Achiever", "Leadership Training / Mentorship")
            if perf >= 2.5: return ("Core Player", "Professional Development / Project Ownership")
            return ("Inconsistent Performer", "Skill Development / Intensive Coaching")
        else:
            if perf >= 4: return ("Expert Professional", "Specialty Focus / Recognition")
            if perf >= 2.5: return ("Solid Performer", "Role Enrichment / Internal Projects")
            return ("Risk", "Performance Coaching / Re-assignment")

    df[['Nine_Box_Category', 'Nine_Box_Guideline']] = df.apply(
        lambda x: pd.Series(get_nine_box(x)), axis=1
    )
    
    return df
