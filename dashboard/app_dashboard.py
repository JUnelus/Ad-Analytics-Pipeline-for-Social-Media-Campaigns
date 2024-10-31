import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from google.cloud import bigquery
import pandas as pd
import plotly.express as px

# Initialize the Dash app and BigQuery client
app = dash.Dash(__name__)
client = bigquery.Client()

def fetch_data():
    # Query to retrieve data from BigQuery
    query = "SELECT title, score, comments FROM your_dataset.reddit_table LIMIT 100"
    return pd.DataFrame([dict(row) for row in client.query(query)])

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Reddit Ad Performance Metrics"),
    html.Label("Select Metric"),
    dcc.Dropdown(
        id="metric-dropdown",
        options=[
            {"label": "Score", "value": "score"},
            {"label": "Comments", "value": "comments"}
        ],
        value="score",
        clearable=False
    ),
    dcc.Graph(id="reddit-graph"),
    html.Button("Refresh Data", id="refresh-button", n_clicks=0)
])

# Callback to update the graph based on selected metric and refresh button
@app.callback(
    Output("reddit-graph", "figure"),
    [Input("metric-dropdown", "value"), Input("refresh-button", "n_clicks")]
)
def update_graph(selected_metric, n_clicks):
    # Fetch data from BigQuery
    df = fetch_data()

    # Create a bar chart for the selected metric
    fig = px.bar(
        df,
        x="title",
        y=selected_metric,
        title=f"Top Reddit Posts by {selected_metric.capitalize()}",
        labels={"title": "Post Title", selected_metric: selected_metric.capitalize()}
    )
    fig.update_layout(
        xaxis={"categoryorder": "total descending"},
        xaxis_title="Post Title",
        yaxis_title=selected_metric.capitalize(),
    )

    return fig

# Run the dashboard server
if __name__ == "__main__":
    app.run_server(debug=True)