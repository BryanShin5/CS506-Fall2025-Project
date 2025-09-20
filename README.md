# Project Proposal

## Project Description
[This Project aims to predict the number of people playing computer games using STEAM platform at a given date and time period, then further aims to predict the ranking of most played games. The data will be collected from STEAM.]

## Goals
- [Build a prediction model to predict the number of players playing different games based on the past data of number of players]
- [Factors that may affect result: Whether it is a working day, time within a day that work ends, Regional time.]
- [Gather data of number of players every hour from Steam DB, train the model, predict using the model.]

## Data Collection
- **Data Sources:** [STEAMDB.info displayes data from STEAM API.]
- **Collection Method:** [Scrapping from STEAMDB website.]
- **Frequency/Timeframe:** [Hourly basis]
- [Will collect data from top 20 games in terms of current players]

## Data Cleaning
- Handle missing values and inconsistencies (e.g., Promotions, updates, server shutdown, etc).   
- Standardize data formats (e.g., date/time, units).   

## Feature Extraction
- Examples of features to extract:  
  - [Day of week, time of day, player count, name of the game, how old the game is.]  
  - [Aggregated/engineered features like rolling averages.]
  - [Possible categorization of the game (may be biased)]

## Modeling Plan
We will experiment with several approaches, including:  
- [Regression.]   
- [Subject to change as we learn more models]  

We will evaluate model performance and select the best one based on accuracy and interpretability.  

## Visualization Plan
- Line chart of number of player over time.  
- Different chart with features that may possibly affect the number of players.   
- Maybe an interactive plot with an option to plug in name of game and date / time.
## Test Plan
- training set will consist of data from September to October 
- Reserve **Data from November** as a holdout test set.  
- Use **k-fold cross-validation** on the training set to tune models.  

## GitHub & Collaboration Plan
- Repo will include:  
  - `data/` for datasets (with `.gitignore` for large/raw data).  
  - `notebooks/` for exploration and analysis.  
  - `src/` for reusable code.  
  - `docs/` for documentation.    
- Submit proposal and final results through this GitHub repo.  
