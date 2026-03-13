import os
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px


# Extract file
DIR_NAME = os.path.dirname(os.path.abspath(__file__))
data = pd.read_csv(os.path.join(DIR_NAME, 'games.csv'))

# Convert Rating to numeric format based on the condition (data based on ESRB (USA) and PEGI (Europe) rating)
RATING_DICT = {
    'EC': 3,
    'E': 6,
    'K-A': 6,
    'E10+': 10,
    'T': 13,
    'M': 17,
    'AO': 18
}

data['Rating_Num'] = data['Rating'].map(RATING_DICT)

# Переводим в нужный тип и оставляем только данные за 1990 - 2010 года. Удаляем NaN
data['User_Score'] = pd.to_numeric(data['User_Score'], errors='coerce')
data['Critic_Score'] = pd.to_numeric(data['Critic_Score'], errors='coerce')
data = data.astype({
    'Year_of_Release': 'Int64',
    'Rating_Num': 'Int64'
})
data = data[data['Year_of_Release'].between(1990, 2010)]

# The final edited dataset 
df = data.dropna().reset_index(drop=True).copy()


# Creating a dash
app = Dash(__name__, external_stylesheets=[dbc.themes.YETI])

available_genres = df['Genre'].unique()
available_platforms = df['Platform'].unique()
min_year, max_year = df['Year_of_Release'].min(), df['Year_of_Release'].max()
kpi_name_1 = "Total games"
kpi_name_2 = "Avg user rating"
kpi_name_3 = "Avg critic rating"
graph_name_1 = "Genre rating"
graph_name_2 = "Critics vs Users"
graph_name_3 = "Releases by year"


# Creating the structure and arrangement of elements 
app.layout = dbc.Container([
    html.Div([
            html.H1([
                "Video game Statistics",
                # Сreate a badge (?)
                dbc.Badge(
                    "?", 
                    id="tooltip-target",
                    pill=True,
                    color="info",
                    className="ms-2",
                    style={"cursor": "pointer", "fontSize": "0.5em", "verticalAlign": "middle"}
                )
            ], className="text-center my-4"),

            # Text hint
            dbc.Tooltip(
                """
                Video Game Market Dashboard (1990-2010). 
                Use the filters below to select platforms, genres, and release years. 
                Charts update automatically.
                """,
                target="tooltip-target",
                placement="bottom",
            )
        ]),

    # Filter block
    dbc.Row([
        dbc.Col([
            html.Label("Platforms:"),
            dcc.Dropdown(
                id='platforms_dropdown',
                options=available_platforms,
                value=available_platforms,
                multi=True,
                placeholder="Select a platforms")
        ], width=4),
        dbc.Col([
            html.Label("Genres:"),
            dcc.Dropdown(
                id='genres_dropdown',
                options=available_genres,
                value=available_genres,
                multi=True,
                placeholder="Select a genres")
        ], width=4),
        dbc.Col([
            html.Label("Year:"),
            dcc.RangeSlider(
                id='years_slider',
                min=min_year,
                max=max_year,
                value=[min_year, max_year],
                step=1)
        ], width=4),
    ], className="mb-4 bg-light p-3 rounded"),

    # Cards block
    # Line 1: 3 cards with KPI
    dbc.Row([
        dbc.Col(id='card_total_container', width=4),
        dbc.Col(id='card_user_container', width=4),
        dbc.Col(id='card_critic_container', width=4),
    ], className="mb-4 gx-2"),

    # Graphs block
    # Line 2: 3 charts
    dbc.Row([
        dbc.Col(dcc.Graph(id='chart_bar'), width=4),
        dbc.Col(dcc.Graph(id='chart_scatter'), width=4),
        dbc.Col(dcc.Graph(id='chart_area'), width=4)
    ], className="mb-4"),

], fluid=True)


# Card creation function (1st line)
def make_card(title, value):
    return dbc.Card(
        dbc.CardBody([
            html.P(title, className="card-title text-secondary"),
            html.H3(value, className="card-text text-primary"),
        ]),
        className="text-center shadow-sm"
    )


# Calling input and output
@app.callback(
    Output('card_total_container', 'children'),
    Output('card_user_container', 'children'),
    Output('card_critic_container', 'children'),
    Output('chart_bar', 'figure'),
    Output('chart_scatter', 'figure'),
    Output('chart_area', 'figure'),
    Input('platforms_dropdown', 'value'),
    Input('genres_dropdown', 'value'),
    Input('years_slider', 'value')
)
# Calculation and rendering filters, cards and charts
def update_all(platforms, genres, year_range):
    # Filtering
    df_filters = df[
        (df['Platform'].isin(platforms)) &
        (df['Genre'].isin(genres)) &
        (df['Year_of_Release'].between(year_range[0], year_range[1]))
    ].copy()

    # Calculation value for cards
    val1 = df_filters['Name'].count()
    val2 = round(df_filters['User_Score'].mean(),
                 1) if not df_filters.empty else 0
    val3 = round(df_filters['Critic_Score'].mean(),
                 1) if not df_filters.empty else 0

    # Creating card objects using the function @make_card
    card1 = make_card(kpi_name_1, val1)
    card2 = make_card(kpi_name_2, val2)
    card3 = make_card(kpi_name_3, val3)

    # 1. Bar chart
    avg_rating = (df_filters.groupby('Genre', as_index=False)['Rating_Num']
                            .mean()
                            .sort_values('Rating_Num', ascending=False))

    fig4 = px.bar(
        avg_rating,
        x='Genre',
        y='Rating_Num',
        title=graph_name_1
    )

    # 2. Scatter plot
    fig5 = px.scatter(
        df_filters,
        x='Critic_Score',
        y='User_Score',
        color='Genre',
        title=graph_name_2
    )

    # 3. Area chart
    graph6 = (df_filters.groupby(['Year_of_Release', 'Platform'], as_index=False)
                        .agg(Games_Count=('Genre', 'count')))
    fig6 = px.area(
        graph6,
        x='Year_of_Release',
        y='Games_Count',
        color='Platform',
        title=graph_name_3
    )

# Style for all charts
    for f in [fig4, fig5, fig6]:
        f.update_layout(
            title_x=0.1,
            margin=dict(l=0, r=0, t=50, b=0)
        )

    return card1, card2, card3, fig4, fig5, fig6


if __name__ == "__main__":
    app.run(debug=True)
