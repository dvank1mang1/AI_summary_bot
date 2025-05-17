import numpy as np

def compute_z_score(x: float, mean: float, std: float) -> float:
    """
    Compute the Z-Score for a given value x.
    """
    if std == 0:
        return 0.0
    return (x - mean) / std


def select_important(articles, threshold: float = 1.96):
    """
    Select important articles based on Z-Score of text length.
    Only articles with Z-Score > threshold are returned.
    """
    # Compute the word count for each article instead of mention_count
    word_counts = [len(a.get("text", "").split()) for a in articles]

    if len(word_counts) < 2:
        return articles

    mean = np.mean(word_counts)
    std = np.std(word_counts)

    filtered = []
    for article in articles:
        count = len(article.get("text", "").split())
        z = compute_z_score(count, mean, std)
        if z > threshold:
            filtered.append(article)
    return filtered
