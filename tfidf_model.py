from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

"What does this model do? Selects one article from each cluster based on TF-IDF and KMeans clustering."
"Что делает эта модель? Выбирает по одной статье из каждого кластера на основе TF-IDF и KMeans кластеризации."

def select_important(articles, n_clusters=3):
    if len(articles) == 0:
        return []

    texts = [article.get('title', '') for article in articles]

    if len(articles) < n_clusters:
        return articles  #No need in clustering

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
