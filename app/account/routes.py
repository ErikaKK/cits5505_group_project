from app.account import bp
from flask import Flask, render_template
from flask_login import current_user, login_required

import pandas as pd
import json
import matplotlib.pyplot as pyplot

class Visualisation:
    def visualise_data(self, json_file_location):
        file = open(json_file_location, 'r', encoding='utf-8')
        columns = json.load(file)
        table = pd.DataFrame(columns)
        table = table[[
            'ts',
            'ms_played',
            'master_metadata_track_name',
            'master_metadata_album_artist_name'
        ]]
        table = table.rename(columns={
            'ts': 'timestamp',
            'master_metadata_track_name': 'track_name',
            'master_metadata_album_artist_name': 'artist_name'
        })
        table['timestamp'] = pd.to_datetime(table['timestamp'])
        table['mins_played'] = table['ms_played'].apply(lambda x: round(x / 60000, 4))
        table['hours_played'] = table['ms_played'].apply(lambda x: round(x / 3600000, 4))
        table['time'] = table['timestamp'].dt.time
        table['hour'] = table['timestamp'].dt.hour

        self.table = table
        self.display_dashboard()

    def top_artists_chart(self, axis):
        artists_played = self.table.groupby('artist_name')['mins_played'].sum()
        top_five_artists = artists_played.sort_values(ascending=False).head(5)

        axis.bar(top_five_artists.index, top_five_artists.values, color='steelblue', width=0.5)
        axis.set_title('Top 5 Artists Played',fontsize=14, fontweight='bold')
        axis.set_xlabel('Minutes Played',fontsize=12)
        

    def top_tracks_chart(self, axis):
        tracks_played = self.table.groupby('track_name')['mins_played'].sum()
        top_five_tracks = tracks_played.sort_values(ascending=False).head(5)

        axis.bar(top_five_tracks.index, top_five_tracks.values, color='indianred', width=0.5)
        axis.set_title('Top 5 Tracks Played', fontsize=14, fontweight='bold')
        axis.set_xlabel('Minutes Played',fontsize=12)
        axis.tick_params(axis='x', rotation=30, labelsize=9)

    def monthly_time_spent(self, axis):
        self.table['year_month'] = self.table['timestamp'].dt.to_period('M').astype(str)
        monthly_play = self.table.groupby('year_month')['hours_played'].sum()

        axis.plot(monthly_play.index, monthly_play.values, color='mediumslateblue', marker='o')
        axis.set_title('Monthly Listening Time (in Hours)',fontsize=14, fontweight='bold')
        axis.set_xlabel('Month',fontsize=12)
        axis.set_ylabel('Hours Played',fontsize=12)
        axis.tick_params(axis='x', rotation=45)
        axis.grid(True, linestyle='--', alpha=0.5)

    def avg_daily_minutes_chart(self, axis):
        self.table['hour'] = self.table['timestamp'].dt.hour
        self.table['date'] = self.table['timestamp'].dt.date

        daily_hourly = self.table.groupby(['date', 'hour'])['mins_played'].sum().reset_index()
        avg_per_hour = daily_hourly.groupby('hour')['mins_played'].mean()

        axis.plot(avg_per_hour.index, avg_per_hour.values, color='seagreen', marker='o')
        axis.set_title('Average Listening Time Per Hour',fontsize=14, fontweight='bold')
        axis.set_xlabel('Hour of Day',fontsize=12)
        axis.set_ylabel('Average Minutes Played',fontsize=12)
        axis.set_xticks(range(0, 24))
        axis.grid(True, linestyle='--', alpha=0.5)

    def display_dashboard(self):
        figure, axis = pyplot.subplots(2, 2, figsize=(14, 10), facecolor='white')
        axis = axis.flatten()

        self.top_artists_chart(axis[0])
        self.top_tracks_chart(axis[1])
        self.monthly_time_spent(axis[2])
        self.avg_daily_minutes_chart(axis[3])

        pyplot.tight_layout()
        pyplot.show()


@bp.route("/")
@bp.route("/profile")
@login_required
def profile():
    return render_template(
        "/account/profile.html", title="My Account", login=current_user.is_authenticated
    )


@bp.route("/v")