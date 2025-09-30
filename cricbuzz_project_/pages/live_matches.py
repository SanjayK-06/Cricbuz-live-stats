import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# 🔑 API Key
CRICBUZZ_API_KEY = "d723372ef9mshf19bc74dba24b9fp17cbc7jsn6ff8a547531f"
CRICBUZZ_HOST = "cricbuzz-cricket.p.rapidapi.com"

# ---------------- Theme CSS ----------------
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
        font-size: 18px !important;
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
    .match-card {
        background: #fff;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 6px 18px rgba(241, 112, 155, 0.25);
        margin-bottom: 18px;
        transition: all 0.3s ease-in-out;
    }
    .match-card:hover {
        transform: translateY(-6px);
        box-shadow: 0px 12px 28px rgba(161, 140, 209, 0.35);
    }
    .match-card h3 { color: #6a11cb; font-size: 22px; margin-bottom: 8px; }
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
    .chat-box {
        background: #fce4ec;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 6px solid #a18cd1;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- API Class ----------------
class CricbuzzAPI:
    def __init__(self):
        self.headers = {
            "x-rapidapi-key": CRICBUZZ_API_KEY,
            "x-rapidapi-host": CRICBUZZ_HOST,
        }
        self.base_url = "https://cricbuzz-cricket.p.rapidapi.com"

    def get_live_matches(self):
        try:
            url = f"{self.base_url}/matches/v1/live"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"⚠ Error fetching live matches: {e}")
            return {}

    def get_scorecard(self, match_id: str):
        try:
            url = f"{self.base_url}/mcenter/v1/{match_id}/scard"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"⚠ Error fetching scorecard: {e}")
            return {}

# ---------------- Helpers ----------------
def format_time(epoch_ms):
    try:
        if epoch_ms:
            return datetime.fromtimestamp(int(epoch_ms) / 1000).strftime("%d %b %Y, %I:%M %p")
        return "N/A"
    except:
        return "N/A"

def show_innings_scorecard(api: CricbuzzAPI, match_id: str):
    data = api.get_scorecard(match_id)
    if not data or "scorecard" not in data:
        st.warning("⚠ No scorecard data available.")
        return

    for i, innings in enumerate(data.get("scorecard", []), start=1):
        team_name = innings.get("batteamname", "Unknown")
        st.subheader(f"📊 Inning {i} - {team_name}")

        # 🏏 Batting
        batsmen_df = pd.DataFrame([
            {
                "Batsman": b.get("name", ""),
                "Runs": b.get("runs", 0),
                "Balls": b.get("balls", 0),
                "4s": b.get("fours", 0),
                "6s": b.get("sixes", 0),
                "SR": b.get("strkrate", 0),
                "Out": b.get("outdec", ""),
            }
            for b in innings.get("batsman", [])
        ])

        # ☄️ Bowling
        bowlers_df = pd.DataFrame([
            {
                "Bowler": bl.get("name", ""),
                "Overs": bl.get("overs", 0),
                "Runs": bl.get("runs", 0),
                "Wickets": bl.get("wickets", 0),
                "Economy": bl.get("economy", 0),
            }
            for bl in innings.get("bowler", [])
        ])

        # 🔎 Summary
        if not batsmen_df.empty:
            top_bat = batsmen_df.loc[batsmen_df["Runs"].idxmax()]
            bat_summary = f"🏏 Top Scorer: **{top_bat['Batsman']}** with {top_bat['Runs']} runs ({top_bat['Balls']} balls, SR {top_bat['SR']})"
        else:
            bat_summary = "🏏 No batting data"

        if not bowlers_df.empty:
            top_bowl = bowlers_df.loc[bowlers_df["Wickets"].idxmax()]
            bowl_summary = f"☄️ Best Bowler: **{top_bowl['Bowler']}** with {top_bowl['Wickets']} wickets, Econ {top_bowl['Economy']}"
        else:
            bowl_summary = "☄️ No bowling data"

        st.markdown(f"""
        <div class="chat-box">
        🤖 Match Summary (Inning {i}):<br>
        {bat_summary}<br>
        {bowl_summary}
        </div>
        """, unsafe_allow_html=True)

        # Batting Table + Chart
        if not batsmen_df.empty:
            st.write("### 🏏 Batting")
            st.dataframe(batsmen_df, use_container_width=True)
            st.bar_chart(batsmen_df.set_index("Batsman")["Runs"])

        # Bowling Table + Chart
        if not bowlers_df.empty:
            st.write("### ☄️ Bowling")
            st.dataframe(bowlers_df, use_container_width=True)
            st.bar_chart(bowlers_df.set_index("Bowler")["Wickets"])

        st.markdown("---")

