import numpy as np
from statsmodels.stats.multitest import multipletests

def compute_pvalues(articles):
    return [1.0 / (a.get("mention_count", 1) + 1e-8) for a in articles]


def select_important(articles, alpha=0.05):
    if len(articles) == 0:
        return []

    pvals = compute_pvalues(articles)
    reject, _, _, _ = multipletests(pvals, alpha=alpha, method='fdr_bh')

    return [a for a, keep in zip(articles, reject) if keep]
