from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

"""
What does this model do? 
Selects one article from each cluster based on TF-IDF and KMeans clustering.
"""

def select_important(articles, n_clusters=2):
    if len(articles) == 0:
        return []

    # Replaced 'title' with 'text'
    texts = [article.get('text', '') for article in articles]

    # Filter empty texts
    texts = [t for t in texts if len(t.split()) > 3]

    if len(texts) < n_clusters:
        return articles  # No need to clusterize

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(texts)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
    labels = kmeans.fit_predict(X)

    selected = []
    seen_labels = set()

    for i, label in enumerate(labels):
        if label not in seen_labels:
            selected.append(articles[i])
            seen_labels.add(label)

    return selected
