import streamlit as st
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from streamlit_option_menu import option_menu

# ---------------- Load ENV ----------------
dotenv_path = r"C:\Users\Amirtha\Downloads\cricbuzz_project_sanjay\utils\.env"
load_dotenv(dotenv_path)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "Cricbuz")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

def get_conn():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD
    )

# ---------------- Helpers ----------------
def fetch_players():
    with get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT player_id, full_name FROM players ORDER BY full_name;")
        return cur.fetchall()

def fetch_teams():
    with get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT team_id, team_name, country FROM teams ORDER BY team_name;")
        return cur.fetchall()

def fetch_all_players():
    with get_conn() as conn:
        df = pd.read_sql("""
            SELECT p.player_id, p.full_name,
                   COALESCE(p.nick_name,'—') AS nick_name,
                   COALESCE(t.team_name,'—') AS team,
                   COALESCE(t.country,'—') AS country,
                   COALESCE(p.role,'—') AS role,
                   COALESCE(p.batting_style,'N/A') AS batting_style,
                   COALESCE(p.bowling_style,'N/A') AS bowling_style,
                   p.team_id,
                   p.created_at
            FROM players p
            LEFT JOIN teams t ON p.team_id = t.team_id
            ORDER BY p.player_id;
        """, conn)
    return df

def insert_player(data):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            INSERT INTO players
            (player_id, full_name, nick_name, role, batting_style, bowling_style, team_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (player_id) DO NOTHING
            RETURNING player_id
        """, (
            data["player_id"], data["full_name"], data["nick_name"], data["role"],
            data["batting_style"], data["bowling_style"], data["team_id"]
        ))
        row = cur.fetchone()
        conn.commit()
        return row[0] if row else None

def update_player(pid, data):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            UPDATE players
            SET full_name=%s, nick_name=%s, role=%s,
                batting_style=%s, bowling_style=%s, team_id=%s
            WHERE player_id=%s
        """, (
            data["full_name"], data["nick_name"], data["role"],
            data["batting_style"], data["bowling_style"],
            data["team_id"], pid
        ))
        conn.commit()

def delete_player(pid):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM players WHERE player_id=%s", (pid,))
        conn.commit()

# ---------------- Page Config ----------------
st.set_page_config(page_title="✍️ Cricbuzz CRUD Manager", layout="wide")

