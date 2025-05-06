import numpy as np
from sklearn.linear_model import LogisticRegression
# Just a simple training for an example (we do not have list of sources ready yet) Each row: [title_length, mention_count]
X_train = np.array([
    [30, 1],
    [50, 3],
    [20, 0],
    [100, 7],
    [80, 6],
    [15, 0],
    [60, 5]
])
# Labels: 1 = important, 0 = not important
y_train = np.array([0, 1, 0, 1, 1, 0, 1])
# Train the logistic regression model once at import time
model = LogisticRegression()
model.fit(X_train, y_train)


def extract_features(article):
    title_length = len(article.get("title", ""))
    mentions = article.get("mention_count", 1)
    return [title_length, mentions]


def select_important(articles, threshold=0.7):
    selected = []
    for article in articles:
        features = np.array(extract_features(article)).reshape(1, -1)
        prob = model.predict_proba(features)[0][1]
        if prob >= threshold:
            selected.append(article)
    return selected