# ---------------- Live Matches ----------------
def show_live_matches():
    st.markdown("""
    <div class="hero">
        <h1>🏏 Cricbuzz LiveStats</h1>
        <p>📡 Real-time cricket updates with layman-friendly summaries & stats</p>
    </div>
    """, unsafe_allow_html=True)

    api = CricbuzzAPI()
    data = api.get_live_matches()

    if not data or "typeMatches" not in data:
        st.warning("⚠ No live matches available right now.")
        return

    series_options = {}
    for type_match in data.get("typeMatches", []):
        match_type = type_match.get("matchType", "Unknown")
        for series in type_match.get("seriesMatches", []):
            series_info = series.get("seriesAdWrapper", {})
            if "matches" in series_info:
                series_name = series_info.get("seriesName", "Unknown Series")
                key = f"{series_name} ({match_type})"
                series_options[key] = series_info["matches"]

    if not series_options:
        st.warning("⚠ No active series at the moment.")
        return

    selected_series = st.selectbox("🛑 LIVE 🎥 Select a Live Series", list(series_options.keys()))
    matches = series_options[selected_series]

    for match in matches:
        match_info = match.get("matchInfo", {})
        match_score = match.get("matchScore", {})

        team1 = match_info.get("team1", {}).get("teamName", "Team 1")
        team2 = match_info.get("team2", {}).get("teamName", "Team 2")
        match_id = match_info.get("matchId", "")

        st.markdown(f"<div class='match-card'><h3>🆚 {team1} vs {team2}</h3>", unsafe_allow_html=True)
        st.write(f"**Match:** {match_info.get('matchDesc', '')} ({match_info.get('matchFormat', '')})")
        st.write(f"**Status:** {match_info.get('status', '')}")
        st.write(f"**State:** {match_info.get('stateTitle', '')}")

        venue = match_info.get("venueInfo", {})
        st.write(f"**Venue:** {venue.get('ground', '')}, {venue.get('city', '')}")
        st.write(f"**Start Time:** {format_time(match_info.get('startDate'))}")
        st.write(f"**End Time:** {format_time(match_info.get('endDate'))}")

        # Scores
        if "team1Score" in match_score:
            t1 = match_info.get("team1", {}).get("teamSName", "Team 1")
            t1_inn = match_score.get("team1Score", {}).get("inngs1", {})
            st.success(f"{t1}: {t1_inn.get('runs', 0)}/{t1_inn.get('wickets', 0)} in {t1_inn.get('overs', 0)} overs")

        if "team2Score" in match_score:
            t2 = match_info.get("team2", {}).get("teamSName", "Team 2")
            t2_inn = match_score.get("team2Score", {}).get("inngs1", {})
            st.success(f"{t2}: {t2_inn.get('runs', 0)}/{t2_inn.get('wickets', 0)} in {t2_inn.get('overs', 0)} overs")

        if match_id and st.button(f"📑 View Scorecard - {team1} vs {team2}", key=f"btn_{match_id}"):
            show_innings_scorecard(api, match_id)

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")


# ✅ Sidebar
st.sidebar.title("ℹ️ About")
st.sidebar.markdown("""
<div class="about-box">
    <h3>✨ About Cricbuzz LiveStats</h3>
    🚀 Built with <b>Streamlit + Cricbuzz API</b><br><br>
    ✅ Real-time <b>Live Matches</b><br>
    📊 Easy-to-read <b>Batting & Bowling Tables</b><br>
    🌍 Explore <b>Series & Match Info</b><br>
</div>
""", unsafe_allow_html=True)

# 🚀 Run App
show_live_matches()
