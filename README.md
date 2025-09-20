# Project Proposal

## Project Description
This project aims to predict the number of people playing computer games on the **Steam** platform at a given date and time. It further aims to predict the ranking of the most played games. The data will be collected from SteamDB, which displays data from the official Steam API.

## Goals
- Build a prediction model to estimate the number of players playing different games based on historical player count data.  
- Identify factors that may influence results, such as:  
  - Whether it is a working day or weekend.  
  - Time of day (e.g., after work hours).  
  - Regional time zones.  
- Collect hourly player count data for the top 20 games from SteamDB, train the model, and use it to make predictions.  

## Data Collection
- **Data Sources:** [SteamDB.info](https://steamdb.info) (uses Steam API).  
- **Collection Method:** Web scraping from the SteamDB website.  
- **Frequency/Timeframe:** Hourly basis.  
- **Scope:** Focus on the top 20 games in terms of current players.  

## Data Cleaning
- Handle missing values and inconsistencies (e.g., promotions, updates, server shutdowns).  
- Standardize data formats (e.g., datetime objects, consistent units).  
- Remove duplicates and ensure consistency across games.  

## Feature Extraction
- Examples of features to extract:  
  - Day of week.  
  - Time of day.  
  - Player count.  
  - Game name.  
  - Game age (time since release).  
- Aggregated / engineered features such as rolling averages and moving trends.  
- Possible categorical features, such as genre or free-to-play vs. paid (noting potential bias).  

## Modeling Plan
We will experiment with several approaches, including:  
- Regression-based models.  
- Subject to change as we learn more advanced models (e.g., time series forecasting or tree-based models).  

We will evaluate model performance and select the best one based on accuracy and interpretability.  

## Visualization Plan
- Line charts of number of players over time.  
- Comparative charts showing relationships between features (e.g., day of week vs. player count).  
- Interactive plots (optional), allowing users to input a game name and date/time to see predictions.  

## Test Plan
- **Training set:** Data from September–October.  
- **Test set:** Reserve data from November as a holdout.  
- Use **k-fold cross-validation** on the training set to tune models.  

## GitHub & Collaboration Plan
The repository will include:  
- `data/` for datasets (with `.gitignore` to exclude large/raw data).  
- `notebooks/` for exploration and analysis.  
- `src/` for reusable code.  
- `docs/` for documentation.  

Proposal and final results will be submitted through this GitHub repository.
