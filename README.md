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

## Data Cleaning
- Handle missing values and inconsistencies.  
- Normalize/standardize data formats (e.g., date/time, units).  
- Merge multiple sources into one dataset.  

## Feature Extraction
- Examples of features to extract:  
  - [Day of week, time of day, weather conditions, holidays, etc.]  
  - [Aggregated/engineered features like rolling averages.]  

## Modeling Plan
We will experiment with several approaches, including:  
- [Linear regression / logistic regression.]  
- [Decision trees or random forests.]  
- [Gradient boosting methods such as XGBoost.]  
- [Optional: Deep learning if time permits.]  

We will evaluate model performance and select the best one based on accuracy and interpretability.  

## Visualization Plan
- Exploratory plots (scatterplots, histograms, correlation heatmaps).  
- Time series plots to observe trends.  
- Feature importance plots (for tree-based models).  
- [Optional: Interactive plots using Plotly or Altair.]  

## Test Plan
- Reserve **20% of the dataset** as a holdout test set.  
- Use **k-fold cross-validation** on the training set to tune models.  
- Compare metrics such as [RMSE, accuracy, F1-score depending on the problem type].  

## GitHub & Collaboration Plan
- Repo will include:  
  - `data/` for datasets (with `.gitignore` for large/raw data).  
  - `notebooks/` for exploration and analysis.  
  - `src/` for reusable code.  
  - `docs/` for documentation.  
- Use **issues** and **pull requests** for collaboration and code review.  
- Submit proposal and final results through this GitHub repo.  
