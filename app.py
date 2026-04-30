import streamlit as st
import pandas as pd
import numpy as np
import os
import json
from datetime import datetime
import plotly.graph_objects as go
from src.gap_analysis import perform_gap_analysis
from src.recommendation import get_recommendations
from src.predictive import generate_predictions

# --- PREMIUM MINIMALIST CSS ---
def inject_modern_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        :root {
            --primary: #6366f1;
            --primary-light: #818cf8;
            --bg-dark: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --border: rgba(255, 255, 255, 0.08);
            --text-muted: #94a3b8;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #f8fafc;
        }

        /* Premium Minimalist Header */
        .premium-header {
            font-size: 2.2rem !important;
            font-weight: 800 !important;
            letter-spacing: -1px !important;
            background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem !important;
        }

        .premium-sub {
            color: var(--text-muted) !important;
            font-size: 0.95rem !important;
            font-weight: 400 !important;
            letter-spacing: 0.5px;
            margin-bottom: 2rem !important;
            text-transform: uppercase;
        }

        /* Glassmorphism Cards */
        div[data-testid="stExpander"], .stAlert, div[data-testid="stMetric"] {
            background: var(--card-bg) !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid var(--border) !important;
            border-radius: 16px !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
            padding: 1.25rem !important;
        }

        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: transparent;
        }

        .stTabs [data-baseweb="tab"] {
            height: 40px;
            white-space: pre;
            background-color: rgba(255, 255, 255, 0.03);
            border-radius: 8px 8px 0px 0px;
            color: var(--text-muted);
            border: none;
            padding: 0px 20px;
            font-weight: 500;
        }

        .stTabs [aria-selected="true"] {
            background-color: rgba(99, 102, 241, 0.1) !important;
            color: var(--primary-light) !important;
            border-bottom: 2px solid var(--primary) !important;
        }

        /* Button Styling */
        .stButton>button {
            background: linear-gradient(135deg, var(--primary) 0%, #4f46e5 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.6rem 1.5rem !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2) !important;
        }

        .stButton>button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 15px rgba(99, 102, 241, 0.3) !important;
            opacity: 0.9;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #020617 !important;
            border-right: 1px solid var(--border);
        }

        /* Dataframe Tuning */
        [data-testid="stDataFrame"] {
            border: 1px solid var(--border) !important;
            border-radius: 12px !important;
        }

        /* Hide Streamlit elements for clean look */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        </style>
    """, unsafe_allow_html=True)

inject_modern_css()

# --- AUTHENTICATION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'auth' not in st.session_state:
    st.session_state.auth = {'logged_in': False, 'role': None, 'user_id': None}

# --- LANDING INTERFACE ---
def show_landing():
    # Hero Section
    st.markdown("""
        <div style="text-align: center; padding: 60px 20px; background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(142, 84, 233, 0.1) 100%); border-radius: 30px; border: 1px solid rgba(255, 255, 255, 0.05); margin-bottom: 40px;">
            <h1 class="premium-header" style="font-size: 3.5rem !important;">Empower Your Growth DNA</h1>
            <p style="font-size: 1.2rem; color: #94a3b8; max-width: 800px; margin: 20px auto;">
                Core Talent is an intelligent Individual Development Plan (IDP) platform designed to bridge the gap between your current skills and your future career aspirations.
            </p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
            <div style="background: var(--card-bg); padding: 30px; border-radius: 20px; border: 1px solid var(--border); height: 100%;">
                <h3 style="color: #6366f1;">🎯 Clear Pathways</h3>
                <p style="color: #94a3b8; font-size: 0.9rem;">Instantly visualize your skill gaps against industry-standard roles. Know exactly what you need to master to reach the next level.</p>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div style="background: var(--card-bg); padding: 30px; border-radius: 20px; border: 1px solid var(--border); height: 100%;">
                <h3 style="color: #8E54E9;">🚀 AI Recommendations</h3>
                <p style="color: #94a3b8; font-size: 0.9rem;">Receive personalized learning activities, mentorship pairings, and job rotation suggestions powered by predictive analytics.</p>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
            <div style="background: var(--card-bg); padding: 30px; border-radius: 20px; border: 1px solid var(--border); height: 100%;">
                <h3 style="color: #22c55e;">📈 Trackable Success</h3>
                <p style="color: #94a3b8; font-size: 0.9rem;">Monitor your progress in real-time, earn badges, and maintain a collaborative journal with your manager to keep growth alive.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col_btn, _ = st.columns([1, 2])
    with col_btn:
        if st.button("Get Started →", use_container_width=True):
            st.session_state.page = 'login'
            st.rerun()

    st.markdown("""
        <div style="margin-top: 60px; padding: 40px; border-top: 1px solid var(--border);">
            <h2 style="font-weight: 700;">How it benefits you:</h2>
            <ul style="color: #94a3b8; line-height: 1.8;">
                <li><b>No more "Set and Forget":</b> Monthly journals keep your development plan active and relevant.</li>
                <li><b>Evidence-Based Promotion:</b> Upload proof of your learning to build a solid case for your next career move.</li>
                <li><b>Gamified Learning:</b> Level up and earn skill badges as you complete your development modules.</li>
                <li><b>Transparency:</b> See exactly how the organization views your potential through the 9-Box Matrix.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# --- LOGIN INTERFACE ---
def show_login():
    if st.button("← Back to Overview"):
        st.session_state.page = 'landing'
        st.rerun()
        
    st.markdown('<h1 class="premium-header">Secure Gateway</h1>', unsafe_allow_html=True)
    st.markdown('<p class="premium-sub">Access your personal development portal</p>', unsafe_allow_html=True)
    
    with st.container():
        role = st.selectbox("Select Role", ["Employee", "Admin"])
        user_id = st.text_input("Username / ID", placeholder="Employee ID or Name")
        token = st.text_input("Password / Token", type="password")
        
        if st.button("Initialize Session", use_container_width=True):
            u_id_raw = user_id.strip().lower()
            t_kn_raw = token.strip().lower()
            
            if role == "Admin":
                if u_id_raw == "admin" and t_kn_raw == "admin123":
                    st.session_state.auth = {'logged_in': True, 'role': 'Admin', 'user_id': 'Admin'}
                    st.rerun()
                else:
                    st.error("Invalid Admin credentials.")
            elif role == "Employee":
                try:
                    if not os.path.exists('data/employees.csv'):
                        st.error("Employee database not found.")
                    else:
                        data = pd.read_csv('data/employees.csv')
                        data.columns = [col.strip() for col in data.columns]
                        id_col = 'Employee_ID' if 'Employee_ID' in data.columns else data.columns[0]
                        name_col = next((c for c in data.columns if 'name' in c.lower()), None)
                        
                        id_map = {str(row[id_col]).strip().lower(): str(row[id_col]) for _, row in data.iterrows()}
                        name_map = {}
                        name_to_id = {}
                        if name_col:
                            for _, row in data.iterrows():
                                n_key = str(row[name_col]).strip().lower()
                                i_val = str(row[id_col])
                                name_map[n_key] = i_val
                                name_to_id[i_val.lower()] = n_key
                        
                        target_id = id_map.get(u_id_raw) or name_map.get(u_id_raw)
                        valid_passwords = ["user123"]
                        if target_id:
                            valid_passwords.append(target_id.lower())
                            if target_id.lower() in name_to_id:
                                valid_passwords.append(name_to_id[target_id.lower()])
                        
                        if target_id and t_kn_raw in valid_passwords:
                            st.session_state.auth = {'logged_in': True, 'role': 'Employee', 'user_id': target_id}
                            st.rerun()
                        else:
                            st.error("Invalid credentials. Please try again.")
                except Exception as e:
                    st.error(f"Authentication error: {e}")

# --- DASHBOARD INTERFACE ---
def show_dashboard():
    # Sidebar
    with st.sidebar:
        st.markdown('<h2 style="color: #4776E6;">💠 CORE PRO</h2>', unsafe_allow_html=True)
        st.write(f"**Session:** {st.session_state.auth['role']}")
        st.write(f"**Identity:** {st.session_state.auth['user_id']}")
        st.divider()
        
        if st.session_state.auth['role'] == "Admin":
            st.markdown('<p class="premium-sub">Master Data Sync</p>', unsafe_allow_html=True)
            uploaded_files = st.file_uploader("Upload CSVs", type="csv", accept_multiple_files=True)
            
            if uploaded_files:
                if st.button("Apply Changes & Refresh", use_container_width=True):
                    for file in uploaded_files:
                        try:
                            # Robust Peek
                            df_peek = pd.read_csv(file)
                            df_peek.columns = [c.strip().lower() for c in df_peek.columns]
                            if any("employee_id" in c for c in df_peek.columns):
                                with open('data/employees.csv', 'wb') as f: f.write(file.getbuffer())
                                st.success(f"Employees Synced")
                            elif any("role" in c for c in df_peek.columns):
                                with open('data/roles.csv', 'wb') as f: f.write(file.getbuffer())
                                st.success(f"Roles Synced")
                        except Exception as e:
                            st.error(f"Sync Error: {e}")
                    st.rerun()

    # Main Content
    try:
        emp_path = 'data/employees.csv'
        roles_path = 'data/roles.csv'
        
        # Ensure directories exist
        for d in ["data", "uploads"]:
            if not os.path.exists(d): os.makedirs(d)

        if not os.path.exists(emp_path) or not os.path.exists(roles_path):
            st.warning("System data files missing. Dashboard will be available once Admin uploads CSVs.")
            return

        df = perform_gap_analysis(emp_path, roles_path)
        if df.empty:
            st.error("Unable to process workforce data. Please check CSV formatting.")
            return
            
        recs = get_recommendations(df)

        # Load persistence data with robust defaults
        paths = {
            'progress': 'data/progress.json',
            'feedback': 'data/feedback.json',
            'evidence': 'data/evidence.json',
            'journal': 'data/journal.json',
            'email_logs': 'data/email_logs.json'
        }
        
        data_store = {}
        for key, p in paths.items():
            if not os.path.exists(p):
                with open(p, 'w') as f: json.dump({}, f)
                data_store[key] = {}
            else:
                try:
                    with open(p, 'r') as f: data_store[key] = json.load(f)
                except:
                    data_store[key] = {}

        progress_data = data_store['progress']
        feedback_data = data_store['feedback']
        evidence_data = data_store['evidence']
        journal_data = data_store['journal']
        email_logs = data_store['email_logs']

        st.markdown('<h1 class="bubble-header">📊 PERFORMANCE INSIGHTS</h1>', unsafe_allow_html=True)
        
        # Admin View
        if st.session_state.auth['role'] == "Admin":
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Workforce", len(df))
            col2.metric("Avg Proficiency", f"{df['Weighted_Score'].mean():.2f}")
            col3.metric("Critical Gaps", (df[['Leadership_Gap', 'Technical_Gap', 'Communication_Gap']] > 1).any(axis=1).sum())
            col4.metric("Elite Tier", len(df[df['Performance_Score'] >= 4]) if 'Performance_Score' in df.columns else 0)
            
            st.markdown("<br>", unsafe_allow_html=True)
            tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs(["🔍 ANALYTICS", "🚀 ACTIONABLE IDP", "📦 9-BOX GRID", "📈 TRACKING", "💬 360 FEEDBACK", "🔮 SUCCESSION", "📔 JOURNAL", "🔔 NUDGES", "🏆 LEADERBOARD", "🤖 PREDICTIVE AI", "🌡️ SKILL HEATMAP"])
            
            with tab1:
                st.markdown('<p class="bubble-sub">Workforce Data Explorer</p>', unsafe_allow_html=True)
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.caption("💡 Use the icons in the top-right of the table to export as CSV or enter full-screen mode.")
            
            with tab11:
                st.markdown('<p class="bubble-sub">Organization Skill Heatmap</p>', unsafe_allow_html=True)
                st.write("Visualizing the skill proficiency across different roles.")
                
                # Pivot data for heatmap
                hm_data = df.groupby('Assigned_Role')[['Leadership', 'Technical', 'Communication']].mean()
                
                fig_hm = go.Figure(data=go.Heatmap(
                    z=hm_data.values,
                    x=hm_data.columns,
                    y=hm_data.index,
                    colorscale='Viridis',
                    colorbar=dict(title='Avg Score')
                ))
                fig_hm.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_hm, use_container_width=True)
                st.info("💡 Deep purple indicates critical skill gaps in specific roles, while bright yellow shows high proficiency.")

            with tab2:
                for _, row in df.iterrows():
                    emp_id = str(row['Employee_ID'])
                    emp_name = str(row.get('Name', emp_id))
                    emp_recs = recs.get(row['Employee_ID'], {})
                    with st.expander(f"👤 {emp_name} ({emp_id})"):
                        st.write(f"**Talent Category:** {row['Nine_Box_Category']}")
                        st.write(f"**Development Path:** {row['Nine_Box_Guideline']}")
                        
                        st.markdown("---")
                        c_act, c_ment, c_rot = st.columns(3)
                        with c_act:
                            st.write("**Activities:**")
                            for act in emp_recs.get('activities', []):
                                if isinstance(act, dict):
                                    st.markdown(f"- [{act['name']}]({act['url']})")
                                else:
                                    st.write(f"- {act}")
                        with c_ment:
                            st.write("**Mentorship:**")
                            st.write(f"_{emp_recs.get('mentorship', 'N/A')}_")
                        with c_rot:
                            st.write("**Job Rotation:**")
                            st.write(f"_{emp_recs.get('rotation', 'N/A')}_")
            
            with tab3:
                st.markdown('<p class="bubble-sub">Talent Distribution Matrix</p>', unsafe_allow_html=True)
                categories = [
                    ["Rough Diamond", "Future Star", "Star"],
                    ["Inconsistent Performer", "Core Player", "High Achiever"],
                    ["Risk", "Solid Performer", "Expert Professional"]
                ]
                counts = df['Nine_Box_Category'].value_counts().to_dict()
                for row_cats in categories:
                    cols = st.columns(3)
                    for i, cat in enumerate(row_cats):
                        with cols[i]:
                            st.metric(cat, counts.get(cat, 0))
            
            with tab4:
                st.markdown('<p class="bubble-sub">Workforce Development Tracker</p>', unsafe_allow_html=True)
                track_data = []
                for _, row in df.iterrows():
                    eid = str(row['Employee_ID'])
                    p = progress_data.get(eid, {'completed': [], 'in_progress': []})
                    total_assigned = len(recs.get(row['Employee_ID'], {}).get('activities', []))
                    completed = len(p.get('completed', []))
                    track_data.append({
                        "Employee": row.get('Name', eid),
                        "ID": eid,
                        "Category": row['Nine_Box_Category'],
                        "Progress": f"{completed}/{total_assigned} Modules",
                        "Status": "On Track" if completed > 0 else "Pending Start"
                    })
                st.table(track_data)
                
                st.markdown("---")
                st.write("### 📂 Evidence Review")
                rev_emp = st.selectbox("View Evidence for", options=df['Employee_ID'].tolist(), format_func=lambda x: f"{df[df['Employee_ID']==x]['Name'].iloc[0]} ({x})")
                emp_ev = evidence_data.get(str(rev_emp), {})
                if emp_ev:
                    for act, file_name in emp_ev.items():
                        st.write(f"**Activity:** {act}")
                        file_path = os.path.join("uploads", file_name)
                        if os.path.exists(file_path):
                            with open(file_path, "rb") as f:
                                st.download_button(f"Download Proof for {act}", f, file_name=file_name, key=f"dl_{rev_emp}_{act}")
                        else:
                            st.error(f"File {file_name} not found on server.")
                else:
                    st.write("_No evidence uploaded by this employee yet._")

            with tab5:
                st.markdown('<p class="bubble-sub">Manager Review & 360 Oversight</p>', unsafe_allow_html=True)
                target_emp = st.selectbox("Select Employee to Review", options=df['Employee_ID'].tolist(), format_func=lambda x: f"{df[df['Employee_ID']==x]['Name'].iloc[0]} ({x})")
                
                emp_id_str = str(target_emp)
                emp_feedback = feedback_data.get(emp_id_str, {})
                
                col_view, col_edit = st.columns(2)
                with col_view:
                    st.write("### Employee Self-Assessment")
                    if 'self' in emp_feedback:
                        st.info(f"**Strengths:** {emp_feedback['self'].get('strengths', 'N/A')}")
                        st.warning(f"**Gaps identified by Employee:** {emp_feedback['self'].get('gaps', 'N/A')}")
                    else:
                        st.write("_No self-assessment submitted yet._")
                
                with col_edit:
                    st.write("### Official Manager Feedback")
                    m_text = st.text_area("Final Manager Recommendations", value=emp_feedback.get('manager', ''), height=150)
                    if st.button("Save Official Feedback"):
                        if emp_id_str not in feedback_data: feedback_data[emp_id_str] = {}
                        feedback_data[emp_id_str]['manager'] = m_text
                        with open(feedback_path, 'w') as f: json.dump(feedback_data, f)
                        st.success("Manager feedback recorded!")

            with tab6:
                st.markdown('<p class="bubble-sub">Succession & Promotion Readiness</p>', unsafe_allow_html=True)
                roles_df = pd.read_csv(roles_path)
                target_role_name = st.selectbox("Select Benchmark Role", options=roles_df['Role'].unique())
                role_reqs = roles_df[roles_df['Role'] == target_role_name].iloc[0]
                
                # Calculate Readiness for all employees
                readiness_list = []
                for _, erow in df.iterrows():
                    l_gap = max(0, role_reqs['Leadership'] - erow['Leadership'])
                    t_gap = max(0, role_reqs['Technical'] - erow['Technical'])
                    c_gap = max(0, role_reqs['Communication'] - erow['Communication'])
                    total_req = role_reqs['Leadership'] + role_reqs['Technical'] + role_reqs['Communication']
                    total_gap = l_gap + t_gap + c_gap
                    readiness_score = max(0, (1 - (total_gap / total_req)) * 100)
                    
                    readiness_list.append({
                        "Employee": erow.get('Name', erow['Employee_ID']),
                        "ID": erow['Employee_ID'],
                        "Current Category": erow['Nine_Box_Category'],
                        "Readiness Score": f"{readiness_score:.1f}%",
                        "_score": readiness_score
                    })
                
                readiness_df = pd.DataFrame(readiness_list).sort_values("_score", ascending=False)
                st.write(f"### Ranking for {target_role_name} Position")
                st.dataframe(readiness_df.drop(columns=["_score"]), use_container_width=True, hide_index=True)
                st.info("💡 High readiness scores (>85%) indicate 'Ready-Now' candidates for promotion.")

            with tab7:
                st.markdown('<p class="bubble-sub">Monthly Development Journal</p>', unsafe_allow_html=True)
                j_emp = st.selectbox("Select Employee Journal", options=df['Employee_ID'].tolist(), format_func=lambda x: f"{df[df['Employee_ID']==x]['Name'].iloc[0]} ({x})", key="j_admin")
                eid_s = str(j_emp)
                
                if eid_s not in journal_data: journal_data[eid_s] = []
                
                # Add Entry
                with st.expander("➕ Add New Meeting Note"):
                    col_j1, col_j2 = st.columns(2)
                    with col_j1:
                        j_date = st.date_input("Meeting Date", datetime.now(), key="j_date_admin")
                        j_type = st.selectbox("Category", ["Monthly 1-on-1", "Ad-hoc Feedback", "Career Goal Setting", "Performance Review"], key="j_type_admin")
                    with col_j2:
                        j_tags = st.text_input("Tags (comma separated)", placeholder="leadership, technical", key="j_tags_admin")
                    
                    j_text = st.text_area("Discussion Notes", placeholder="Record key takeaways from the meeting...", height=150, key="j_notes_admin")
                    j_actions = st.text_area("Action Items (One per line)", placeholder="e.g. Finish Python course\nUpdate resume", key="j_actions_admin")
                    
                    if st.button("Commit Entry", key="j_btn_admin", use_container_width=True):
                        if j_text:
                            entry = {
                                "date": j_date.strftime("%Y-%m-%d"),
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "author": "Manager",
                                "type": j_type,
                                "tags": [t.strip() for t in j_tags.split(",")] if j_tags else [],
                                "content": j_text,
                                "actions": [a.strip() for a in j_actions.split("\n") if a.strip()]
                            }
                            journal_data[eid_s].append(entry)
                            with open(journal_path, 'w') as f: json.dump(journal_data, f)
                            st.success("Note added to journal!")
                            st.rerun()
                        else:
                            st.warning("Please enter some notes before saving.")
                
                # Display Timeline
                st.write("### Discussion Timeline")
                if not journal_data[eid_s]:
                    st.write("_No entries found for this employee._")
                else:
                    for entry in reversed(journal_data[eid_s]):
                        with st.container():
                            # Header with Date and Type
                            e_date = entry.get('date', entry.get('date')) # Fallback for old entries
                            e_type = entry.get('type', 'General Note')
                            e_author = entry.get('author', 'Manager')
                            
                            st.markdown(f"#### {e_type} ({e_date})")
                            st.markdown(f"**By:** {e_author}")
                            
                            if entry.get('tags'):
                                st.markdown(" ".join([f"`{t}`" for t in entry['tags']]))
                            
                            st.info(entry['content'])
                            
                            if entry.get('actions'):
                                st.write("**Action Items:**")
                                for action in entry['actions']:
                                    st.markdown(f"- [ ] {action}")
                            
                            st.divider()

            with tab8:
                st.markdown('<p class="bubble-sub">Automated Engagement Nudges</p>', unsafe_allow_html=True)
                st.write("Employees who haven't updated their progress in over **30 days**.")
                
                nudge_list = []
                today = datetime.now()
                for _, row in df.iterrows():
                    eid = str(row['Employee_ID'])
                    p_info = progress_data.get(eid, {})
                    last_upd_str = p_info.get('last_updated')
                    
                    days_inactive = 999 # Default for never updated
                    if last_upd_str:
                        last_upd = datetime.strptime(last_upd_str, "%Y-%m-%d")
                        days_inactive = (today - last_upd).days
                    
                    if days_inactive >= 30:
                        nudge_list.append({
                            "Employee": row.get('Name', eid),
                            "ID": eid,
                            "Last Update": last_upd_str or "Never",
                            "Days Inactive": days_inactive,
                            "Last Nudge": email_logs.get(eid, {}).get('last_nudge', "None")
                        })
                
                if nudge_list:
                    nudge_df = pd.DataFrame(nudge_list).sort_values("Days Inactive", ascending=False)
                    st.dataframe(nudge_df, use_container_width=True, hide_index=True)
                    
                    if st.button("🚀 Send Bulk Nudges to All Inactive", use_container_width=True):
                        sent_count = 0
                        for n in nudge_list:
                            eid = n['ID']
                            email_logs[eid] = {
                                "last_nudge": today.strftime("%Y-%m-%d"),
                                "recipient": n['Employee'],
                                "message": f"Hi {n['Employee']}, it's been {n['Days Inactive']} days since your last IDP update. Please check your dashboard!"
                            }
                            sent_count += 1
                        with open(email_logs_path, 'w') as f: json.dump(email_logs, f)
                        st.success(f"Successfully simulated sending {sent_count} nudge emails!")
                        st.rerun()
                else:
                    st.success("🎉 All employees are active! No nudges required.")
                
                st.divider()
                st.write("### 📬 Recently Sent Nudges")
                if email_logs:
                    for eid, log in reversed(list(email_logs.items())):
                        with st.expander(f"To: {log['recipient']} ({eid}) - {log['last_nudge']}"):
                            st.code(log['message'])
                else:
                    st.write("_No nudges sent yet._")

            with tab9:
                st.markdown('<p class="bubble-sub">Gamification & Achievement Leaderboard</p>', unsafe_allow_html=True)
                leaderboard_data = []
                for _, row in df.iterrows():
                    eid = str(row['Employee_ID'])
                    p_info = progress_data.get(eid, {'completed': []})
                    comp_count = len(p_info.get('completed', []))
                    
                    level = 1 + (comp_count // 2)
                    
                    # Calculate badges for leaderboard
                    user_badges = []
                    badge_defs = {
                        "Leadership Vanguard": "👑",
                        "Technical Architect": "💻",
                        "Elite Communicator": "🗣️",
                        "Strategic Star": "⭐",
                        "Fast Learner": "⚡"
                    }
                    # ... simple badge logic for summary ...
                    b_count = 0
                    if comp_count >= 2: b_count += 1 # Fast Learner
                    # Check keywords
                    for b_name, b_icon in badge_defs.items():
                        if any(b_name.split()[0].lower() in act.lower() for act in p_info.get('completed', [])):
                            b_count += 1
                    
                    leaderboard_data.append({
                        "Employee": row.get('Name', eid),
                        "ID": eid,
                        "Level": level,
                        "Completed": comp_count,
                        "Badges": b_count
                    })
                
                lb_df = pd.DataFrame(leaderboard_data).sort_values(["Level", "Completed"], ascending=False)
                st.dataframe(lb_df, use_container_width=True, hide_index=True)
                st.info("💡 Levels increase every 2 completed activities. Badges are awarded for mastering specific skill clusters.")

            with tab10:
                st.markdown('<p class="bubble-sub">AI Predictive Modeling</p>', unsafe_allow_html=True)
                st.write("Leveraging engagement and performance data to predict future workforce trends.")
                
                try:
                    pred_df = generate_predictions(df, progress_data)
                    
                    c_ai1, c_ai2 = st.columns(2)
                    with c_ai1:
                        high_risk_count = len(pred_df[pred_df['Flight Risk'] == "🔴 High Risk"])
                        st.metric("🚨 High Attrition Risk", high_risk_count)
                    with c_ai2:
                        star_count = len(pred_df[pred_df['_star_val'] >= 80])
                        st.metric("⭐ High Future Star Probability (>80%)", star_count)
                    
                    st.write("### Predictive Assessment Matrix")
                    st.dataframe(pred_df.drop(columns=["_risk_val", "_star_val"]), use_container_width=True, hide_index=True)
                    
                    st.info("💡 **Flight Risk** is calculated using engagement metrics (days since last IDP update) crossed with performance and tenure. **Future Star Probability** considers current placement and learning momentum.")
                except Exception as e:
                    st.error(f"Error generating predictions: {e}")


        # Employee View
        else:
            df_ids = df['Employee_ID'].astype(str).str.lower()
            auth_id = str(st.session_state.auth['user_id']).lower()
            emp_data = df[df_ids == auth_id]
            
            if not emp_data.empty:
                row = emp_data.iloc[0]
                emp_id_orig = row['Employee_ID']
                emp_id_str = str(emp_id_orig)
                emp_recs = recs.get(emp_id_orig, {})
                
                st.markdown(f'<h2 style="font-weight: 800;">Welcome, <span style="color: #4776E6;">{row.get("Name", "User")}</span></h2>', unsafe_allow_html=True)
                
                # --- GAMIFICATION LOGIC ---
                user_p = progress_data.get(emp_id_str, {'completed': [], 'in_progress': []})
                completed_acts = user_p.get('completed', [])
                num_completed = len(completed_acts)
                
                # Define Levels
                level = 1 + (num_completed // 2) # Level up every 2 activities
                xp = (num_completed % 2) * 50
                if num_completed > 0 and num_completed % 2 == 0: xp = 100
                
                # Define Badges based on keywords
                badges = []
                badge_defs = {
                    "Leadership Vanguard": {"icon": "👑", "keyword": "Leadership"},
                    "Technical Architect": {"icon": "💻", "keyword": "Technical"},
                    "Elite Communicator": {"icon": "🗣️", "keyword": "Communication"},
                    "Strategic Star": {"icon": "⭐", "keyword": "Strategic"},
                    "Fast Learner": {"icon": "⚡", "count": 2}
                }
                
                for b_name, b_info in badge_defs.items():
                    if "keyword" in b_info:
                        if any(b_info['keyword'].lower() in act.lower() for act in completed_acts):
                            badges.append(f"{b_info['icon']} {b_name}")
                    elif "count" in b_info:
                        if num_completed >= b_info['count']:
                            badges.append(f"{b_info['icon']} {b_name}")

                c_gam1, c_gam2 = st.columns([2, 3])
                with c_gam1:
                    st.markdown(f"""
                        <div style="background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1);">
                            <h3 style="margin: 0; color: #8E54E9;">Level {level}</h3>
                            <p style="font-size: 0.9rem; color: #aaa;">{num_completed} Activities Mastered</p>
                            <div style="background: rgba(255, 255, 255, 0.1); height: 10px; border-radius: 5px; margin-top: 10px;">
                                <div style="background: linear-gradient(90deg, #4776E6, #8E54E9); width: {xp if num_completed % 2 != 0 else (100 if num_completed > 0 else 0)}%; height: 100%; border-radius: 5px;"></div>
                            </div>
                            <p style="font-size: 0.8rem; margin-top: 5px; text-align: right;">{xp if num_completed % 2 != 0 else (100 if num_completed > 0 else 0)}% to Level {level + 1}</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                with c_gam2:
                    st.write("### Your Badges")
                    if badges:
                        b_cols = st.columns(len(badges) if len(badges) < 4 else 4)
                        for i, badge in enumerate(badges):
                            with b_cols[i % 4]:
                                st.markdown(f"""
                                    <div style="text-align: center; background: rgba(71, 118, 230, 0.1); padding: 10px; border-radius: 15px; border: 1px solid rgba(71, 118, 230, 0.2); margin-bottom: 10px;">
                                        <div style="font-size: 1.5rem;">{badge.split()[0]}</div>
                                        <div style="font-size: 0.7rem; font-weight: 700; color: #4776E6;">{' '.join(badge.split()[1:])}</div>
                                    </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.write("_Complete activities to earn badges!_")

                st.markdown("<br>", unsafe_allow_html=True)
                
                c1, c2, c3 = st.columns(3)
                c1.metric("Your Proficiency", f"{row['Weighted_Score']:.2f}")
                c2.metric("Performance", row['Performance_Score'])
                c3.metric("Talent Tier", row['Nine_Box_Category'])
                
                tab_viz, tab_path, tab_dev, tab_track, tab_360, tab_journal, tab_coach = st.tabs(["📊 SKILL RADAR", "🔮 CAREER PATHING", "🚀 MY DEVELOPMENT PLAN", "📈 PROGRESS TRACKER", "💬 360 FEEDBACK", "📔 JOURNAL", "🤖 AI CAREER COACH"])
                
                with tab_coach:
                    st.markdown('<p class="bubble-sub">24/7 AI Growth Partner</p>', unsafe_allow_html=True)
                    st.write("Ask our AI anything about your career growth, skill gaps, or development plan.")
                    
                    if "messages" not in st.session_state:
                        st.session_state.messages = [{"role": "assistant", "content": f"Hello {row.get('Name', 'User')}! I've analyzed your {row['Nine_Box_Category']} profile. How can I help you bridge your gaps today?"}]

                    for msg in st.session_state.messages:
                        with st.chat_message(msg["role"]):
                            st.write(msg["content"])

                    if prompt := st.chat_input("Ask about your career..."):
                        st.session_state.messages.append({"role": "user", "content": prompt})
                        with st.chat_message("user"):
                            st.write(prompt)
                        
                        # Simple Mock Response Logic
                        response = ""
                        if "leadership" in prompt.lower():
                            response = "To improve your Leadership score, I recommend focusing on the 'High-Stakes Decision Making' module and seeking a mentorship pairing with a senior director."
                        elif "technical" in prompt.lower():
                            response = "Your technical gap is 2.0. You should prioritize the 'Advanced Technical Certification' and perhaps shadow a senior engineer in the R&D lab."
                        elif "promotion" in prompt.lower() or "next step" in prompt.lower():
                            response = f"Based on your current readiness for {row['Assigned_Role']}, you are {row['Performance_Score']} out of 5 in performance. Focus on closing your communication gaps to become 'Ready-Now'."
                        else:
                            response = "That's a great goal! I suggest reviewing your 'My Development Plan' tab to see the specific activities I've curated for your growth dna."
                        
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        with st.chat_message("assistant"):
                            st.write(response)

                with tab_viz:
                    st.markdown('<p class="bubble-sub">DNA Proficiency Visualization</p>', unsafe_allow_html=True)
                    
                    categories = ['Leadership', 'Technical', 'Communication']
                    current_scores = [row['Leadership'], row['Technical'], row['Communication']]
                    target_scores = [row.get('Leadership_Req', 0), row.get('Technical_Req', 0), row.get('Communication_Req', 0)]
                    
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatterpolar(
                        r=current_scores + [current_scores[0]],
                        theta=categories + [categories[0]],
                        fill='toself',
                        name='Current Skill Level',
                        line_color='#4776E6'
                    ))
                    
                    fig.add_trace(go.Scatterpolar(
                        r=target_scores + [target_scores[0]],
                        theta=categories + [categories[0]],
                        fill='toself',
                        name='Target Role Requirement',
                        line_color='#8E54E9',
                        opacity=0.5
                    ))
                    
                    fig.update_layout(
                        polar=dict(
                            radialaxis=dict(visible=True, range=[0, 5], gridcolor='rgba(255, 255, 255, 0.1)'),
                            angularaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
                            bgcolor='rgba(0,0,0,0)'
                        ),
                        showlegend=True,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white', size=12),
                        margin=dict(t=40, b=40, l=40, r=40)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    st.info("💡 The **blue** area represents your current skills, while the **purple** area shows the target requirements for your assigned role.")

                with tab_path:
                    st.markdown('<p class="bubble-sub">Future Role Simulator</p>', unsafe_allow_html=True)
                    roles_df = pd.read_csv(roles_path)
                    future_role = st.selectbox("Select a Future Target Role", options=roles_df['Role'].unique())
                    f_reqs = roles_df[roles_df['Role'] == future_role].iloc[0]
                    
                    # Readiness Calculation
                    l_gap = max(0, f_reqs['Leadership'] - row['Leadership'])
                    t_gap = max(0, f_reqs['Technical'] - row['Technical'])
                    c_gap = max(0, f_reqs['Communication'] - row['Communication'])
                    total_req = f_reqs['Leadership'] + f_reqs['Technical'] + f_reqs['Communication']
                    total_gap = l_gap + t_gap + c_gap
                    readiness = max(0, (1 - (total_gap / total_req)) * 100)
                    
                    st.metric("Readiness for " + future_role, f"{readiness:.1f}%")
                    
                    # Radar Overlay for Future Role
                    categories = ['Leadership', 'Technical', 'Communication']
                    c_scores = [row['Leadership'], row['Technical'], row['Communication']]
                    f_scores = [f_reqs['Leadership'], f_reqs['Technical'], f_reqs['Communication']]
                    
                    fig_f = go.Figure()
                    fig_f.add_trace(go.Scatterpolar(r=c_scores + [c_scores[0]], theta=categories + [categories[0]], fill='toself', name='Current Skills', line_color='#4776E6'))
                    fig_f.add_trace(go.Scatterpolar(r=f_scores + [f_scores[0]], theta=categories + [categories[0]], fill='toself', name=f'Future {future_role} Requirements', line_color='#FF4B4B', opacity=0.4))
                    fig_f.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
                    st.plotly_chart(fig_f, use_container_width=True)
                    
                    if readiness > 90: st.success("🚀 You are highly ready for this role!")
                    elif readiness > 70: st.info("📈 You are on the right track. Focus on the red areas to bridge the gap.")
                    else: st.warning("🚩 Significant development needed in specific areas to reach this role.")

                with tab_dev:
                    st.markdown('<p class="bubble-sub">Growth & Development Pathway</p>', unsafe_allow_html=True)
                    st.info(f"**{row['Nine_Box_Category']}**: {row['Nine_Box_Guideline']}")
                    
                    st.write("### Personalized Activities")
                    a1, a2, a3 = st.columns(3)
                    with a1:
                        st.success("**Training Modules**")
                        for act in emp_recs.get('activities', []):
                            if isinstance(act, dict):
                                st.markdown(f"✅ [{act['name']}]({act['url']})")
                            else:
                                st.write(f"✅ {act}")
                    with a2:
                        st.info("**Mentorship Pairing**")
                        st.write(emp_recs.get('mentorship', 'N/A'))
                    with a3:
                        st.warning("**Job Rotation**")
                        st.write(emp_recs.get('rotation', 'N/A'))

                    st.divider()
                    st.markdown('<p class="bubble-sub">Proficiency Breakdown</p>', unsafe_allow_html=True)
                    s1, s2, s3 = st.columns(3)
                    skills = [
                        ("Leadership", row['Leadership'], row.get('Leadership_Req', 0)),
                        ("Technical", row['Technical'], row.get('Technical_Req', 0)),
                        ("Communication", row['Communication'], row.get('Communication_Req', 0))
                    ]
                    for i, (name, score, req) in enumerate(skills):
                        with [s1, s2, s3][i]:
                            prof = "Expert" if score >= 4.5 else "Advanced" if score >= 3.5 else "Intermediate" if score >= 2.5 else "Novice"
                            st.metric(name, f"{score}/5")
                            st.write(f"Level: **{prof}**")
                            if score < req:
                                st.warning(f"Gap (Target: {req})")
                            else:
                                st.success(f"On Target")

                with tab_track:
                    st.markdown('<p class="bubble-sub">IDP Progress Tracker</p>', unsafe_allow_html=True)
                    if emp_id_str not in progress_data: progress_data[emp_id_str] = {'completed': [], 'in_progress': []}
                    user_p = progress_data[emp_id_str]
                    all_acts = emp_recs.get('activities', [])
                    
                    st.write("Update your activity status:")
                    changed = False
                    for act in all_acts:
                        act_name = act['name'] if isinstance(act, dict) else act
                        col_stat, col_file = st.columns([2, 3])
                        with col_stat:
                            status = "Not Started"
                            if act_name in user_p['completed']: status = "Completed"
                            elif act_name in user_p['in_progress']: status = "In Progress"
                            
                            new_status = st.selectbox(f"Status for {act_name}", ["Not Started", "In Progress", "Completed"], index=["Not Started", "In Progress", "Completed"].index(status), key=f"status_{act_name}")
                            if new_status != status:
                                changed = True
                                if act_name in user_p['completed']: user_p['completed'].remove(act_name)
                                if act_name in user_p['in_progress']: user_p['in_progress'].remove(act_name)
                                if new_status == "Completed": user_p['completed'].append(act_name)
                                elif new_status == "In Progress": user_p['in_progress'].append(act_name)
                        
                        with col_file:
                            uploaded_file = st.file_uploader(f"Upload Evidence for {act_name}", type=["pdf", "png", "jpg", "jpeg"], key=f"file_{act_name}")
                            if uploaded_file:
                                file_name = f"{emp_id_str}_{act_name.replace(' ', '_')}_{uploaded_file.name}"
                                with open(os.path.join("uploads", file_name), "wb") as f:
                                    f.write(uploaded_file.getbuffer())
                                if emp_id_str not in evidence_data: evidence_data[emp_id_str] = {}
                                evidence_data[emp_id_str][act_name] = file_name
                                with open(evidence_path, 'w') as f: json.dump(evidence_data, f)
                                st.success(f"Proof for {act_name} uploaded!")
                    
                    if changed:
                        progress_data[emp_id_str]['last_updated'] = datetime.now().strftime("%Y-%m-%d")
                        with open(progress_path, 'w') as f: json.dump(progress_data, f)
                        st.success("Progress updated successfully!")
                        st.rerun()

                    st.markdown("---")
                    done_count = len(user_p['completed'])
                    total_count = len(all_acts)
                    st.progress((done_count / total_count) if total_count > 0 else 0)
                    st.write(f"Overall Completion: **{done_count}/{total_count} Modules**")

                with tab_360:
                    st.markdown('<p class="bubble-sub">Personalized 360 Feedback Portal</p>', unsafe_allow_html=True)
                    if emp_id_str not in feedback_data: feedback_data[emp_id_str] = {}
                    user_f = feedback_data[emp_id_str]

                    col_self, col_mgr = st.columns(2)
                    with col_self:
                        st.write("### My Self-Assessment")
                        s_str = st.text_area("What are your key strengths?", value=user_f.get('self', {}).get('strengths', ''), key="self_str")
                        s_gap = st.text_area("Where do you see skill gaps?", value=user_f.get('self', {}).get('gaps', ''), key="self_gap")
                        if st.button("Submit Self-Assessment"):
                            feedback_data[emp_id_str]['self'] = {'strengths': s_str, 'gaps': s_gap}
                            with open(feedback_path, 'w') as f: json.dump(feedback_data, f)
                            st.success("Self-assessment saved!")

                    with col_mgr:
                        st.write("### Manager Feedback")
                        if 'manager' in user_f:
                            st.success(f"**From Management:** {user_f['manager']}")
                        else:
                            st.info("Manager feedback is pending. Continue focusing on your IDP activities.")

                with tab_journal:
                    st.markdown('<p class="bubble-sub">My Development Reflection Journal</p>', unsafe_allow_html=True)
                    if emp_id_str not in journal_data: journal_data[emp_id_str] = []
                    
                    # Add Entry
                    with st.expander("➕ Log Today's Reflection"):
                        col_e1, col_e2 = st.columns(2)
                        with col_e1:
                            e_date = st.date_input("Reflection Date", datetime.now(), key="e_date_emp")
                            e_type = st.selectbox("Type", ["Self-Reflection", "Learning Note", "Goal Milestone", "Check-in Preparation"], key="e_type_emp")
                        with col_e2:
                            e_tags = st.text_input("Tags (comma separated)", placeholder="productivity, skill-up", key="e_tags_emp")
                        
                        e_text = st.text_area("What did you learn or discuss today?", height=150, key="e_notes_emp")
                        
                        if st.button("Save Reflection", key="j_btn_emp", use_container_width=True):
                            if e_text:
                                entry = {
                                    "date": e_date.strftime("%Y-%m-%d"),
                                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    "author": row.get("Name", "Employee"),
                                    "type": e_type,
                                    "tags": [t.strip() for t in e_tags.split(",")] if e_tags else [],
                                    "content": e_text
                                }
                                journal_data[emp_id_str].append(entry)
                                with open(journal_path, 'w') as f: json.dump(journal_data, f)
                                st.success("Reflection saved!")
                                st.rerun()
                            else:
                                st.warning("Please enter your reflection before saving.")
                    
                    # Display History
                    st.write("### Discussion History")
                    if not journal_data[emp_id_str]:
                        st.write("_No journal entries yet. Start by logging your first reflection!_")
                    else:
                        for entry in reversed(journal_data[emp_id_str]):
                            with st.container():
                                date_str = entry.get('date', entry.get('date'))
                                type_str = entry.get('type', 'Reflection')
                                author_str = entry.get('author', 'User')
                                
                                st.markdown(f"#### {type_str} ({date_str})")
                                st.markdown(f"**By:** {author_str}")
                                
                                if entry.get('tags'):
                                    st.markdown(" ".join([f"`{t}`" for t in entry['tags']]))
                                
                                if author_str == "Manager":
                                    st.success(entry['content'])
                                    if entry.get('actions'):
                                        st.write("**Manager's Action Items:**")
                                        for action in entry['actions']:
                                            st.markdown(f"- [ ] {action}")
                                else:
                                    st.info(entry['content'])
                                
                                st.divider()

    except Exception as e:
        st.error(f"Data processing error: {e}")

# --- MAIN ROUTER ---
if st.session_state.auth['logged_in']:
    show_dashboard()
elif st.session_state.page == 'login':
    show_login()
else:
    show_landing()
