# -------------------------------------------------------------
# interactive_plot.py — event-driven refresh version
# -------------------------------------------------------------

import os
import pandas as pd
import plotly.graph_objs as go
import ipywidgets as widgets
from IPython.display import display
import datetime
import numpy as np

# -------------------------------------------------------------
# Configuration
# -------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "../data"))

# Load CSV list
csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
if not csv_files:
    raise FileNotFoundError(f"No CSV files found in {DATA_DIR}")

# -------------------------------------------------------------
# Create widgets
# -------------------------------------------------------------
game_selector = widgets.Dropdown(
    options=csv_files,
    value=csv_files[0],
    description="Select Game:",
    style={"description_width": "initial"},
    layout=widgets.Layout(width="400px"),
)

# -------------------------------------------------------------
# Load initial dataset
# -------------------------------------------------------------
year = 2025
path = os.path.join(DATA_DIR, game_selector.value)
df = pd.read_csv(path)
year = 2025

df["date"] = df["date"].astype(str).str.strip()
df["time"] = df["time"].astype(str).str.strip()

# Combine date and time cleanly with fixed year
df["datetime_str"] = f"{year}-" + df["date"] + " " + df["time"]

# ✅ Convert explicitly to datetime dtype
df["datetime"] = pd.to_datetime(df["datetime_str"], errors="coerce", format="%Y-%m-%d %H:%M:%S")

# ✅ Enforce pandas datetime64[ns] type (critical)
df["datetime"] = pd.to_datetime(df["datetime"], utc=False)

df = df.dropna(subset=["datetime"])

# -------------------------------------------------------------
# Create FigureWidget
# -------------------------------------------------------------
g = go.FigureWidget(
    data=[go.Scatter(
        x=(df["datetime"].dt.to_pydatetime().tolist()),
        y=df["players"],
        mode="lines",
        line=dict(color="royalblue"),
        name=game_selector.value.replace(".csv", "")
    )]
)

g.update_layout(
    title=f"Player Count Over Time — {game_selector.value.replace('.csv', '')}",
    xaxis_title="Time",
    yaxis_title="Number of Players",
    template="plotly_white",
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(step="all", label="All")
            ])
        ),
        rangeslider_visible=False
    ),
    title_x=0.5
)

# Hide year in axis labels
g.update_xaxes(
    tickformat="%b %d",
    showline=True,
    ticks="outside"
)

# -------------------------------------------------------------
# Validation
# -------------------------------------------------------------
def validate():
    return game_selector.value in csv_files

# -------------------------------------------------------------
# Callback — updates figure dynamically
# -------------------------------------------------------------
def response(change):
    if validate():
        game_file = game_selector.value
        path = os.path.join(DATA_DIR, game_file)
        year = 2025

        # ✅ Load CSV before processing
        temp_df = pd.read_csv(path)

# Ensure date/time are strings
        temp_df["date"] = temp_df["date"].astype(str).str.strip()
        temp_df["time"] = temp_df["time"].astype(str).str.strip()

# Combine date and time cleanly with fixed year
        temp_df["datetime_str"] = f"{year}-" + temp_df["date"] + " " + temp_df["time"]

# ✅ Convert explicitly to datetime dtype
        temp_df["datetime"] = pd.to_datetime(temp_df["datetime_str"], errors="coerce", format="%Y-%m-%d %H:%M:%S")

# ✅ Enforce pandas datetime64[ns] type (critical)
        temp_df["datetime"] = pd.to_datetime(temp_df["datetime"], utc=False)

        temp_df = temp_df.dropna(subset=["datetime"])

        with g.batch_update():
            g.data[0].x = np.array(temp_df["datetime"].dt.to_pydatetime().tolist())
            g.data[0].y = temp_df["players"]
            g.data[0].name = game_file.replace(".csv", "")
            g.layout.title = f"Player Count Over Time — {game_file.replace('.csv', '')}"
    else:
        with g.batch_update():
            g.layout.title = "⚠️ Invalid selection — please choose a valid game"

# -------------------------------------------------------------
# Link widget to callback
# -------------------------------------------------------------
game_selector.observe(response, names="value")

# -------------------------------------------------------------
# Display
# -------------------------------------------------------------
ui = widgets.VBox([game_selector, g])
display(ui)
