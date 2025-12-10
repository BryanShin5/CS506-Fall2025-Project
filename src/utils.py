import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import matplotlib.dates as mdates
import numpy as np
import os
from sklearn.linear_model import LinearRegression


def extract_daily_max_dict(csv_path: str):
    """
    Returns a dictionary mapping each date to (peak_time, max_players)
    from a given CSV file with columns: date, time, players
    """
    # Load the CSV
    df = pd.read_csv(csv_path)

    # Validate structure
    expected_cols = {"date", "time", "players"}
    if not expected_cols.issubset(df.columns):
        raise ValueError(f"CSV must include columns {expected_cols}")

    # Convert players to numeric
    df["players"] = pd.to_numeric(df["players"], errors="coerce")

    # Find index of max per date
    idx = df.groupby("date")["players"].idxmax()

    # Extract the corresponding rows
    daily_max = df.loc[idx, ["date", "time", "players"]].reset_index(drop=True)

    # Build dictionary {date: (time, players)}
    daily_max_dict = {
        row["date"]: (row["time"], int(row["players"]))
        for _, row in daily_max.iterrows()
    }

    return daily_max_dict

def plot_daily_max(daily_peaks, weekend_csv_path, year=2025):
    """
    Plots daily max player count, coloring weekends (Fri–Sun) differently.

    Parameters
    ----------
    daily_peaks : dict[str, tuple[str, int]]
        e.g. {'09-20': ('19:00:00', 31245), ...}
    weekend_csv_path : str
        Path to weekend.csv
    year : int
        Year prefix for date strings (default=2025)
    """
    import pandas as pd

    # --- Load weekend info ---
    weekend_df = pd.read_csv(weekend_csv_path)
    weekend_df["date"] = pd.to_datetime(weekend_df["date"])
    weekend_map = {d.date(): int(flag) for d, flag in zip(weekend_df["date"], weekend_df["is_weekend"])}

    # --- Prepare data from dictionary ---
    dates = [datetime.strptime(f"{year}-{d}", "%Y-%m-%d") for d in daily_peaks.keys()]
    counts = [count for _, count in daily_peaks.values()]

    # --- Assign colors based on weekend ---
    colors = ["tomato" if weekend_map.get(dt.date(), 0) == 1 else "royalblue" for dt in dates]

    # --- Sort by date for smooth plotting ---
    paired = sorted(zip(dates, counts, colors))
    dates, counts, colors = zip(*paired)

    # --- Plot ---
    plt.figure(figsize=(10, 5))
    for d, c, col in zip(dates, counts, colors):
        plt.scatter(d, c, color=col, s=80)
    plt.plot(dates, counts, color="gray", alpha=0.4, linewidth=1)

    plt.title("Daily Peak Player Count (Weekends in Red)")
    plt.xlabel("Date")
    plt.ylabel("Max Player Count")
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))

    # --- Legend ---
    plt.scatter([], [], color="royalblue", label="Weekday", s=80)
    plt.scatter([], [], color="tomato", label="Weekend", s=80)
    plt.legend()

    plt.tight_layout()
    plt.show()
def plot_peak_time_with_weekends(daily_peaks, weekend_csv_path, year=2025):
    """
    Plots the time of day when the daily peak occurred, colored by weekend vs weekday.

    Parameters:
        daily_peaks: dict[str, tuple[str, int]]
            e.g. {'09-20': ('19:00:00', 31245), ...}
        weekend_csv_path: str
            Path to weekend.csv file
        year: int
            Year to prepend to date (default 2025)
    """
    import pandas as pd

    # Load weekend data
    weekend_df = pd.read_csv(weekend_csv_path)
    weekend_df["date"] = pd.to_datetime(weekend_df["date"])
    weekend_map = {d.date(): int(flag) for d, flag in zip(weekend_df["date"], weekend_df["is_weekend"])}

    # Convert dictionary into lists
    date_objs = [datetime.strptime(f"{year}-{d}", "%Y-%m-%d") for d in daily_peaks.keys()]
    time_objs = [datetime.strptime(t, "%H:%M:%S").time() for t, _ in daily_peaks.values()]
    time_as_dt = [datetime.combine(datetime(2025, 1, 1).date(), t) for t in time_objs]

    # Determine color (weekend or weekday)
    colors = ["tomato" if weekend_map.get(date.date(), 0) == 1 else "royalblue" for date in date_objs]

    # Sort everything by date
    paired = sorted(zip(date_objs, time_as_dt, colors))
    date_objs, time_as_dt, colors = zip(*paired)

    # Plot
    plt.figure(figsize=(10, 5))
    for d, t, c in zip(date_objs, time_as_dt, colors):
        plt.scatter(d, t, color=c, s=80)

    # Lines for continuity
    plt.plot(date_objs, time_as_dt, color="gray", alpha=0.4, linewidth=1)

    plt.title("Time of Peak Player Activity Each Day (Weekends in Red)")
    plt.xlabel("Date")
    plt.ylabel("Time of Peak (UTC)")
    plt.grid(True)

    # Format y-axis to display hours
    plt.gca().yaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

    # Add legend
    plt.scatter([], [], color="royalblue", label="Weekday", s=80)
    plt.scatter([], [], color="tomato", label="Weekend", s=80)
    plt.legend()

    plt.tight_layout()
    plt.show()

