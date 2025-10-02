from datetime import datetime
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

import db, db_with_local_cache

# Global state
query_count = 0
last_query = ""

# Get min/max dates
min_date, max_date = db.get_min_max()

# Initial data
query = db.get_query(min_date, max_date)
df = db.run_query(query)
fig = px.line(df, x="day", y="count", title="Posts per Day")

# Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("📊 StackOverflow Posts Explorer"),

    html.Div([
        html.Label("Cache data?"),
        dcc.RadioItems(
            id="cache-toggle",
            options=[
                {"label": "Yes", "value": "yes"},
                {"label": "No", "value": "no"}
            ],
            value="no",
            inline=True
        )
    ], style={"marginBottom": "20px"}),

    html.Div([
        html.Label("Select timeframe:"),
        dcc.DatePickerRange(
            id="date-picker-range",
            min_date_allowed=min_date,
            max_date_allowed=max_date,
            start_date=min_date,
            end_date=max_date,
            display_format="YYYY-MM-DD",
            style={"marginBottom": "20px"}
        )
    ]),

    dcc.Graph(
        id="posts-graph",
        figure=fig,
        config={"staticPlot": True}
    ),

    html.Div(id="date-range-output", style={"marginTop": "10px"}),
    html.Div(id="query-count-output", style={"marginTop": "10px", "fontWeight": "bold"}),
    html.Div(id="last-query-output", style={
        "marginTop": "20px",
        "fontFamily": "monospace",
        "whiteSpace": "pre-wrap"
    })
])


@app.callback(
    Output("posts-graph", "figure"),
    Output("date-range-output", "children"),
    Output("query-count-output", "children"),
    Output("last-query-output", "children"),
    Input("date-picker-range", "start_date"),
    Input("date-picker-range", "end_date"),
    Input("cache-toggle", "value")
)
def update_graph(start_date_str, end_date_str, cache_option):
    global query_count, last_query

    start = datetime.fromisoformat(start_date_str).date()
    end = datetime.fromisoformat(end_date_str).date()

    db_module = db_with_local_cache if cache_option == "yes" else db
    query = db_module.get_query(start, end)
    df_new = db_module.run_query(query)

    query_count += 1
    last_query = query

    fig = px.line(df_new, x="day", y="count", title="Posts per Day")

    return (
        fig,
        f"Current range: {start} → {end}",
        f"Total queries executed: {query_count}",
        last_query
    )


if __name__ == "__main__":
    app.run(debug=True)
