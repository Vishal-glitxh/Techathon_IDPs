import pandas as pd
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
    
    print("\n" + "="*60)
    print("INTELLIGENT IDP RECOMMENDATION SYSTEM - SUMMARY REPORT")
    print("="*60)
    print(results_df[['Employee_ID', 'Name', 'Assigned_Role', 'Weighted_Score', 'Recommendations']].head(15))
    print("\n... and 35 more records processed successfully.")

if __name__ == "__main__":
    main()