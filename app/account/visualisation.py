import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as pyplot


class Visualisation:
    """
    A class to handle Spotify data visualisation.

    This class processes Spotify streaming history data and creates
    various visualisations including top artists, top tracks,
    monthly listening time, and daily listening patterns.

    Attributes:
        table (pd.DataFrame): Processed Spotify streaming data

    Methods:
        process_data(df): Process raw DataFrame into required format
        top_artists_chart(axis): Create top 5 artists visualisation
        top_tracks_chart(axis): Create top 5 tracks visualisation
        monthly_time_spent(axis): Create monthly listening time visualisation
        avg_daily_minutes_chart(axis): Create daily listening pattern visualisation
    """

    def process_data(self, df):
        """Process DataFrame directly instead of reading from file"""
        try:
            # Check if required columns exist
            required_columns = [
                "ts",
                "ms_played",
                "master_metadata_track_name",
                "master_metadata_album_artist_name",
            ]
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")

            table = df[
                [
                    "ts",
                    "ms_played",
                    "master_metadata_track_name",
                    "master_metadata_album_artist_name",
                ]
            ]

            # Rename columns
            table = table.rename(
                columns={
                    "ts": "timestamp",
                    "master_metadata_track_name": "track_name",
                    "master_metadata_album_artist_name": "artist_name",
                }
            )

            # Convert and create new columns
            table["timestamp"] = pd.to_datetime(table["timestamp"])
            table["mins_played"] = table["ms_played"].apply(
                lambda x: round(x / 60000, 4)
            )
            table["hours_played"] = table["ms_played"].apply(
                lambda x: round(x / 3600000, 4)
            )
            table["time"] = table["timestamp"].dt.time
            table["hour"] = table["timestamp"].dt.hour

            self.table = table
            return self.table

        except Exception as e:
            raise Exception(f"Error processing data: {e}")

    def top_artists_chart(self, axis):
        """Create top 5 artists chart"""
        if axis is None:
            raise ValueError("Axis parameter cannot be None")

        # Handle empty data
        if self.table.empty:
            axis.text(
                0.5,
                0.5,
                "No data available",
                horizontalalignment="center",
                verticalalignment="center",
            )
            return

        artists_played = self.table.groupby("artist_name")["mins_played"].sum()
        top_five_artists = artists_played.sort_values(ascending=False).head(5)

        bars = axis.bar(
            top_five_artists.index,
            top_five_artists.values,
            color="steelblue",
            width=0.5,
        )

        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            axis.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{int(height)}",
                ha="center",
                va="bottom",
            )

        axis.set_title("Top 5 Artists Played", fontsize=14, fontweight="bold")
        axis.set_xlabel("Artist Name", fontsize=12)
        axis.set_ylabel("Minutes Played", fontsize=12)
        axis.tick_params(axis="x", rotation=20, labelsize=9)

    def top_tracks_chart(self, axis):
        """Create top 5 tracks chart"""
        if axis is None:
            raise ValueError("Axis parameter cannot be None")

        if self.table.empty:
            axis.text(
                0.5,
                0.5,
                "No data available",
                horizontalalignment="center",
                verticalalignment="center",
            )
            return

        tracks_played = self.table.groupby("track_name")["mins_played"].sum()
        top_five_tracks = tracks_played.sort_values(ascending=False).head(5)

        bars = axis.bar(
            top_five_tracks.index, top_five_tracks.values, color="indianred", width=0.5
        )

        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            axis.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{int(height)}",
                ha="center",
                va="bottom",
            )

        axis.set_title("Top 5 Tracks Played", fontsize=14, fontweight="bold")
        axis.set_xlabel("Track Name", fontsize=12)
        axis.set_ylabel("Minutes Played", fontsize=12)
        axis.tick_params(axis="x", rotation=30, labelsize=9)

    def monthly_time_spent(self, axis):
        """Create monthly listening time chart"""
        if axis is None:
            raise ValueError("Axis parameter cannot be None")

        if self.table.empty:
            axis.text(
                0.5,
                0.5,
                "No data available",
                horizontalalignment="center",
                verticalalignment="center",
            )
            return

        self.table["year_month"] = self.table["timestamp"].dt.tz_localize(None).dt.to_period("M").astype(str)

        monthly_play = self.table.groupby("year_month")["hours_played"].sum()

        line = axis.plot(
            monthly_play.index, monthly_play.values, color="darkslateblue", marker="o"
        )

        # Add value labels on points
        for x, y in zip(monthly_play.index, monthly_play.values):
            axis.text(x, y+0.25, f"{round(y, 1)}", ha="center", va="bottom"
                      ,bbox=dict(boxstyle='roundtooth',facecolor='lightyellow',edgecolor='black', pad=0.1))

        axis.set_title(
            "Monthly Listening Time (in Hours)", fontsize=14, fontweight="bold"
        )
        axis.set_xlabel("Month", fontsize=12)
        axis.set_ylabel("Hours Played", fontsize=12)
        axis.tick_params(axis="x", rotation=45)
        axis.grid(True, linestyle="--", alpha=0.5)

    def avg_daily_minutes_chart(self, axis):
        """Create average daily minutes chart"""
        if axis is None:
            raise ValueError("Axis parameter cannot be None")

        if self.table.empty:
            axis.text(
                0.5,
                0.5,
                "No data available",
                horizontalalignment="center",
                verticalalignment="center",
            )
            return

        self.table["hour"] = self.table["timestamp"].dt.hour
        self.table["date"] = self.table["timestamp"].dt.date

        daily_hourly = (
            self.table.groupby(["date", "hour"])["mins_played"].sum().reset_index()
        )
        avg_per_hour = daily_hourly.groupby("hour")["mins_played"].mean()

        line = axis.plot(
            avg_per_hour.index, avg_per_hour.values, color="seagreen", marker="o"
        )

        # Add value labels on points
        for x, y in zip(avg_per_hour.index, avg_per_hour.values):
            axis.text(x, y+0.25 , f"{round(y, 1)}", ha="center", va="bottom"
                      ,bbox=dict(boxstyle='roundtooth',facecolor='yellow',edgecolor='black', pad=0.1))

        axis.set_title(
            "Average Listening Time Every Hour", fontsize=14, fontweight="bold"
        )
        axis.set_xlabel("Hour of Day", fontsize=12)
        axis.set_ylabel("Average Minutes Played", fontsize=12)
        axis.set_xticks(range(0, 24))
        axis.grid(True, linestyle="--", alpha=0.5)

    def create_dashboard(self, output_buffer):
        """Create the complete dashboard and save to buffer"""
        try:
            figure, axis = pyplot.subplots(2, 2, figsize=(14, 10), facecolor="white")
            figure.suptitle("Personalised Spotify Listening Dashboard", fontsize=14, fontweight='bold')
            axis = axis.flatten()

            self.top_artists_chart(axis[0])
            self.top_tracks_chart(axis[1])
            self.monthly_time_spent(axis[2])
            self.avg_daily_minutes_chart(axis[3])

            pyplot.tight_layout()

            # Save to buffer
            pyplot.savefig(output_buffer, format="png", bbox_inches="tight", dpi=100)
            pyplot.close(figure)  # Clean up

            output_buffer.seek(0)

        except Exception as e:
            pyplot.close("all")  # Clean up in case of error
            raise Exception(f"Error creating dashboard: {e}")
