"""
Cricket SQL Analytics Page - Interactive Queries (Postgres)
Execute 25+ SQL queries with progressive difficulty levels
"""

import streamlit as st
import pandas as pd
import psycopg2

# ---------- DB CONFIG ----------
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "Cricbuz",
    "user": "postgres",
    "password": "susmitha2102"
}

# ---------- Helper Functions ----------
def run_query(query):
    """Execute query and return dataframe"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Database Error: {e}")
        return pd.DataFrame()

def display_query_stats(df):
    """Basic stats about query results"""
    st.markdown("#### 📈 Result Statistics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Rows", len(df))
    with col2:
        st.metric("Columns", len(df.columns))
    with col3:
        st.metric("Numeric Columns", len(df.select_dtypes(include='number').columns))
    with col4:
        st.metric("Text Columns", len(df.select_dtypes(include='object').columns))

def get_difficulty_badge(title):
    """Tag difficulty level based on question number"""
    q_num = int(title.split('.')[0][1:])
    if q_num <= 8:
        return "🟢 Beginner"
    elif q_num <= 16:
        return "🟡 Intermediate"
    else:
        return "🔴 Advanced"

# ---------- All Queries ----------
QUERIES = {
   "Q1. Players from India": """
    SELECT full_name, role, batting_style, bowling_style 
    FROM players 
    JOIN teams ON players.team_id = teams.team_id 
    WHERE teams.country = 'India';
    """,

    "Q2. Matches played in last few days": """
    SELECT match_desc, team1_name, team2_name, venue_name, venue_city, start_date 
    FROM matches 
    WHERE start_date >= CURRENT_DATE - INTERVAL '7 days' 
    ORDER BY start_date DESC;
    """,

    "Q3. Top 10 run scorers in ODI": """
    SELECT player_name, runs, batting_average, hundreds 
    FROM player_master_stats 
    WHERE format = 'ODI' 
    ORDER BY runs DESC 
    LIMIT 10;
    """,

    "Q4. Venues with capacity > 30000": """
    SELECT ground, city, country, capacity 
    FROM venues 
    WHERE capacity > 30000 
    ORDER BY capacity DESC;
    """,

    "Q5. Matches won by each team": """
    SELECT winner_team_name, COUNT(*) AS total_wins 
    FROM matches 
    WHERE winner_team_name != 'No Result' 
    GROUP BY winner_team_name 
    ORDER BY total_wins DESC;
    """,

    "Q6. Count players by role": """
    SELECT role, COUNT(*) AS total_players 
    FROM players 
    GROUP BY role;
    """,

    "Q7. Highest individual score by format": """
    SELECT format, MAX(highest_score) AS highest_score 
    FROM player_master_stats 
    GROUP BY format;
    """,

    "Q8. Series started in 2024": """
    SELECT series_name, host_country, series_type, start_date, total_matches 
    FROM series 
    WHERE EXTRACT(YEAR FROM start_date) = 2024;
    """,

    "Q9. All-rounders with 1000 runs and 50 wickets": """
    SELECT player_name,format,runs,wickets
    FROM player_master_stats
    WHERE runs>1000 AND wickets>50
    ORDER BY runs DESC,wickets DESC;
    """,

    "Q10. Last 20 completed matches": """
    SELECT start_date,match_desc, team1_name, team2_name,status,winner_team_name,
           win_by_runs, win_by_wickets, venue_name  
    FROM matches 
    WHERE LOWER(state) = 'complete' 
    ORDER BY start_date DESC 
    LIMIT 20;
    """,

    "Q11. Compare player runs across formats": """
    SELECT player_name, 
           SUM(CASE WHEN format='Test' THEN runs ELSE 0 END) AS test_runs, 
           SUM(CASE WHEN format='ODI' THEN runs ELSE 0 END) AS odi_runs, 
           SUM(CASE WHEN format='T20I' THEN runs ELSE 0 END) AS t20_runs, 
           ROUND(AVG(batting_average),2) AS overall_avg
    FROM player_master_stats
    GROUP BY player_name
    HAVING COUNT(DISTINCT format)>=2;
    """,

    "Q12. Team wins home vs away": """
    SELECT t.team_name, 
           SUM(CASE WHEN m.venue_country = t.country AND m.winner_team_id = t.team_id THEN 1 ELSE 0 END) AS home_wins, 
           SUM(CASE WHEN m.venue_country <> t.country AND m.winner_team_id = t.team_id THEN 1 ELSE 0 END) AS away_wins 
    FROM teams t 
    JOIN matches m ON t.team_id IN (m.team1_id, m.team2_id) 
    GROUP BY t.team_name;
    """,

    "Q13. Partnerships above 100 runs": """
    SELECT batsman1, batsman2, runs, innings_number 
    FROM partnerships 
    WHERE runs >= 100;
    """,

    "Q14. Bowling performance at venues": """
    SELECT b.player_name,
           m.venue_name,
           ROUND(AVG(b.economy_rate)::numeric,2) AS avg_economy,
           SUM(b.wickets) AS total_wickets,
           COUNT(DISTINCT b.match_id) AS matches_played
    FROM bowling_scorecard b
    JOIN matches m ON b.match_id = m.match_id
    WHERE b.overs >= 4
    GROUP BY b.player_name, m.venue_name
    HAVING COUNT(DISTINCT b.match_id) >= 3
    ORDER BY avg_economy ASC, total_wickets DESC;
    """,

    "Q15. Player performance in close matches": """
    SELECT b.player_name,
           t.country,
           ROUND(AVG(b.runs)::numeric,0) AS avg_runs,
           COUNT(DISTINCT b.match_id) AS close_matches
    FROM batting_scorecard b
    JOIN matches m ON b.match_id = m.match_id
    JOIN players p ON b.player_name = p.full_name
    JOIN teams t ON p.team_id = t.team_id
    WHERE (m.win_by_runs < 50 OR m.win_by_wickets < 5)
      AND m.winner_team_name != 'No Result'
    GROUP BY b.player_name,t.country
    ORDER BY avg_runs DESC;
    """,

    "Q16. Yearly batting since 2020": """
    SELECT b.player_name,
           b.team_name,
           EXTRACT(YEAR FROM m.start_date) AS year,
           ROUND(AVG(b.runs)::NUMERIC,0) AS avg_runs,
           ROUND(AVG(b.strike_rate)::NUMERIC,2) AS avg_sr,
           COUNT(b.match_id) AS matches_played
    FROM batting_scorecard b
    JOIN matches m ON b.match_id=m.match_id
    WHERE EXTRACT(YEAR FROM m.start_date)>=2020
    GROUP BY b.player_name,b.team_name,EXTRACT(YEAR FROM m.start_date)
    HAVING COUNT(b.match_id)>=1  
    ORDER BY year DESC,avg_runs DESC;
    """,

    "Q17. Toss advantage": """
    SELECT toss_decision,
           COUNT(*) AS matches,
           ROUND(AVG(CASE WHEN winner_team_id=toss_winner_id THEN 1 ELSE 0 END)*100,2) AS win_percent
    FROM matches
    WHERE LOWER(state)='complete' AND toss_winner_id IS NOT NULL
    GROUP BY toss_decision;
    """,

    "Q18. Most economical bowlers (ODI,T20)": """
    SELECT b.player_name,
           b.team_name,
           ROUND(AVG(b.economy_rate)::NUMERIC,2) AS avg_economy,
           SUM(b.wickets) AS total_wickets,
           COUNT(DISTINCT b.match_id) AS matches_bowled
    FROM bowling_scorecard b
    JOIN matches m ON b.match_id=m.match_id
    WHERE m.match_format IN('ODI','T20I')
      AND b.overs>=2
    GROUP BY b.player_name,b.team_name
    HAVING COUNT(DISTINCT b.match_id)>=1   
    ORDER BY avg_economy ASC,total_wickets DESC;
    """,

    "Q19. Consistent batsmen since 2022": """
    SELECT b.player_name,
           b.team_name,
           ROUND(AVG(b.runs)::NUMERIC,0) AS avg_runs,
           ROUND(STDDEV_POP(b.runs)::NUMERIC,2) AS run_stddev,
           COUNT(*) AS innings
    FROM batting_scorecard b
    JOIN matches m ON b.match_id=m.match_id
    WHERE m.start_date>='2022-01-01'
      AND b.balls_faced>=10
    GROUP BY b.player_name,b.team_name
    HAVING COUNT(*)>=1
    ORDER BY run_stddev ASC,avg_runs DESC;
    """,

    "Q20. Matches and averages per format": """
    SELECT player_name,
           SUM(CASE WHEN format='Test' THEN matches ELSE 0 END) AS test_matches,
           SUM(CASE WHEN format='ODI' THEN matches ELSE 0 END) AS odi_matches,
           SUM(CASE WHEN format='T20I' THEN matches ELSE 0 END) AS t20_matches,
           ROUND(SUM(runs)::NUMERIC/NULLIF(SUM(innings),0),2) AS overall_bat_avg
    FROM player_master_stats
    GROUP BY player_name
    HAVING SUM(matches)>=20;
    """,

    "Q21. Player ranking score": """
    SELECT player_name,
           format,
           ROUND(
               SUM(runs)*0.01 
             + AVG(batting_average)*0.5 
             + AVG(strike_rate)*0.3
             + SUM(wickets)*2 
             + (50-AVG(bowling_average))*0.5 
             + (6-AVG(economy_rate))*2
           , 2) AS total_points
    FROM player_master_stats
    GROUP BY player_name, format
    ORDER BY format DESC;
    """,

    "Q22. Head-to-head team stats (last 3 yrs)": """
    SELECT m.team1_name,
           m.team2_name,
           COUNT(*) AS total_matches,
           SUM(CASE WHEN m.winner_team_name=m.team1_name THEN 1 ELSE 0 END) AS team1_wins,
           SUM(CASE WHEN m.winner_team_name=m.team2_name THEN 1 ELSE 0 END) AS team2_wins
    FROM matches m
    WHERE m.start_date>=CURRENT_DATE-INTERVAL '3 years'
      AND m.winner_team_name!='No Result'
    GROUP BY m.team1_name,m.team2_name
    HAVING COUNT(*)>=1
    ORDER BY total_matches DESC;
    """,

    "Q23. Recent form (last 10 innings)": """
    SELECT b.player_name,b.team_name,
           ROUND(AVG(b.runs)::NUMERIC,0) AS avg_runs,
           ROUND(AVG(b.strike_rate)::NUMERIC,2) AS avg_sr,
           SUM(CASE WHEN b.runs>=50 THEN 1 ELSE 0 END) AS fifties
    FROM batting_scorecard b
    JOIN matches m ON b.match_id=m.match_id
    GROUP BY b.player_name,b.team_name
    ORDER BY avg_runs DESC
    LIMIT 50;
    """,

    "Q24. Successful partnerships": """
    SELECT batsman1,
           batsman2,
           ROUND(AVG(runs)::NUMERIC,0) AS avg_runs,
           COUNT(*) AS total_partnerships,
           MAX(runs) AS highest
    FROM partnerships
    GROUP BY batsman1,batsman2
    HAVING COUNT(*)>=1
    ORDER BY avg_runs DESC;
    """,

    "Q25. Time series performance by quarter": """
    SELECT b.player_name,b.team_name,
           DATE_TRUNC('quarter',m.start_date) AS quarter,
           ROUND(AVG(b.runs)::NUMERIC,0) AS avg_runs,
           ROUND(AVG(b.strike_rate)::NUMERIC,2) AS avg_sr,
           COUNT(*) AS matches
    FROM batting_scorecard b
    JOIN matches m ON b.match_id=m.match_id
    GROUP BY b.player_name,b.team_name,DATE_TRUNC('quarter',m.start_date)
    HAVING COUNT(*)>=3
    ORDER BY b.player_name,quarter;
    """
}

# ---------- Theme CSS ----------
st.markdown("""
    <style>
    body {
        font-family: 'Poppins', sans-serif;
        background: #f9f9f9;
        color: #111;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #a18cd1, #fbc2eb);
        color: white !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
        font-size: 17px !important;
        font-weight: 600 !important;
    }
    .hero {
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #a18cd1, #fbc2eb);
        color: white;
        border-radius: 12px;
        margin: 0 auto 25px auto;
        max-width: 95%;
        box-shadow: 0px 6px 18px rgba(0,0,0,0.15);
    }
    .hero h1 { font-size: 36px; font-weight: 700; margin-bottom: 8px; }
    .hero p { font-size: 18px; margin: 0; }
    .query-box {
        background: #fff;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 6px 18px rgba(241, 112, 155, 0.25);
        margin-bottom: 20px;
    }
    div.stButton > button {
        background: linear-gradient(90deg, #a18cd1, #fbc2eb);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 8px 14px;
        transition: 0.3s;
        border: none;
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        background: linear-gradient(90deg, #ff9a9e, #fad0c4);
        color: #111;
    }
    .about-box {
        background: linear-gradient(135deg, #fbc2eb, #a6c1ee);
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
        margin-top: 20px;
        font-size: 15px;
        line-height: 1.6;
        color: #fff;
    }
    .about-box h3 {
        text-align: center;
        color: #fff;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Streamlit Page ----------
st.set_page_config(page_title="🏏 Cricket SQL Analytics", layout="wide")

st.markdown("""
<div class="hero">
    <h1>🏏 Cricket SQL Analytics</h1>
    <p>Practice 25+ cricket-themed SQL queries across Beginner, Intermediate, and Advanced levels</p>
</div>
""", unsafe_allow_html=True)

# Query selector
query_titles = list(QUERIES.keys())
selected_query_title = st.selectbox("Choose a question:", query_titles)

if selected_query_title:
    st.subheader(selected_query_title)
    st.markdown(f"**Difficulty Level:** {get_difficulty_badge(selected_query_title)}")

    sql_query = QUERIES[selected_query_title]

    # Frozen SQL Editor (Read-only)
    st.markdown("#### 📝 SQL Query")
    st.code(sql_query, language="sql")

    if st.button("▶️ Execute Query"):
        with st.spinner("Running query..."):
            df = run_query(sql_query)

            if not df.empty:
                st.success(f"✅ Query executed successfully! Found {len(df)} rows.")
                st.dataframe(df, use_container_width=True)

                # Stats only (CSV removed)
                display_query_stats(df)
            else:
                st.warning("⚠️ Query executed but returned no results.")

# ✅ Sidebar About Section
st.sidebar.title("ℹ️ About")
st.sidebar.markdown("""
<div class="about-box">
    ✨ <b>About SQL Analytics</b><br><br>
    🚀 Explore 25 curated SQL queries<br><br>
    🟢 Beginner<br>
    🟡 Intermediate<br>
    🔴 Advanced<br><br>
    📊 Covers players, matches, venues, stats
</div>
""", unsafe_allow_html=True)


