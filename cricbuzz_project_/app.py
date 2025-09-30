import streamlit as st

# ----------------- Page Config -----------------
st.set_page_config(
    page_title="🏏 Cricbuzz LiveStats",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- Custom CSS -----------------
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">

    <style>
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif !important; }

    body {
        margin: 0;
        background: linear-gradient(135deg, #fdfbfb, #f5f7fa, #fce4ec);
        background-attachment: fixed;
        color: #222;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #a18cd1, #fbc2eb);
        color: white !important;
        border-right: 2px solid #8e44ad;
    }
    [data-testid="stSidebar"] * {
        color: #fff !important;
        font-size: 18px !important;
        font-weight: 600 !important;
    }

    /* Hero */
    .hero {
        text-align: center;
        padding: 40px 25px;
        background: linear-gradient(135deg, #ff9a9e, #fad0c4);
        border-radius: 20px;
        margin: 0 auto 35px auto;
        max-width: 95%;
        box-shadow: 0px 8px 25px rgba(0,0,0,0.15);
    }
    .hero h1 { font-size: 42px; font-weight: 700; margin-bottom: 12px; color: #2c3e50; }
    .hero p { font-size: 20px; font-weight: 400; color: #444; }

    /* Section Titles */
    .section-title {
        font-size: 26px;
        font-weight: 700;
        color: #6a11cb;
        margin: 40px 0 20px 0;
        text-align: center;
        position: relative;
    }
    .section-title::after {
        content: "";
        display: block;
        width: 80px;
        height: 4px;
        background: linear-gradient(90deg, #ff9a9e, #fad0c4);
        margin: 8px auto 0 auto;
        border-radius: 2px;
    }

    /* Cards with Highlight */
    .section-container {
        padding: 25px 15px;
        margin: 20px auto 35px auto;
        max-width: 1100px;
    }
    .section-flex {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        justify-content: center;
    }
    .card {
        flex: 1 1 220px;
        background: linear-gradient(145deg, #ffffff, #f9f9ff);
        border-radius: 18px;
        padding: 25px;
        text-align: center;
        border: 2px solid transparent;
        background-clip: padding-box;
        position: relative;
        box-shadow: 0 6px 18px rgba(255,182,193,0.2);
        transition: all 0.35s ease-in-out;
        min-width: 220px;
    }
    .card::before {
        content: "";
        position: absolute;
        inset: 0;
        border-radius: 18px;
        padding: 2px;
        background: linear-gradient(135deg, #a18cd1, #fbc2eb, #fad0c4);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: destination-out;
        mask-composite: exclude;
        pointer-events: none;
    }
    .card:hover {
        transform: translateY(-8px) scale(1.03);
        box-shadow: 0px 14px 30px rgba(241,112,155,0.35);
    }
    .card-icon { font-size: 42px; margin-bottom: 12px; }
    .card h3 { font-size: 22px; font-weight: 700; color: #2c2c2c; margin-bottom: 8px; }
    .card p { font-size: 16px; color: #555; }

    /* Badges */
    .badges { text-align: center; margin-top: 20px; }
    .badge {
        display: inline-block;
        background: linear-gradient(90deg, #a1c4fd, #c2e9fb);
        color: #2c2c2c;
        padding: 10px 18px;
        border-radius: 20px;
        margin: 6px;
        font-size: 15px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 50px;
        padding: 16px;
        font-size: 15px;
        color: #444;
        border-top: 1px solid #ddd;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- Hero -----------------
st.markdown("""
<div class="hero">
    <h1>🏏 Cricbuzz LiveStats</h1>
    <p>Your all-in-one cricket dashboard with live data, analytics & management ✨</p>
</div>
""", unsafe_allow_html=True)

# ----------------- Page Content -----------------
st.write("Welcome to the **Cricbuzz LiveStats Dashboard**. Use the sidebar to explore features.")

# ----------------- Project Overview -----------------
st.markdown("<div class='section-title'>📖 Project Overview</div>", unsafe_allow_html=True)
st.write("""
I built **Cricbuzz LiveStats** to make cricket data more interactive and easy to explore.  
Instead of just seeing scores on a website, my goal was to create a dashboard where I can view **live matches, player stats, and custom insights** — all in one place.

This project combines **API integration, database management, and data visualization**.  
It’s not just about displaying data, but also about **storing it in a PostgreSQL database** so I can run SQL queries and learn from the data.
""")

# ----------------- Project Goals -----------------
st.markdown("<div class='section-title'>🎯 Project Goals</div>", unsafe_allow_html=True)
st.write("""
- Build a **real-time cricket dashboard** 🏏  
- Learn how to **integrate APIs with databases**  
- Improve **SQL & analytics skills** 📊  
- Create a **user-friendly web app** with Streamlit 🎨  
""")

# ----------------- How It Works -----------------
st.markdown("<div class='section-title'>⚙️ How It Works</div>", unsafe_allow_html=True)
st.markdown("""
<div class="section-container">
  <div class="section-flex">
    <div class="card"><div class="card-icon">🌐</div><h3>Fetch Data</h3><p>Collect match & player info</p></div>
    <div class="card"><div class="card-icon">🗄</div><h3>Store Data</h3><p>Save in PostgreSQL schema</p></div>
    <div class="card"><div class="card-icon">🧮</div><h3>SQL Analysis</h3><p>Top scorers, wickets, trends</p></div>
    <div class="card"><div class="card-icon">📊</div><h3>Visualize</h3><p>Charts & dashboards</p></div>
    <div class="card"><div class="card-icon">✍️</div><h3>Manage</h3><p>CRUD operations</p></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ----------------- Tech Stack -----------------
st.markdown("<div class='section-title'>🛠️ Tech Stack</div>", unsafe_allow_html=True)
st.write("""
- 🐍 **Python** – backend scripting & data handling  
- 🗄 **PostgreSQL** – database for storing matches & players  
- 📡 **Cricbuzz API** – live cricket data  
- 🎨 **Streamlit** – interactive dashboard UI  
- ⚡ **SQLAlchemy / psycopg2** – DB integration  
""")

# ----------------- Explore Pages -----------------
st.markdown("<div class='section-title'>📌 Explore Pages</div>", unsafe_allow_html=True)
st.markdown("""
<div class="section-container">
  <div class="section-flex">
    <div class="card"><div class="card-icon">🏏</div><h3>Live Match Page</h3><p>Shows live score updates with ball-by-ball details.</p></div>
    <div class="card"><div class="card-icon">🏆</div><h3>Player Stats Page</h3><p>See most runs, wickets, averages, and strike rates.</p></div>
    <div class="card"><div class="card-icon">📊</div><h3>SQL Insights Page</h3><p>Run analytics and learn SQL using real cricket data.</p></div>
    <div class="card"><div class="card-icon">✍️</div><h3>CRUD Page</h3><p>Manage database records (insert, update, delete).</p></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ----------------- What I Learned -----------------
st.markdown("<div class='section-title'>💡 What I Learned</div>", unsafe_allow_html=True)
st.markdown("""
<div class="badges">
    <span class="badge">🔗 Python + PostgreSQL</span>
    <span class="badge">🗝 Schema Design</span>
    <span class="badge">📡 API Integration</span>
    <span class="badge">📊 SQL Analytics</span>
    <span class="badge">🎨 Streamlit UI</span>
    <span class="badge">⚡ CRUD Operations</span>
</div>
""", unsafe_allow_html=True)



# ----------------- Footer -----------------
st.markdown("<div class='footer'>💡 Built with ❤️ by <b>Sanjay Kannan</b> | Cricbuzz LiveStats</div>", unsafe_allow_html=True)
