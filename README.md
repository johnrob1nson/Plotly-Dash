# 🎮 Video Game Statistics Dashboard

An interactive dashboard for video game market analysis, built with **Plotly Dash** and **Dash Bootstrap Components**.

## 📋 Description

The application visualizes video game statistics for the **1990–2010** period based on the `games.csv` dataset (~16,700 records). The dashboard allows filtering data by platform, genre, and release year, displaying key metrics and charts in real time.

## 🔧 Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | Dash 4.0 |
| Visualization | Plotly Express |
| UI Components | Dash Bootstrap (YETI theme) |
| Data Processing | Pandas |

## 📊 Dashboard Features

### Filters
- **Platforms** — multi-select dropdown (PS2, Wii, X360, PC, etc.)
- **Genres** — multi-select dropdown (Action, Sports, RPG, etc.)
- **Release Year** — range slider (1990–2010)

### KPI Cards
- **Total games** — total number of games
- **Avg user rating** — average user score
- **Avg critic rating** — average critic score

### Charts
- **Genre rating** — bar chart of average age rating by genre (ESRB/PEGI)
- **Critics vs Users** — scatter plot of critic scores vs. user scores
- **Releases by year** — area chart of release counts by year, broken down by platform

## 📁 Project Structure

```
Plotly-Dash/
├── games_market_dash.py   # Main application file
├── games.csv              # Video game dataset
├── requirements.txt       # Python dependencies
└── README.md
```

## 🗂 Dataset Description (`games.csv`)

| Field | Description |
|-------|-------------|
| `Name` | Game title |
| `Platform` | Platform (PS2, Wii, X360, PC, etc.) |
| `Year_of_Release` | Release year |
| `Genre` | Genre (Action, Sports, Role-Playing, etc.) |
| `Critic_Score` | Critic score (0–100) |
| `User_Score` | User score (0–10) |
| `Rating` | Age rating (ESRB: E, T, M, AO, etc.) |

## 🚀 Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python games_market_dash.py
```

The app will be available at: **http://127.0.0.1:8050**
