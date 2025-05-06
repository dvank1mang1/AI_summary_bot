def bayesian_importance(prior: float, likelihood: float, evidence: float) -> float:
    if evidence == 0:
        return 0.0
    return (likelihood * prior) / evidence


def select_important(articles, threshold: float = 0.6):
    prior = 0.5  # Prior belief that any given article is important
    evidence = 1.0  # Simplified assumption

    selected = []
    for article in articles:
        mention_count = article.get("mention_count", 1)
        likelihood = min(mention_count / 10, 1.0)  # Normalized to max of 1.0
        posterior = bayesian_importance(prior, likelihood, evidence)
        if posterior > threshold:
            selected.append(article)

    return selected