def prepare_features(daily_df, weekend_csv, game_csv):
    """
    Combines daily player data with weekend indicators and game metadata.

    Parameters
    ----------
    daily_df : pd.DataFrame
        Must include ['game_name', 'date', 'max_count']
    weekend_csv : str
        Path to weekend.csv (columns: ['date', 'is_weekend'])
    game_csv : str
        Path to game.csv (columns: ['game_name', 'genre', 'release_date', 'price_usd'])

    Returns
    -------
    pd.DataFrame
        Combined DataFrame ready for regression.
    """

    # --- Load data ---
    weekend_df = pd.read_csv(weekend_csv, parse_dates=["date"])
    game_df = pd.read_csv(game_csv)

    # --- Clean metadata ---
    game_df["price_usd"] = pd.to_numeric(game_df["price_usd"], errors="coerce").fillna(0)
    game_df["release_date"] = pd.to_datetime(game_df["release_date"], errors="coerce")
    

    # --- Merge weekend and game info ---
    df = pd.merge(daily_df, weekend_df, on="date", how="left")
    df = pd.merge(df, game_df, on="game_name", how="left")
    df["days_since_release"] = (df["date"] - df["release_date"]).dt.days.clip(lower=0)
    # --- Encode time-based features ---
    df["day_index"] = (df["date"] - df["date"].min()).dt.days
    df["day_of_week"] = df["date"].dt.dayofweek
    df["dow_sin"] = np.sin(2 * np.pi * df["day_of_week"] / 7)
    df["dow_cos"] = np.cos(2 * np.pi * df["day_of_week"] / 7)

    # --- Encode genre (one-hot) ---
    df = pd.get_dummies(df, columns=["genre"], drop_first=True)

    # --- Fill weekend nulls and drop redundant columns ---
    df["is_weekend"] = df["is_weekend"].fillna(0).astype(int)
    df = df.drop(columns=["release_date"])

    return df

def fit_and_plot_regression(df):
    """
    Fit a linear regression model to training data and plot predicted vs actual values.
    Assumes df is the output of prepare_features().
    """

    # Drop non-numeric or irrelevant columns
    X = df.drop(columns=["game_name", "date", "max_count"])
    y = df["max_count"]

    # Fit the model
    model = LinearRegression()
    model.fit(X, y)

    # Predictions on the training set
    y_pred = model.predict(X)

    # Display coefficients
    print("Linear Regression Coefficients:")
    print("---------------------------------")
    for name, coef in zip(X.columns, model.coef_):
        print(f"{name:25s}: {coef:.4f}")
    print(f"\nIntercept: {model.intercept_:.4f}")

    # R² score (fit quality)
    r2 = model.score(X, y)
    print(f"\nR² (on training data): {r2:.3f}")

    # Plot actual vs predicted
    plt.figure(figsize=(8, 5))
    plt.scatter(y, y_pred, alpha=0.7, color="royalblue")
    plt.xlabel("Actual Max Player Count")
    plt.ylabel("Predicted Max Player Count")
    plt.title("Linear Regression Fit (Training Data)")
    plt.grid(True)
    plt.plot([y.min(), y.max()], [y.min(), y.max()], color="red", linestyle="--")
    plt.tight_layout()
    plt.show()

    return model

