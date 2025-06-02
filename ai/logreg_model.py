import numpy as np
from sklearn.linear_model import LogisticRegression

# Training data
X_train = np.array([
    [30, 1, 150],    # [title_length, mention_count, word_count]
    [50, 3, 300],
    [20, 0, 80],
    [100, 7, 800],
    [80, 6, 600],
    [15, 0, 70],
    [60, 5, 400]
])

# Labels: 1 = important, 0 = not important
y_train = np.array([0, 1, 0, 1, 1, 0, 1])

# Train the logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)


def extract_features(article):
    title_length = len(article.get("text", ""))
    mentions = article.get("mention_count", 1)  # Now it is real
    word_count = len(article.get("text", "").split())
    return [title_length, mentions, word_count]


def select_important(articles, threshold=0.6):
    """
    Select important articles using Logistic Regression with a high probability threshold and softened penalties.
    """
    selected = []
    for article in articles:
        features = np.array(extract_features(article)).reshape(1, -1)
        prob = model.predict_proba(features)[0][1]
        
        # Print probability for debugging
        print(f"Article URL: {article['url']}, Initial probability: {prob:.4f}")
        
        # Soft penalty for missing keywords
        keywords = ["AI", "GPT", "OpenAI", "Machine Learning", "Deep Learning"]
        if not any(kw in article.get("text", "") for kw in keywords):
            prob *= 0.85  # Soft penalty for missing keywords
        
        # Soft penalty for articles with low mention count
        if article.get("mention_count", 1) < 3:  # Threshold for mentions
            prob *= 0.9  # Soft penalty for low mentions
        
        print(f"Adjusted probability: {prob:.4f}")

        # Only select articles if probability is above the threshold
        if prob >= threshold:
            selected.append(article)
    return selected
