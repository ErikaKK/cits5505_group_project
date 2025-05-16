import unittest
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from app.account.visualisation import Visualisation

class TestVisualisation(unittest.TestCase):
    def setUp(self):
        self.sample_df = pd.DataFrame([
            {"ts": "2024-01-01T10:00:00Z", "ms_played": 60000, "master_metadata_track_name": "SongA", "master_metadata_album_artist_name": "Artist1"},
            {"ts": "2024-01-01T11:00:00Z", "ms_played": 120000, "master_metadata_track_name": "SongB", "master_metadata_album_artist_name": "Artist2"},
            {"ts": "2024-01-02T10:00:00Z", "ms_played": 180000, "master_metadata_track_name": "SongA", "master_metadata_album_artist_name": "Artist1"},
            {"ts": "2024-02-01T10:00:00Z", "ms_played": 240000, "master_metadata_track_name": "SongC", "master_metadata_album_artist_name": "Artist3"},
            {"ts": "2024-02-01T11:00:00Z", "ms_played": 300000, "master_metadata_track_name": "SongD", "master_metadata_album_artist_name": "Artist4"},
        ])

    def test_process_data_success(self):
        vis = Visualisation()
        table = vis.process_data(self.sample_df)
        self.assertFalse(table.empty)
        self.assertTrue(set(["timestamp", "ms_played", "track_name", "artist_name", "mins_played", "hours_played", "time", "hour"]).issubset(table.columns))

    def test_process_data_missing_columns(self):
        vis = Visualisation()
        df = pd.DataFrame({"ts": ["2024-01-01T10:00:00Z"]})
        with self.assertRaises(Exception):
            vis.process_data(df)

    def test_top_artists_chart_with_data(self):
        vis = Visualisation()
        vis.process_data(self.sample_df)
        fig, ax = plt.subplots()
        vis.top_artists_chart(ax)
        plt.close(fig)

    def test_top_artists_chart_empty(self):
        vis = Visualisation()
        vis.table = pd.DataFrame(columns=["artist_name", "mins_played"])
        fig, ax = plt.subplots()
        vis.top_artists_chart(ax)
        plt.close(fig)

    def test_top_tracks_chart_with_data(self):
        vis = Visualisation()
        vis.process_data(self.sample_df)
        fig, ax = plt.subplots()
        vis.top_tracks_chart(ax)
        plt.close(fig)

    def test_monthly_time_spent_with_data(self):
        vis = Visualisation()
        vis.process_data(self.sample_df)
        fig, ax = plt.subplots()
        vis.monthly_time_spent(ax)
        plt.close(fig)

    def test_avg_daily_minutes_chart_with_data(self):
        vis = Visualisation()
        vis.process_data(self.sample_df)
        fig, ax = plt.subplots()
        vis.avg_daily_minutes_chart(ax)
        plt.close(fig)

    def test_charts_axis_none(self):
        vis = Visualisation()
        vis.process_data(self.sample_df)
        with self.assertRaises(ValueError):
            vis.top_artists_chart(None)
        with self.assertRaises(ValueError):
            vis.top_tracks_chart(None)
        with self.assertRaises(ValueError):
            vis.monthly_time_spent(None)
        with self.assertRaises(ValueError):
            vis.avg_daily_minutes_chart(None)

if __name__ == "__main__":
    unittest.main() 