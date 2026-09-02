# SIH AI Problem Recommendation System

An AI-powered recommendation system that helps users find relevant Smart India Hackathon (SIH) problem statements based on their skills, interests, technologies, and domains.

## Features

* Recommends relevant SIH problem statements
* Uses TF-IDF for text feature extraction
* Uses Cosine Similarity for problem matching
* Supports multi-skill matching
* Uses hybrid recommendation scoring
* Considers problem title, theme, category, and description
* Penalizes generic problem titles
* Provides Top 10 recommendations
* Shows matching skills
* Provides recommendation explanations
* Supports recommendation quality evaluation

## Project Workflow

User Skills and Interests
↓
Skill Detection
↓
TF-IDF Vectorization
↓
Cosine Similarity
↓
Multi-Skill Matching
↓
Theme and Domain Matching
↓
Hybrid Scoring
↓
Rank SIH Problem Statements
↓
Top 10 Recommendations
↓
Why Recommended Explanation

## Project Structure

```text
SIH_AI_Problem_Recommendation/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── 02_recommendation_model.ipynb
│
├── models/
│   ├── sih_tfidf_vectorizer.pkl
│   └── sih_tfidf_matrix.pkl
│
├── src/
│   ├── __init__.py
│   ├── data_preprocessing.py
│   ├── feature_engineering.py
│   ├── skill_matching.py
│   ├── scoring.py
│   ├── recommendation_engine.py
│   └── evaluation.py
│
├── app/
│   ├── app.py
│   ├── config.py
│   ├── templates/
│   └── static/
│
└── tests/
```

## Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* TF-IDF Vectorizer
* Cosine Similarity
* Jupyter Notebook / Google Colab

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd SIH_AI_Problem_Recommendation
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Model Components

### TF-IDF Vectorizer

Converts SIH problem text into numerical vectors.

### Cosine Similarity

Measures similarity between user skills/interests and SIH problem statements.

### Multi-Skill Matching

Detects multiple skills from the user input and checks which skills match each problem.

### Hybrid Scoring

The final recommendation score combines:

```text
TF-IDF Similarity
+
Skill Matching
+
Skill Coverage
+
Theme/Domain Matching
-
Generic Title Penalty
=
Final Recommendation Score
```

## Current Status

Core recommendation model: Completed

Next development stages:

* Convert notebook code into reusable Python modules
* Build recommendation engine
* Build application interface
* Add testing
* Deploy the system

## Author

Sahil

BCA AI/ML Student
Amrapali University
