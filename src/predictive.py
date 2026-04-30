import pandas as pd
import numpy as np
from datetime import datetime

def generate_predictions(df, progress_data):
    """
    Generates predictive analytics for Attrition Risk and Future Star potential.
    """
    predictions = []
    today = datetime.now()
    
    for _, row in df.iterrows():
        eid = str(row['Employee_ID'])
        perf = row.get('Performance_Score', 3)
        cat = row.get('Nine_Box_Category', 'Core Player')
        exp = row.get('Experience_Years', 1)
        
        # Engagement metrics
        p_info = progress_data.get(eid, {})
        completed_acts = len(p_info.get('completed', []))
        last_upd_str = p_info.get('last_updated')
        
        days_inactive = 90 # default for never updated
        if last_upd_str:
            try:
                last_upd = datetime.strptime(last_upd_str, "%Y-%m-%d")
                days_inactive = (today - last_upd).days
            except:
                pass
                
        # Flight Risk (Attrition) Logic
        # High risk if high performer but disengaged
        risk_score = 40
        
        if perf >= 4.0:
            if days_inactive > 30:
                risk_score += 35 # Disengaged high performer -> high flight risk
            if exp > 4:
                risk_score += 15 # Tenured top performer -> might be poached
        elif perf <= 2.5:
            if days_inactive > 60:
                risk_score += 25 # Low performer, disengaged
                
        if completed_acts > 2:
            risk_score -= 25 # Highly engaged in learning -> lower flight risk
            
        risk_score = max(5, min(95, risk_score))
        
        if risk_score >= 70:
            risk_label = "🔴 High Risk"
        elif risk_score >= 40:
            risk_label = "🟡 Medium Risk"
        else:
            risk_label = "🟢 Low Risk"
            
        # Future Star Probability Logic
        star_prob = 20
        if cat == "Star":
            star_prob = 95
        elif cat == "Future Star":
            star_prob = 70 + (completed_acts * 5)
        elif cat in ["Core Player", "High Achiever"]:
            star_prob = 40 + (completed_acts * 10)
        elif cat == "Rough Diamond":
            star_prob = 30 + (completed_acts * 12)
            
        if days_inactive < 15:
            star_prob += 10 # Recent activity boosts potential
            
        star_prob = max(5, min(99, star_prob))
        
        predictions.append({
            "Employee": row.get('Name', eid),
            "ID": eid,
            "Current Category": cat,
            "Flight Risk": risk_label,
            "Future Star Prob": f"{star_prob}%",
            "_risk_val": risk_score,
            "_star_val": star_prob
        })
        
    return pd.DataFrame(predictions)