def prepare_all_points(game_files, weekend_csv, game_csv):
    """
    Merge timestamp-level player data with weekend and game metadata.
    Can handle a single file or a list of files.
    """

    # Allow single string input
    if isinstance(game_files, str):
        game_files = [game_files]

    weekend_df = pd.read_csv(weekend_csv, parse_dates=["date"])
    game_df = pd.read_csv(game_csv)
    game_df["price_usd"] = pd.to_numeric(game_df["price_usd"], errors="coerce").fillna(0)
    game_df["release_date"] = pd.to_datetime(game_df["release_date"], errors="coerce")

    all_data = []

    for path in game_files:
        game_name = os.path.splitext(os.path.basename(path))[0].replace("_test", "")
        df = pd.read_csv(path)

        # Format strings
        df["date"] = df["date"].astype(str).str.strip()
        df["time"] = df["time"].astype(str).str.strip()

        # Construct datetime
        df["datetime"] = pd.to_datetime(
            "2025-" + df["date"] + " " + df["time"],
            errors="coerce",
            format="%Y-%m-%d %H:%M:%S"
        )
        df = df.dropna(subset=["datetime", "players"])
        df["game_name"] = game_name

        # Normalize date type for merge
        df["date"] = pd.to_datetime("2025-" + df["date"], errors="coerce").dt.normalize()
        weekend_df["date"] = weekend_df["date"].dt.normalize()

        # Merge weekend info
        df = pd.merge(df, weekend_df, on="date", how="left")
        df["is_weekend"] = df["is_weekend"].fillna(0).astype(int)

        # Merge static metadata
        meta = game_df.loc[game_df["game_name"] == game_name]
        if meta.empty:
            continue
        meta = meta.iloc[0]
        df["genre"] = meta["genre"]
        df["price_usd"] = meta["price_usd"]
        df["release_date"] = meta["release_date"]

        # ✅ FIXED: Use .dt.days to extract integer days
        df["days_since_release"] = (df["datetime"] - meta["release_date"]).dt.days.clip(lower=0)

        # Time-based features
        df["hour"] = df["datetime"].dt.hour
        df["day_of_week"] = df["datetime"].dt.dayofweek
        df["dow_sin"] = np.sin(2 * np.pi * df["day_of_week"] / 7)
        df["dow_cos"] = np.cos(2 * np.pi * df["day_of_week"] / 7)
        df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
        df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)
        all_data.append(df)

    # Combine all data
    combined = pd.concat(all_data, ignore_index=True)
    combined = pd.get_dummies(combined, columns=["genre"], drop_first=True)

    # Optional: print summary
    print(f"Combined {len(combined):,} total data points from {len(game_files)} file(s).")

    return combined

def predict_player_count(model, game_name, target_datetime, game_csv, weekend_csv):
    """
    Predicts player count at a given datetime for a specific game using a trained linear regression model.

    Parameters
    ----------
    model : fitted LinearRegression
    game_name : str
        The name of the game (must exist in game_csv)
    target_datetime : datetime.datetime
        The target time to predict
    game_csv : str
        Path to game.csv (columns: game_name, genre, release_date, price_usd)
    weekend_csv : str
        Path to weekend.csv (columns: date, is_weekend)
    """

    # --- Load metadata ---
    game_df = pd.read_csv(game_csv)
    weekend_df = pd.read_csv(weekend_csv, parse_dates=["date"])

    meta = game_df.loc[game_df["game_name"] == game_name]
    if meta.empty:
        raise ValueError(f"Game '{game_name}' not found in {game_csv}")
    meta = meta.iloc[0]

    # --- Static info ---
    price_usd = float(meta["price_usd"])
    release_date = pd.to_datetime(meta["release_date"], errors="coerce")
    genre = meta["genre"]

    # --- Compute date/time features ---
    target_date = pd.to_datetime(target_datetime).normalize()
    is_weekend = int(weekend_df["date"].dt.normalize().eq(target_date).any() and 
                     weekend_df.loc[weekend_df["date"].dt.normalize().eq(target_date), "is_weekend"].iloc[0])

    days_since_release = max((target_datetime - release_date).days, 0)
    hour = target_datetime.hour
    hour_sin = np.sin(2 * np.pi * hour / 24)
    hour_cos = np.cos(2 * np.pi * hour / 24)
    day_of_week = target_datetime.weekday()
    dow_sin = np.sin(2 * np.pi * day_of_week / 7)
    dow_cos = np.cos(2 * np.pi * day_of_week / 7)
    
    # --- Construct feature DataFrame ---
    data = {
        "is_weekend": [is_weekend],
        "price_usd": [price_usd],
        "days_since_release": [days_since_release],
        "hour": [hour],
        "day_of_week": [day_of_week],
        "dow_sin": [dow_sin],
        "dow_cos": [dow_cos],
        "hour_sin": [hour_sin],
        "hour_cos": [hour_cos],
    }

    df_pred = pd.DataFrame(data)

    # --- Align columns (same order as training) ---
    df_pred = df_pred.reindex(columns=model.feature_names_in_, fill_value=0)

    # --- Predict ---
    predicted = model.predict(df_pred)[0]
    print(f"🎮 Predicted player count for {game_name} at {target_datetime}: {predicted:,.0f}")

    return predicted