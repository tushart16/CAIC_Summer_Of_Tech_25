# 🚀 CAIC Summer of Technology 2025 
## 🧠 Machine Learning: Week 1  
### 🔍 Problem Understanding, Dataset Familiarization & Exploratory Data Analysis (EDA)  

---

## 🗒 Problem Statement Recap: Behavior Simulation

Welcome to Week 1! 🎉

Our goal is to simulate *user engagement behavior* on Twitter. Specifically, we are trying to *predict the number of likes* a tweet will receive, given its metadata:

> *Inputs*:  
- Date and Time of posting  
- Tweet Text  
- Media Links  
- Company & Username  

> *Output*:  
- Predicted number of Likes

This model will help *digital marketers* evaluate the potential impact of their content and optimize what they post and when they post it.

---

## 📦 Dataset Details

We are given a dataset of *~300,000 tweets* from verified brand handles, with attributes:
- date (Timestamp)
- content (Tweet Text)
- username
- media (Image/Video URLs)
- company
- likes (Target variable)

🧪 The test dataset is split into:
- Tweets from *unseen brands*
- Tweets from *unseen time periods*

📁 *Links*:  
- [Train Data Sheet](https://docs.google.com/spreadsheets/d/1JcESl7qCCBvS6xpWMZplhCXunvmkcNU_)  

---

## 🧰 Week 1 Plan: Step-by-Step Guide

### ✅ 1. Setup Your ML Environment

We recommend using *Google Colab* for this assignment:
- No installation required
- Free GPU and TPU
- Easy collaboration and notebook sharing

🔗 [Colab Setup Guide (Playlist)](https://www.youtube.com/playlist?list=PLjVLYmrlmjGcV3YFqPy5V2ZvJ1XuzvFiu)

Optional: Use local Jupyter Notebooks if you're comfortable.

---

### ✅ 2. Load and View the Data

Steps to follow in your notebook:

python
import pandas as pd

# Load the dataset
df = pd.read_csv("path_to_train_data.csv")  # Replace with your path or mount Google Drive

# View dataset shape
print("Shape of dataset:", df.shape)

# Peek at the data
df.head()

# Data types and missing values
df.info()
df.isnull().sum()


---

### 🧹 3. Data Cleaning & Preprocessing

#### 🧼 Handle Missing Values

python
# Drop rows where crucial info is missing
df.dropna(subset=['content', 'username', 'company', 'likes'], inplace=True)

# Fill media nulls with 'no_media'
df['media'].fillna('no_media', inplace=True)

# Add a binary flag for media presence
df['has_media'] = df['media'].apply(lambda x: x != 'no_media')


#### 🧼 Remove Duplicates

python
df.drop_duplicates(inplace=True)


#### 🧼 Clean Text Columns

python
df['content'] = df['content'].astype(str).str.strip().str.lower()


#### 🧼 Convert Timestamp to Datetime

python
df['datetime'] = pd.to_datetime(df['date'], errors='coerce')


---

### 📊 4. Exploratory Data Analysis (EDA)

This is where we understand *data patterns* and uncover *feature importance* for future modeling.

---

#### 🎯 Target Variable Analysis: likes

python
import seaborn as sns
import matplotlib.pyplot as plt

sns.histplot(df['likes'], kde=True)
plt.title("Distribution of Likes")


python
sns.boxplot(x=df['likes'])


python
import numpy as np
df['log_likes'] = np.log1p(df['likes'])


---

#### 🧠 Categorical Analysis

python
# Media impact
sns.boxplot(x='has_media', y='likes', data=df)

# Average likes per company
df.groupby('company')['likes'].mean().sort_values(ascending=False).head(10).plot(kind='barh')


---

#### ⏰ Temporal Patterns

python
df['hour'] = df['datetime'].dt.hour
df['day_of_week'] = df['datetime'].dt.day_name()

# Likes by hour
sns.barplot(x='hour', y='likes', data=df)

# Likes by day
sns.boxplot(x='day_of_week', y='likes', data=df)


---

#### 📏 Text Feature Engineering

python
# Length-based features
df['word_count'] = df['content'].apply(lambda x: len(str(x).split()))
df['char_count'] = df['content'].apply(lambda x: len(str(x)))

# Plot
sns.scatterplot(x='word_count', y='likes', data=df)


---

#### 💬 Sentiment Analysis (Optional)

python
from textblob import TextBlob

df['sentiment'] = df['content'].apply(lambda x: TextBlob(x).sentiment.polarity)
sns.scatterplot(x='sentiment', y='likes', data=df)


---

## 🧠 Bonus EDA Ideas

| Technique | Why Use It |
|----------|------------|
| Correlation Heatmap | Understand numeric relationships |
| t-SNE / UMAP | Reduce high-dim features for visualization |
| Word Clouds | Spot common high-engagement terms |
| TF-IDF Vectorization | Use for clustering/content analysis |
| N-gram analysis | Phrase patterns in high-like tweets |
| Clustering with KMeans | Discover content themes |
| Time Series Decomposition | Engagement trends over time |
| Named Entity Recognition | Extract brands/places/products mentioned |

---

## 📚 Useful Resources

### 🧪 EDA & Data Cleaning  
- [Kaggle: EDA Course](https://www.kaggle.com/learn/data-cleaning)  
- [Practical Pandas](https://realpython.com/pandas-python-explore-dataset/)  
- [Seaborn Gallery](https://seaborn.pydata.org/examples/index.html)

### 🏗 Feature Engineering  
- [Feature Engineering Guide](https://www.kaggle.com/learn/feature-engineering)  

---

## ✅ Week 1 Deliverables

1. 📒 A Colab Notebook that includes:
   - Data Loading
   - Data Cleaning & Feature Preparation
   - EDA Visualizations and Feature Insights
2. ✍ Summary of observations and potential features for modeling

---

## 🔮 What’s Next?

In *Week 2*, we’ll dive into building models that predict likes using features we explored in this week.

Stay curious, and keep exploring! 💡  
“Behind every great model is a great EDA.”