# ---------------- Custom CSS ----------------
st.markdown("""
    <style>
    body {
        margin: 0;
        font-family: 'Poppins', sans-serif;
        background: #f9f9f9;
        color: #111;
    }

    /* Sidebar Gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #a18cd1, #fbc2eb);
        color: white !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
        font-size: 18px !important;
        font-weight: 600 !important;
    }

    /* Hero */
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
    .hero h1 { font-size: 32px; font-weight: 700; margin-bottom: 8px; }
    .hero p { font-size: 18px; margin: 0; }

    /* Table Styling */
    .dataframe {
        border-collapse: collapse !important;
        width: 100%;
        border: 3px double #a18cd1; 
        border-radius: 8px;
        overflow: hidden;
    }
    .dataframe th {
        background: linear-gradient(90deg, #a18cd1, #fbc2eb);
        color: white;
        font-weight: bold;
        padding: 10px;
        border: 2px double #a18cd1;
        text-align: center;
    }
    .dataframe td {
        border: 1px solid #e0c8f5;
        padding: 8px;
        text-align: center;
        color: #333;
    }
    .dataframe tr:nth-child(even) { background-color: #fdf5ff; }
    .dataframe tr:hover { background-color: #f3e8ff; }

    /* Highlight rows */
    .highlight-modified { background-color: #e0c3fc !important; }
    .highlight-deleted { background-color: #f8cdda !important; }

    /* Alerts */
    .stAlert {
        border-radius: 10px;
        padding: 15px;
        font-weight: 600;
    }
    .stAlert.success {
        background: linear-gradient(90deg, #a1c4fd, #c2e9fb);
        color: #1e3a8a;
    }
    .stAlert.warning {
        background: linear-gradient(90deg, #fceabb, #f8b500);
        color: #7c2d12;
    }
    .stAlert.error {
        background: linear-gradient(90deg, #fbc2eb, #a6c1ee);
        color: #7f1d1d;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- Hero Section ----------------
st.markdown("""
<div class="hero">
    <h1>✍️ Cricbuzz CRUD Manager</h1>
    <p>Add, Update, Delete & View Players from Database</p>
</div>
""", unsafe_allow_html=True)

# ---------------- Sidebar ----------------
with st.sidebar:
    menu = option_menu(
        "Navigation",
        ["➕ Add Player", "✏️ Update Player", "🗑 Delete Player", "📊 View Players"],
        icons=["plus-circle", "pencil-square", "trash", "table"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background": "linear-gradient(180deg, #a18cd1, #fbc2eb)"},
            "icon": {"color": "white", "font-size": "20px"},
            "nav-link": {"font-size": "18px", "color": "white", "text-align": "left", "margin":"2px"},
            "nav-link-selected": {"background-color": "#8e44ad", "color": "white"},
        }
    )

# ---------------- Session State ----------------
if "last_modified_id" not in st.session_state: st.session_state.last_modified_id = None
if "last_deleted_id" not in st.session_state: st.session_state.last_deleted_id = None

roles = ["Batsman", "Bowler", "All-Rounder", "Wicket-Keeper", "Captain", "—"]
batting_styles = ["Right-hand Bat", "Left-hand Bat", "N/A"]
bowling_styles = [
    "Right-arm Fast", "Right-arm Medium", "Right-arm Offbreak",
    "Left-arm Fast", "Left-arm Medium", "Left-arm Orthodox", "Legbreak Googly", "N/A"
]

# ---------------- Add ----------------
if menu == "➕ Add Player":
    st.subheader("➕ Add New Player")
    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            player_id = st.number_input("Player ID (from API)", min_value=1, step=1)
            full_name = st.text_input("Full Name")
            nick_name = st.text_input("Nick Name")
            role = st.selectbox("Role", roles)
        with col2:
            bat_style = st.selectbox("Batting Style", batting_styles)
            bowl_style = st.selectbox("Bowling Style", bowling_styles)
        teams = fetch_teams()
        team_map = {"— None —": None}
        for t in teams: team_map[f"{t['team_name']} ({t['country']})"] = t["team_id"]
        team_label = st.selectbox("Team", list(team_map.keys()))
        team_id = team_map[team_label]
        submit = st.form_submit_button("✅ Add Player")
        if submit:
            if not full_name.strip():
                st.error("⚠️ Full Name is required")
            else:
                new_id = insert_player({
                    "player_id": player_id, "full_name": full_name.strip(),
                    "nick_name": nick_name.strip(), "role": role,
                    "batting_style": bat_style, "bowling_style": bowl_style,
                    "team_id": team_id
                })
                if new_id:
                    st.session_state.last_modified_id, st.session_state.last_deleted_id = new_id, None
                    st.success(f"🎉 Player **{full_name}** added successfully")
                    st.balloons()
                else: st.warning("⚠️ Player already exists!")

# ---------------- Update ----------------
elif menu == "✏️ Update Player":
    st.subheader("✏️ Update Player")
    players = fetch_players()
    if not players: st.warning("No players found.")
    else:
        pick = st.selectbox("🔍 Search Player", players, format_func=lambda x: x['full_name'])
        sel_id = pick["player_id"]
        df = fetch_all_players()
        row = df[df["player_id"] == sel_id].iloc[0]
        with st.form("update_form", clear_on_submit=False):
            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input("Full Name", value=row["full_name"])
                nick_name = st.text_input("Nick Name", value=row["nick_name"])
                role = st.selectbox("Role", roles, index=roles.index(row["role"]) if row["role"] in roles else len(roles)-1)
            with col2:
                bat_style = st.selectbox("Batting Style", batting_styles, index=batting_styles.index(row["batting_style"]) if row["batting_style"] in batting_styles else 2)
                bowl_style = st.selectbox("Bowling Style", bowling_styles, index=bowling_styles.index(row["bowling_style"]) if row["bowling_style"] in bowling_styles else len(bowling_styles)-1)
            teams = fetch_teams()
            team_map = {"— None —": None}
            for t in teams: team_map[f"{t['team_name']} ({t['country']})"] = t["team_id"]
            team_label = st.selectbox("Team", list(team_map.keys()), index=list(team_map.values()).index(row["team_id"]) if row["team_id"] in team_map.values() else 0)
            team_id = team_map[team_label]
            submit = st.form_submit_button("🔄 Update Player")
            if submit:
                update_player(sel_id, {
                    "full_name": full_name.strip(), "nick_name": nick_name.strip(),
                    "role": role, "batting_style": bat_style,
                    "bowling_style": bowl_style, "team_id": team_id
                })
                st.session_state.last_modified_id, st.session_state.last_deleted_id = sel_id, None
                st.success(f"✅ Player **{full_name}** updated successfully")
                st.balloons()

# ---------------- Delete ----------------
elif menu == "🗑 Delete Player":
    st.subheader("🗑 Delete Player")
    players = fetch_players()
    if not players: st.warning("No players to delete.")
    else:
        pick = st.selectbox("🔍 Search Player to Delete", players, format_func=lambda x: x['full_name'])
        sel_id = pick["player_id"]
        st.error("⚠️ Deletion is permanent!")
        confirm = st.checkbox("Confirm delete?")
        if st.button("🚨 Delete"):
            if not confirm: st.error("Please confirm delete.")
            else:
                st.session_state.last_deleted_id, st.session_state.last_modified_id = sel_id, None
                delete_player(sel_id)
                st.success("❌ Player deleted successfully")
                st.balloons()

# ---------------- View ----------------
elif menu == "📊 View Players":
    st.subheader("📊 Player Records")
    df = fetch_all_players()
    search = st.text_input("🔍 Search Player")
    if search: df = df[df["full_name"].str.contains(search, case=False)]
    def highlight_row(x):
        if 'player_id' in x:
            if st.session_state.last_modified_id and x['player_id'] == st.session_state.last_modified_id:
                return ['background-color: #e0c3fc'] * len(x)
            if st.session_state.last_deleted_id and x['player_id'] == st.session_state.last_deleted_id:
                return ['background-color: #f8cdda'] * len(x)
        return [''] * len(x)
    st.dataframe(df.style.apply(highlight_row, axis=1))
