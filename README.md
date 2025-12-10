# Midterm Report
https://youtu.be/5TNirlYUUzY
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

## How to reproduce:
- run make setup in the terminal. Will create a virtual environment. 
- Then run .venv\Scripts\activate
- run make enable-widgets
- run make notebook. This will open up the notebook server.

## GitHub Plan
The repository will include:  
- `data/` for datasets (with `.gitignore` to exclude large/raw data).  
- `src/` for reusable code.  
- `docs/` for documentation.  

Proposal and final results will be submitted through this GitHub repository.
## Data
- **Data Sources:** [SteamDB.info](https://steamdb.info) (uses Steam API).  
- **Collection Method:** Download csv files conatining user count per time from the website, scrapping other game specific features from the SteamDB.    
- **Frequency/Timeframe:** Hourly basis, 10minute basis for data from 10/14 to 10/20.  
- **Scope:** Focus on the top 20 games by player count in terms of current players on October 20th.
- **Name of Games:** Counter-Strike 2, Dota 2, PUBG: Battlegrounds, APEX Legends, Delta Force, Rust, NARAKA: BLADEPOINT, Banana, Bongo Cat, Stardew Valley, Megabonk, Marvel Rivals, Grand Theft Auto V, Warframe, Baldur's Gate 3, Hollow Knight: Silksong, Team Fortress 2, Dead by Daylight, DayZ, Call of Duty
- **Contents:**
  - Game.csv containing game related features
  - Weekend.csv maps dates to indicator variable
  - 20 csv files whose name is the name of the game, contains hourly player count from 09/20-10/20

## Data Cleaning:
- Using UTC for any time related data
- Cropped data before September 20th to focus on recent month as a training set.

## Feature Extraction
- Features extracted for Game.csv:  
  - Name of Game.  
  - Genre(1 if it is a clicker game, 0 otherwise). Specifically chosen Clicker games since they encourage player to turn the game on even if they are Idle, contributing to player count.  
  - Release date.  
  - Price in US Dollar, 0 if available free.
  - Sin / Cos of day and hour, capturing repetitive trend of the data  
- Features extracted for Weekend.csv:
  - Date
  - Indicator variable(1 if Friday or Weekend, 0 Otherwise). Holidays are not accounted due to global distribution of players, may bias towards certain regions.  
- Features extracted for GameName.csv:
  - Date (MM/DD)
  - Time (HH/MM/SS)
  - Player Count

## Modeling Plan
We will experiment with several approaches, including:  
- Regression-based models.  
- Subject to change as we learn more advanced models.  

We will evaluate model performance and select the best one based on accuracy and interpretability.  
Yet the linear regression model seems pretty promising by far. 

## Visualization of the data
- Visualization of Hourly player counts data is available at /notebook/Interactive_Plot.ipynb
- Any code that is used in the notebook is present in /src.

## Test Plan
- **Training set:** Data from September 20th – October 20th.  
- **Test set:** Reserve data starting from October 20th as a holdout.
- **Evaluation method**: R squared value

## Observations: 
- The shape of the player count curve repeated in a daily basis, yet not in clicker games like Banana and Bongo Cat. The curve was totally unpredictable there, which is a reason to note whether it is a clicker game or not.
- For games released earlier in time, the player count curve was stable than games that were recently released.
- When not including hour sin and cos, changing the hour of the time I want to predict did not affect the result at all.
- When included missing sin and cos, the line was lot closer to a linear plot.

## Plans:
- Fit more data, compare prediction accuracy and possibly identify more factors that may contribute to player count.
- Seems like date since release does not affect the model much, need a way to modify that feature to capture growing trend for recently released games like Megabonk.
- Return a ranking amongst those 20 games according to player count. 
