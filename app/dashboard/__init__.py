# In your Flask app (e.g., app.py or dashboard.py in your blueprints)
from flask import Blueprint, render_template
from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import json

# Create Blueprint
dashboard_bp = Blueprint("dashboard", __name__)


def init_dashboard(flask_app):
    dash_app = Dash(
        __name__,
        server=flask_app,
        url_base_pathname="/dashboard/viz/",
        assets_folder="static",
    )

    # Create the layout
    dash_app.layout = html.Div(
        [
            # Store component to hold the data
            dcc.Store(id="spotify-data-store"),
            html.H1("Your Spotify Listening History"),
            # Loading component to show loading state
            dcc.Loading(
                id="loading-graphs",
                type="default",
                children=[
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H2("Top 5 Artists"),
                                    dcc.Graph(
                                        id="top-artists-chart",
                                        figure={},  # Initialize with empty figure
                                    ),
                                ]
                            ),
                            html.Div(
                                [
                                    html.H2("Top 5 Tracks"),
                                    dcc.Graph(
                                        id="top-tracks-chart",
                                        figure={},  # Initialize with empty figure
                                    ),
                                ]
                            ),
                            html.Div(
                                [
                                    html.H2("Listening Hours Distribution"),
                                    dcc.Graph(
                                        id="hours-distribution-chart",
                                        figure={},  # Initialize with empty figure
                                    ),
                                ]
                            ),
                            html.Div(
                                [
                                    html.H2("Monthly Listening Hours"),
                                    dcc.Graph(
                                        id="monthly-hours-chart",
                                        figure={},  # Initialize with empty figure
                                    ),
                                ]
                            ),
                        ]
                    )
                ],
            ),
        ]
    )

    # Add custom JavaScript to the index page
    dash_app.index_string = """
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
        </head>
        <body>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
                <script>
                    // Function to load data from IndexedDB
                    async function loadFromIndexedDB() {
                        return new Promise((resolve, reject) => {
                            const request = indexedDB.open("MyDatabase", 2);
                            
                            request.onerror = () => reject(request.error);
                            
                            request.onsuccess = (event) => {
                                const db = event.target.result;
                                const tx = db.transaction("jsonStore", "readonly");
                                const store = tx.objectStore("jsonStore");
                                const getRequest = store.get("myBigData");
                                
                                getRequest.onerror = () => reject(getRequest.error);
                                getRequest.onsuccess = () => resolve(getRequest.result);
                            };
                        });
                    }

                    // Load data when page loads
                    document.addEventListener('DOMContentLoaded', async () => {
                        try {
                            const data = await loadFromIndexedDB();
                            if (data) {
                                // Get the dcc.Store component
                                const store = document.querySelector('#spotify-data-store');
                                if (store) {
                                    // Update the store's data property
                                    store._dashprivate_.setProps({
                                        'data': JSON.stringify(data)
                                    });
                                }
                            }
                        } catch (error) {
                            console.error('Error loading data:', error);
                        }
                    });
                </script>
            </footer>
        </body>
    </html>
    """

    @dash_app.callback(
        [
            Output("top-artists-chart", "figure"),
            Output("top-tracks-chart", "figure"),
            Output("hours-distribution-chart", "figure"),
            Output("monthly-hours-chart", "figure"),
        ],
        [Input("spotify-data-store", "data")],
    )
    def update_charts(json_data):
        # Create empty figures as default
        empty_fig = {"data": [], "layout": {"title": "Loading..."}}

        if not json_data:
            return empty_fig, empty_fig, empty_fig, empty_fig

        try:
            data = json.loads(json_data)

            # Process data for charts
            artist_counts = {}
            track_counts = {}
            hours_distribution = [0] * 24
            monthly_hours = {}

            for item in data:
                # Top artists
                artist = item.get("master_metadata_album_artist_name")
                if artist:
                    artist_counts[artist] = artist_counts.get(artist, 0) + 1

                # Top tracks
                track = item.get("master_metadata_track_name")
                if track:
                    track_counts[track] = track_counts.get(track, 0) + 1

                # Hours distribution
                timestamp = item.get("ts")
                if timestamp:
                    try:
                        hour = int(timestamp.split("T")[1].split(":")[0])
                        hours_distribution[hour] += 1
                    except (IndexError, ValueError):
                        continue

                # Monthly distribution
                if timestamp:
                    try:
                        month = timestamp.split("-")[0] + "-" + timestamp.split("-")[1]
                        monthly_hours[month] = monthly_hours.get(month, 0) + 1
                    except IndexError:
                        continue

            # Create top artists chart
            top_artists = sorted(
                artist_counts.items(), key=lambda x: x[1], reverse=True
            )[:5]
            artists_fig = px.bar(
                x=[a[0] for a in top_artists],
                y=[a[1] for a in top_artists],
                title="Top 5 Artists",
            )

            # Create top tracks chart
            top_tracks = sorted(track_counts.items(), key=lambda x: x[1], reverse=True)[
                :5
            ]
            tracks_fig = px.bar(
                x=[t[0] for t in top_tracks],
                y=[t[1] for t in top_tracks],
                title="Top 5 Tracks",
            )

            # Create hours distribution chart
            hours_fig = px.line(
                x=list(range(24)),
                y=hours_distribution,
                title="Listening Hours Distribution",
            )

            # Create monthly hours chart
            sorted_months = sorted(monthly_hours.keys())
            monthly_fig = px.line(
                x=sorted_months,
                y=[monthly_hours[month] for month in sorted_months],
                title="Monthly Listening Hours",
            )

            return artists_fig, tracks_fig, hours_fig, monthly_fig

        except Exception as e:
            print(f"Error processing data: {e}")
            return empty_fig, empty_fig, empty_fig, empty_fig

    return dash_app


from app.dashboard import routes
