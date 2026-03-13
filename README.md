# 🏏 Cricbuzz LiveStats

### Real-Time Cricket Dashboard & SQL Analytics

**Cricbuzz LiveStats** is a modern cricket analytics dashboard that integrates **real-time match data from the Cricbuzz API** with **PostgreSQL database analytics**.
The project features a **stylish Streamlit interface**, **CRUD operations**, and **25+ SQL queries** designed to explore cricket statistics and trends.

This project demonstrates the integration of **API data, relational databases, analytics queries, and interactive dashboards**.

---

# 📌 Project Overview

Cricbuzz LiveStats provides a comprehensive platform to:

* Track **live cricket match scores**
* Explore **player statistics**
* Perform **SQL-based cricket analytics**
* Manage **player and match data**
* Visualize sports data through an interactive dashboard

The system combines **real-time API data with structured database analytics** to deliver both **live insights and historical analysis**.

---

# 🚀 Quick Start

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/cricbuzz-livestats.git
cd cricbuzz-livestats
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Setup PostgreSQL Database

Create a database named:

```
Cricbuzz
```

Then import the schema and tables defined in:

```
utils/db_connection.py
```

---

## 4️⃣ Run the Application

```bash
streamlit run app.py
```

---

## 5️⃣ Open the Dashboard

Navigate to:

```
http://localhost:8501
```

---

# 🎯 Key Features

### 📺 Live Match Tracking

Fetch real-time match scores and updates using the **Cricbuzz API via RapidAPI**.

### 📊 Player Statistics

View player performance data including **batting stats, bowling stats, and ICC rankings**.

### 🔍 SQL Analytics (25+ Queries)

Explore cricket insights through **SQL queries ranging from beginner to advanced level**.

### 🛠️ CRUD Operations

Manage database records with the ability to:

* Add players and matches
* Update existing records
* Delete records
* View stored data

### 🎨 Modern UI

The dashboard includes:

* Gradient UI themes
* Cricket stadium background
* Animated hero sections
* Interactive dashboard layout

### 📱 Responsive Dashboard

Clean layout designed for readability and smooth navigation.

---

# 🏗️ System Architecture

**Frontend**

* Streamlit
* Custom CSS styling
* Hero banners and UI animations

**Backend**

* PostgreSQL database
* Structured tables for players, matches, and statistics

**API Integration**

* Cricbuzz API (via RapidAPI)

**Analytics Layer**

* 25 SQL queries for statistical analysis

**Data Processing**

* Pandas for cleaning and displaying data

---

# 📊 SQL Query Categories

The project contains **25 SQL queries** categorized by difficulty level.

---

## 🟢 Beginner Queries (1–8)

* Basic `SELECT` statements
* `WHERE` filters
* `GROUP BY` aggregations
* Simple statistical calculations

Example insights:

* Total runs scored by players
* Average runs per format
* Wicket totals

---

## 🟡 Intermediate Queries (9–16)

* `JOIN` operations across multiple tables
* Subqueries
* Series-based performance analysis

Example insights:

* Player performance by series
* Match statistics by team
* Player comparisons

---

## 🔴 Advanced Queries (17–25)

* Window functions
* Common Table Expressions (CTEs)
* Ranking and performance trends

Example insights:

* Top performers across formats
* Player rankings based on performance metrics
* Trend analysis over seasons

---

# 🧰 Tech Stack

**Programming Language**

* Python 3.9+

**Web Framework**

* Streamlit

**Database**

* PostgreSQL

**Database Tools**

* SQLAlchemy
* psycopg2

**Data Processing**

* Pandas

**API Integration**

* Cricbuzz API (RapidAPI)

**Visualization**

* Streamlit DataFrames
* Future integration with Plotly / Matplotlib

**UI Styling**

* Custom CSS
* Gradient themes
* Animated UI elements

---

# 📁 Project Structure

```
cricbuzz_livestats/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
│
├── pages/                      # Streamlit multipage app
│   ├── home.py                 # Homepage & navigation
│   ├── live_matches.py         # Live Cricbuzz API integration
│   ├── top_stats.py            # Player statistics & rankings
│   ├── sql_queries.py          # SQL analytics queries
│   └── crud_operations.py      # CRUD operations
│
├── utils/
│   ├── api_utils.py            # Cricbuzz API utilities
│   └── db_connection.py        # PostgreSQL connection setup
│
└── notebooks/
    └── data_fetching.ipynb     # Data fetching and experimentation
```

---

# 🔑 API Configuration

The **RapidAPI key** is configured directly in the code.

Update your API key in:

```
utils/api_utils.py
```

Example configuration:

```python
self.headers = {
    "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY_HERE",
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}
```

---

# 🎨 UI Highlights

* Gradient sidebar navigation
* Animated cricket-themed hero section
* Interactive dashboard cards
* Smooth hover animations
* Cricket stadium background

The design focuses on **modern aesthetics while maintaining usability**.

---

# 🎓 Educational Value

This project is useful for learning:

* SQL query development
* API integration in Python
* Database design using PostgreSQL
* Building multipage Streamlit dashboards
* Sports data analytics
* Interactive UI design with CSS

It serves as a **complete end-to-end data analytics project combining API, database, and visualization layers**.

---

# 🚀 Future Enhancements

Potential improvements include:

* Real-time chart visualizations using **Plotly**
* Machine learning models for **match prediction**
* Player performance forecasting
* Cloud deployment
* User authentication system

---

# 👨‍💻 Author

**Sanjay Kannan**

Data Analytics | Python | SQL | Streamlit Developer

Built with ❤️ for **cricket enthusiasts and data science learners**.


