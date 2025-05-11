import numpy as np

def compute_z_score(x: float, mean: float, std: float) -> float:
    if std == 0:
        return 0.0
    return (x - mean) / std


def select_important(articles, threshold: float = 1.96):
    mention_counts = [a.get("mention_count", 1) for a in articles]

    if len(mention_counts) < 2:
        return articles

    mean = np.mean(mention_counts)
    std = np.std(mention_counts)

    filtered = []
    for article in articles:
        count = article.get("mention_count", 1)
        z = compute_z_score(count, mean, std)
        if z > threshold:
            filtered.append(article)

    return filtered
