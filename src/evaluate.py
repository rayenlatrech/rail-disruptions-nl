from sklearn.metrics import (
    average_precision_score, 
    brier_score_loss, 
    roc_auc_score
)

def evaluate(y_true, y_prob, name):
    """Return ROC-AUC, PR-AUC and Brier score for predicted probabilities."""
    return {
        "model": name,
        "roc_auc": roc_auc_score(y_true,y_prob),
        "pr_auc": average_precision_score(y_true,y_prob),
        "brier": brier_score_loss(y_true,y_prob)
    }

