🏏 Cricbuzz LiveStats: Real-Time Cricket Dashboard & SQL Analytics

A modern cricket analytics dashboard that integrates live data from the Cricbuzz API with PostgreSQL database operations, featuring stylish UI, CRUD management, and 25+ SQL queries for analytics.

🚀 Quick Start

Clone Repository & Install Dependencies:

pip install -r requirements.txt

Setup Database (PostgreSQL):

Create database Cricbuzz

Import schema and tables from /utils/db_connection.py

Run Application:

cd cricbuzz_livestats
streamlit run app.py


Open Browser:
Navigate to 👉 http://localhost:8501

🎯 Features

📺 Live Matches – Real-time score updates with Cricbuzz API

📊 Player Stats – Batting & bowling career insights with ICC rankings

🔍 25+ SQL Queries – Beginner to advanced analytics (runs, wickets, trends)

🛠️ CRUD Operations – Add, update, delete player & match records

🖼️ Modern UI – Gradient themes + cricket stadium background 🏟️

📱 Responsive Design – Clean dashboard layout with animations

🏗️ Architecture

Frontend: Streamlit + custom CSS (hero banners, cards, animations)

Backend: PostgreSQL (players, matches, scorecards, stats)

API: Cricbuzz (via RapidAPI) → Live matches & player stats

Analytics: 25 SQL queries (Beginner → Advanced)

Visualization: Pandas + Streamlit DataFrames (future: Plotly/Matplotlib)

📊 SQL Query Categories
🟢 Beginner (1–8)

Simple SELECT, WHERE, GROUP BY

Aggregations like runs, wickets, averages

🟡 Intermediate (9–16)

JOINs, subqueries, multi-table analysis

Player vs series breakdowns

🔴 Advanced (17–25)

Window functions, CTEs, ranking queries

Performance trends across formats (ODI, Test, T20)

🛠️ Tech Stack

Python 3.9+

Streamlit – Interactive dashboard

PostgreSQL – Relational database

SQLAlchemy / psycopg2 – DB connection & queries

Cricbuzz API (RapidAPI) – Real-time cricket data

Pandas – Data cleaning & display

Custom CSS – Modern gradients, animations, cricket background


📁 Project Structure
cricbuzz_livestats/
├── app.py                 # Main application (entry point)
├── requirements.txt       # Dependencies
├── pages/                 # Streamlit pages
│   ├── home.py            # Hero + Overview + Navigation
│   ├── live_matches.py    # Live Cricbuzz API integration
│   ├── top_stats.py       # Player stats + ICC rankings
│   ├── sql_queries.py     # 25 SQL analytics queries
│   └── crud_operations.py # CRUD operations (PostgreSQL)
├── utils/                 
│   ├── api_utils.py       # Cricbuzz API management
│   └── db_connection.py   # DB connection (PostgreSQL + SQLAlchemy)
└── notebooks/             
    └── data_fetching.ipynb  # Data fetching 



    
🎓 Educational Value

Perfect for learning:

✅ SQL – 25 queries from basic to advanced

✅ API Integration – Cricbuzz REST API

✅ Database Design – Cricket schema in PostgreSQL

✅ Web Development – Streamlit apps with CSS styling

✅ Data Analytics – Sports insights (runs, wickets, trends)

🔑 API Configuration

API key is loaded directly in code (no .env needed).
Update in utils/api_utils.py:

self.headers = {
    "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY_HERE",
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

🎨 UI Highlights

🎨 Gradient Sidebar + Hero Banner

🏏 Animated Cricket Ball in Hero Section

📊 Interactive Cards & Sections

✨ Hover Animations + Modern Aesthetic

👨‍💻 Author

💡 Built with ❤️ by Sanjay Kannan
For cricket enthusiasts & data science learners
