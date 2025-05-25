
# 🤖 CAIC Summer of Tech 2025: ML+Dev Track

## Introduction

Welcome to the **Machine Learning + Development (ML+Dev)** track of the DevClub Summer of Code 2025!

This vertical is designed to teach you not just machine learning fundamentals, but also how to apply them to real-world scenarios. The goal is simple but powerful: **build ML-powered systems, and share them with the world**. You’ll go from raw data to a deployed application solving a real marketing problem — predicting and generating engaging content using machine learning.

## Why ML+Dev?

Machine Learning and Development together offer a unique opportunity to:
- **Bridge theory and practice**: Learn core ML concepts and build full-stack systems powered by them.
- **Solve real-world problems**: Use data to simulate behavior and generate creative content.
- **Think end-to-end**: Go from dataset → model → product → deployment.
- **Show your work**: Share your project with the world — open source it, write a devlog, or even host it online.

Whether you’re a data enthusiast, a developer curious about ML, or someone who loves building impactful tools — this is for you.

## What’s the Problem We’re Tackling?

We’ll be working on a real-world challenge inspired by Adobe's Experience Cloud, involving two tasks:

### Task 1: Behavior Simulation
Given a tweet (its content, timestamp, media, etc.), **predict the number of likes** it will receive. This simulates user engagement and helps marketers understand what resonates with their audience.

### Task 2: Content Simulation
Given metadata (e.g., brand, media, timestamp), **generate the tweet text** itself. This is a generative NLP task — essentially an intelligent assistant helping marketers craft high-impact posts.

You’ll be working with a real dataset of 300K tweets from brand accounts, sampled over five years.

## Weekly Roadmap — DevClub Summer of Code: ML+Dev Track

### Week 1: Understanding the Problem & EDA
**Goal:** Grasp the challenge, inspect the dataset, and draw early insights.

**Key Tasks:**
- Read the full problem statement
- Load and explore the dataset (pandas, seaborn, matplotlib)
- Clean and preprocess data
- Identify trends and gaps
- Discuss modeling strategy with mentors or peers

**Checkpoint:**
- Dataset loaded and understood
- EDA report or notebook ready
- Key insights documented

---

### Week 2: Predicting Likes (Behavior Simulation - Task 1)
**Goal:** Train an ML model to estimate user engagement.

**Key Tasks:**
- Feature engineering from tweet metadata
- Train models: Linear Regression, XGBoost, or neural networks
- Evaluate and tune using validation sets
- Create inference script or notebook

**Checkpoint:**
- Trained ML model with baseline RMSE
- Short report explaining your modeling choices

---

### Week 3: Generating Tweets (Content Simulation - Task 2)
**Goal:** Use text generation models to generate tweet content.

**Key Tasks:**
- Prepare data for text generation (tokenization, format)
- Choose a model (T5, GPT-2, or LSTM-based encoder-decoder)
- Train and evaluate using BLEU, ROUGE, CIDEr
- Generate samples and compare with real tweets

**Checkpoint:**
- Generative model with meaningful outputs
- Evaluation scores and generated examples

---

### Week 4: UI Development & System Integration
**Goal:** Build a simple interface where users can input metadata and get predicted likes or generated tweets.

**Key Tasks:**
- Build a basic frontend (Streamlit, Flask, or React)
- Backend to serve models (FastAPI, Flask, or Gradio)
- Integrate models into the app
- UI for input (tweet metadata) and output (likes or content)

**Checkpoint:**
- End-to-end working system locally

---

### Week 5: Model Deployment & Hosting
**Goal:** Package, deploy, and document your project.

**Key Tasks:**
- Containerize with Docker (optional but recommended)
- Host using platforms like Render, HuggingFace Spaces, or AWS
- Create demo video or GIF
- Write a blog or devlog post

**Checkpoint:**
- Deployed app with working URL
- Submission ready for final review

---

## Tools & Technologies

- **Languages:** Python
- **ML Libraries:** Scikit-learn, XGBoost, Transformers (HuggingFace), PyTorch or TensorFlow
- **EDA & Viz:** Pandas, Matplotlib, Seaborn
- **Frontend:** Streamlit / Flask / React
- **Deployment:** HuggingFace Spaces, Render, Vercel, Docker
- **Version Control:** Git + GitHub

## Learning Resources

- [Kaggle Learn: Intro to ML](https://www.kaggle.com/learn/intro-to-machine-learning)
- [CS229 by Andrew Ng (Stanford ML)](https://cs229.stanford.edu/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Gradio Docs](https://www.gradio.app/)
- [PyTorch Tutorials](https://pytorch.org/tutorials/)
- [How to Deploy ML Models](https://mlops.community/)

---

## FAQs

**Q: Do I need deep ML knowledge to join?**  
A: Not at all! We start from the basics and provide beginner-friendly resources.

**Q: Will I have something to show at the end?**  
A: Absolutely — a working ML-powered product and a GitHub repo you can showcase in your resume.

---

## Conclusion

By the end of this 5-week sprint, you’ll have built something real — a deployed ML system that simulates human behavior and content creation. You’ll have gone through all the stages: data cleaning, model training, system integration, and deployment. Most importantly, you’ll have a story to tell and a project to showcase.

Welcome to ML+Dev — let’s build something impactful 🚀
