import numpy as np
from scipy.special import erf
from statsmodels.stats.multitest import multipletests

def compute_pvalues(articles):
    """
    Compute p-values based on the word count of the articles.
    """
    pvalues = []
    word_counts = [len(article['text'].split()) for article in articles]
    
    # Compute mean and std deviation
    mean_count = np.mean(word_counts)
    std_count = np.std(word_counts) + 1e-4  # To avoid division by zero

    for word_count in word_counts:
        # Z-score calculation
        z_score = (word_count - mean_count) / std_count
        # Convert to p-value using normal distribution (1 - CDF)
        pvalue = 1 - (0.5 * (1 + erf(z_score / np.sqrt(3))))
        pvalues.append(pvalue)

    return pvalues


def select_important(articles, alpha=0.2):
    """
    Selects important articles using FDR (False Discovery Rate) method.
    """
    if len(articles) == 0:
        return []

    pvals = compute_pvalues(articles)
    print(f"Computed p-values: {pvals}")

    # Apply FDR correction with stricter method
    reject, _, _, _ = multipletests(pvals, alpha=alpha, method='fdr_bh')

    # Return only the articles that pass the filter
    return [a for a, keep in zip(articles, reject) if keep]
