# Project Proposal

## Project Description
This project aims to predict the number of people playing computer games on the **Steam** platform at a given date and time. It further aims to predict the ranking of the most played games. The data will be collected using Steam API.

## Goals
- Build a prediction model to estimate the number of players playing different games based on historical player count data.  
- Identify factors that may influence results, such as:  
  - Whether it is a working day or weekend.  
  - Time of day (e.g., after work hours).  
  - Regional time zones. (Unfortunately can not be isolated)
  - Popularity of the game, but using top 20 games will reduce the variance hopefully.
  - Date since its release
- Collect hourly player count data for the top 20 games by number of players in a day from SteamDB, train the model, and use it to make predictions.  

## Data
- **Data Sources:** [SteamDB.info](https://steamdb.info) (uses Steam API).  
- **Collection Method:** Download csv files conatining user count per time from the website, scrapping other game specific features from the SteamDB.    
- **Frequency/Timeframe:** Hourly basis, 10minute basis for data from 10/14 to 10/20.  
- **Scope:** Focus on the top 20 games by player count in terms of current players on October 20th.
- **Name of Games:** Counter-Strike 2, Dota 2, PUBG: Battlegrounds, APEX Legends, Delta Force, Rust, NARAKA: BLADEPOINT, Banana, Bongo Cat, Stardew Valley, Megabonk, Marvel Rivals, Grand Theft Auto V, Warframe, Baldur's Gate 3, Hollow Knight: Silksong, Team Fortress 2, Dead by Daylight, DayZ, Call of Duty
- **Contents:**
- Game.csv that contains name of the game, indicator for clicker genre, release date, price
- Weekend.csv for 

## Data Cleaning
- Handle missing values and inconsistencies (e.g., promotions, updates, server shutdowns).  
- Standardize data formats (e.g., using UTC for datetime objects, consistent units).  
- Remove duplicates and ensure consistency across games.  

## Feature Extraction
- Features extracted:  
  - Date.  
  - Time of day.  
  - Player count.  
  - Game name (stored as name of csv).    
- Aggregated / engineered features such as rolling averages and moving trends.  
- Possible categorical features, such as genre or free-to-play vs. paid (noting potential bias).  

## Modeling Plan
We will experiment with several approaches, including:  
- Regression-based models.  
- Subject to change as we learn more advanced models.  

We will evaluate model performance and select the best one based on accuracy and interpretability.  

## Visualization Plan
- Line charts of number of players over time.  
- Comparative charts showing relationships between features (e.g., day of week vs. player count).  
- Interactive plots (optional), allowing users to input a game name and date/time to see predictions.  

## Test Plan
- **Training set:** Data from September 20th – October.  
- **Test set:** Reserve data starting from November 20th as a holdout.  
- Use **k-fold cross-validation** on the training set to tune models.  

## GitHub & Collaboration Plan
The repository will include:  
- `data/` for datasets (with `.gitignore` to exclude large/raw data).  
- `notebooks/` for exploration and analysis.  
- `src/` for reusable code.  
- `docs/` for documentation.  

Proposal and final results will be submitted through this GitHub repository.

## How to reproduce:
- run make setup in the terminal. Will create a virtual environment. 
- Then run .venv\Scripts\activate
- run make enable-widgets
- run make notebook. This will open up the notebook server.
