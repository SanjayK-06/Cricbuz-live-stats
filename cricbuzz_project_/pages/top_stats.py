import streamlit as st
import http.client
import json
import requests
import pandas as pd
import os
from urllib.parse import quote

# ---------------- Setup ----------------
st.set_page_config(page_title="🏏 Cricbuzz LiveStats", layout="wide")

# 🔑 Direct API Key (replace with your key)
API_KEY = "d723372ef9mshf19bc74dba24b9fp17cbc7jsn6ff8a547531f"

HEADERS = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"}
BASE_URL = "cricbuzz-cricket.p.rapidapi.com"

# ---------------- Global CSS ----------------
st.markdown("""
    <style>
    body {
        font-family: "Poppins", sans-serif !important;
        background: #f9f9f9;
        color: #111;
    }
    /* Hero Section */
    .hero {
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #a18cd1, #fbc2eb);
        color: white;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0px 6px 18px rgba(0,0,0,0.15);
    }
    .hero h1 { font-size: 38px; font-weight: 700; margin-bottom: 8px; }
    .hero p { font-size: 18px; margin: 0; }
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #a18cd1, #fbc2eb);
        color: white !important;
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
        font-size: 16px !important;
        font-weight: 500 !important;
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
    /* DataFrame Styling */
    div[data-testid="stDataFrame"] table {
        border: 2px solid #e0c8f5;
        border-radius: 8px;
    }
    .stMarkdown p {
        font-size: 16px;
    }
    /* Card Style */
    .profile-card {
        background: #fff;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0px 6px 18px rgba(161, 140, 209, 0.25);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- Helper Functions ----------------
def search_players(query):
    query_encoded = quote(query)
    conn = http.client.HTTPSConnection(BASE_URL)
    conn.request("GET", f"/stats/v1/player/search?plrN={query_encoded}", headers=HEADERS)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    try:
        return json.loads(data.decode("utf-8"))
    except:
        return {}

def get_player_details(player_id):
    conn = http.client.HTTPSConnection(BASE_URL)
    conn.request("GET", f"/stats/v1/player/{player_id}", headers=HEADERS)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    try:
        return json.loads(data.decode("utf-8"))
    except:
        return {}

def get_player_stats(player_id, stat_type="batting"):
    url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}/{stat_type}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return {}

def parse_stats_table(stats_json, drop_columns=None):
    if not stats_json or "headers" not in stats_json or "values" not in stats_json:
        return pd.DataFrame()
    headers = stats_json["headers"]
    rows = [row["values"] for row in stats_json["values"]]
    df = pd.DataFrame(rows, columns=headers)
    if drop_columns:
        df = df.drop(columns=drop_columns, errors="ignore")
    return df

# ---------------- Sidebar ----------------
st.sidebar.title("ℹ️ About")
st.sidebar.markdown("""
<div class="about-box">
    <h3>✨ About LiveStats</h3>
    🚀 <b>Real-time Player Profiles</b><br><br>
    🏆 <b>ICC Rankings (Card Design)</b><br><br>
    🏏 <b>Batting & Bowling Stats</b><br><br>
    📊 <b>Powered by Cricbuzz API</b>
</div>
""", unsafe_allow_html=True)

# ---------------- Main Page ----------------
st.markdown("""
<div class="hero">
    <h1>🏏 Cricbuzz LiveStats</h1>
    <p>Player Profiles • ICC Rankings • Batting & Bowling Stats</p>
</div>
""", unsafe_allow_html=True)

player_name = st.text_input("🔍 Enter player name (e.g. Virat Kohli, Joe Root):")

if player_name:
    results = search_players(player_name)

    if "player" in results and results["player"]:
        player_options = {p["name"]: p for p in results["player"]}
        selected_name = st.selectbox("Select a player:", list(player_options.keys()))
        selected_player = player_options[selected_name]

        tabs = st.tabs(["📌 Profile", "🏏 Batting Stats", "🎯 Bowling Stats"])

        # ---------------- Profile Tab ----------------
        with tabs[0]:
            details = get_player_details(selected_player["id"])
            st.markdown(f"""
            <div class="profile-card">
                <h2>{selected_player['name']} ({selected_player['teamName']})</h2>
                <p>📅 <b>DOB:</b> {selected_player.get('dob', 'N/A')}</p>
                <p>🧢 <b>Role:</b> {details.get('role', 'N/A')}</p>
                <p>🏏 <b>Batting Style:</b> {details.get('bat', 'N/A')}</p>
                <p>⚾ <b>Bowling Style:</b> {details.get('bowl', 'N/A')}</p>
                <p>🌍 <b>Birth Place:</b> {details.get('birthPlace', 'N/A')}</p>
                <p>👤👤👤 <b>Teams:</b> {details.get('teams', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)

            # ---------------- ICC Rankings ----------------
            if "rankings" in details and details["rankings"]:
                st.subheader("🏆 ICC Rankings")
                rankings = details["rankings"]

                col1, col2, col3 = st.columns(3)

                def styled_metric(title, value):
                    try:
                        rank_int = int(value)
                    except:
                        rank_int = None
                    color = "#F5F5F5"
                    if rank_int is not None:
                        if rank_int <= 5:
                            color = "#A8E6CF"
                        elif rank_int <= 10:
                            color = "#FFD3B6"
                    return f"""
                    <div style='background-color:{color};padding:10px;
                                border-radius:10px;margin:5px;
                                text-align:center;box-shadow:0 2px 5px rgba(0,0,0,0.1);'>
                        <h5 style='margin-bottom:5px;font-size:14px;'>{title}</h5>
                        <h3 style='margin:0;font-size:18px;color:#333;'>{value}</h3>
                    </div>
                    """

                with col1:
                    st.markdown("### 🏏 Batting")
                    for k, v in rankings.get("bat", {}).items():
                        if "DiffRank" not in k:
                            label = k.replace("odi", "ODI ").replace("test", "Test ").replace("t20", "T20 ").replace("Rank", " Rank").replace("Best", " Best")
                            st.markdown(styled_metric(label.strip(), v), unsafe_allow_html=True)

                with col2:
                    st.markdown("### ⚾ Bowling")
                    for k, v in rankings.get("bowl", {}).items():
                        if "DiffRank" not in k:
                            label = k.replace("odi", "ODI ").replace("test", "Test ").replace("t20", "T20 ").replace("Rank", " Rank").replace("Best", " Best")
                            st.markdown(styled_metric(label.strip(), v), unsafe_allow_html=True)

                with col3:
                    st.markdown("### 🏏⚾ All-Rounder")
                    for k, v in rankings.get("all", {}).items():
                        if "DiffRank" not in k:
                            label = k.replace("odi", "ODI ").replace("test", "Test ").replace("t20", "T20 ").replace("Rank", " Rank").replace("Best", " Best")
                            st.markdown(styled_metric(label.strip(), v), unsafe_allow_html=True)

        # ---------------- Batting Stats Tab ----------------
        with tabs[1]:
            st.subheader("🏏 Batting Stats")
            batting_stats = get_player_stats(selected_player["id"], "batting")
            df_bat = parse_stats_table(batting_stats, drop_columns=["400"])
            if not df_bat.empty:
                st.dataframe(df_bat, use_container_width=True)
            else:
                st.warning("No batting stats available.")

        # ---------------- Bowling Stats Tab ----------------
        with tabs[2]:
            st.subheader("☄ Bowling Stats")
            bowling_stats = get_player_stats(selected_player["id"], "bowling")
            df_bowl = parse_stats_table(bowling_stats, drop_columns=["10w"])
            if not df_bowl.empty:
                st.dataframe(df_bowl, use_container_width=True)
            else:
                st.warning("No bowling stats available.")
    else:
        st.warning("⚠ No players found. Try another name.")
