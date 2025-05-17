def bayesian_importance(prior: float, likelihood: float, evidence: float) -> float:
    """
    Computes Bayesian importance using the formula:
    P(H|E) = (P(E|H) * P(H)) / P(E)
    """
    if evidence == 0:
        return 0.0
    return (likelihood * prior) / evidence


def select_important(articles, threshold: float = 0.574):
    """
    Selects important articles based on Bayesian inference.
    """
    prior = 0.5  # Base probability that an article is important
    evidence = 1.0  # Simplified assumption
    
    selected = []
    keywords = {"AI", "OpenAI", "GPT", "Machine Learning", "Deep Learning"}
    
    for article in articles:
        word_count = len(article['text'].split())

        # Ignore very short articles
        if word_count < 20:
            continue

        # Calculate base likelihood
        likelihood = min(word_count / 150, 1.0)  # Smoother normalization

        # Boost for keywords, but with diminishing returns
        keyword_count = sum(article['text'].count(kw) for kw in keywords)
        
        # Adjust likelihood based on keyword occurrence (capped at 0.2)
        likelihood += 0.03 * min(keyword_count, 5)

        # Compute the posterior
        posterior = bayesian_importance(prior, likelihood, evidence)

        if posterior > threshold:
            selected.append(article)

    print(f"Model `bayesian` returned {len(selected)} articles.")
    return selected
