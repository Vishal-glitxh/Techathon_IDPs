def get_recommendations(df):
    """
    Generates a structured dictionary of personalized development activities with resources.
    Returns: { emp_id: { 'activities': [{'name': str, 'url': str}], 'mentorship': str, 'rotation': str } }
    """
    # Resource Library
    RESOURCE_MAP = {
        "High-Stakes Decision Making (Stanford Online)": "https://online.stanford.edu/courses/xelp240-making-high-quality-decisions",
        "Advanced Technical Certification (Cloud/AI)": "https://www.coursera.org/specializations/cloud-computing",
        "Executive Presence & Storytelling Masterclass": "https://www.linkedin.com/learning/executive-presence-on-video-calls",
        "Global Strategy & Market Expansion": "https://www.coursera.org/learn/international-business-1",
        "Strategic Influencing Skills": "https://www.linkedin.com/learning/strategic-influence",
        "Technical Speaking: Lead Quarterly Tech Talk": "https://www.pluralsight.com/blog/career/how-to-give-a-great-technical-talk",
        "Performance Management Fundamentals": "https://www.linkedin.com/learning/performance-management-fundamentals",
        "Collaborative Project Management": "https://www.coursera.org/learn/project-management-foundations",
        "Advanced SQL for Data Analysis": "https://www.linkedin.com/learning/sql-for-data-analysis-2",
        "Python for Automation": "https://www.coursera.org/learn/python-crash-course",
        "Public Speaking Masterclass": "https://www.linkedin.com/learning/public-speaking-foundations",
        "Continuous Learning: Open Electives": "https://www.linkedin.com/learning/"
    }

    recommendations = {}
    for _, row in df.iterrows():
        emp_id = row['Employee_ID']
        category = row.get('Nine_Box_Category', 'Core Player')
        
        raw_activities = []
        mentorship = "Assigned Peer Mentor"
        rotation = "Stay in Current Role"
        
        # 1. Activities based on Gaps
        if row.get('Leadership_Gap', 0) > 1:
            raw_activities.append("High-Stakes Decision Making (Stanford Online)")
        if row.get('Technical_Gap', 0) > 1:
            raw_activities.append("Advanced Technical Certification (Cloud/AI)")
        if row.get('Communication_Gap', 0) > 1:
            raw_activities.append("Executive Presence & Storytelling Masterclass")
            
        # 2. Strategic Assignments based on Nine-Box
        if category == "Star":
            mentorship = "Mentorship with C-Suite Executive"
            rotation = "Cross-Functional Leadership Rotation (Operations/Strategy)"
            raw_activities.append("Global Strategy & Market Expansion")
        elif category == "Future Star":
            mentorship = "Senior Director Mentorship"
            rotation = "High-Impact Task Force (Special Projects)"
            raw_activities.append("Strategic Influencing Skills")
        elif category == "Expert Professional":
            mentorship = "Technical Subject Matter Expert (SME) Pairing"
            rotation = "R&D or Innovation Lab Stint"
            raw_activities.append("Technical Speaking: Lead Quarterly Tech Talk")
        elif category == "Rough Diamond":
            mentorship = "Performance Coaching with Department Head"
            rotation = "Job Shadowing in High-Performance Teams"
            raw_activities.append("Performance Management Fundamentals")
        elif category == "Risk":
            mentorship = "Intensive Performance Coaching"
            rotation = "Performance Improvement Plan (PIP)"
            raw_activities.append("Daily Check-ins with Immediate Manager")
        else:
            mentorship = "Managerial Mentorship"
            rotation = "Internal Team Project Lead"
            raw_activities.append("Collaborative Project Management")

        if not raw_activities:
            raw_activities.append("Continuous Learning: Open Electives")

        # Convert to structured activities with URLs
        activities_with_links = []
        for act in raw_activities:
            activities_with_links.append({
                "name": act,
                "url": RESOURCE_MAP.get(act, "#")
            })

        recommendations[emp_id] = {
            'activities': activities_with_links,
            'mentorship': mentorship,
            'rotation': rotation
        }
    return recommendations
