def comprehensive_evaluation(y_true, y_pred_proba, model_name="Model"):
    """Comprehensive model evaluation with multiple metrics"""
    
    # Calculate metrics at optimal threshold
    precision, recall, thresholds = precision_recall_curve(y_true, y_pred_proba)
    f1_scores = 2 * (precision * recall) / (precision + recall)
    optimal_idx = np.argmax(f1_scores[:-1])  # Exclude last element
    optimal_threshold = thresholds[optimal_idx]
    
    y_pred_optimal = (y_pred_proba >= optimal_threshold).astype(int)
    
    # Calculate all metrics
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    
    accuracy = accuracy_score(y_true, y_pred_optimal)
    precision_val = precision_score(y_true, y_pred_optimal)
    recall_val = recall_score(y_true, y_pred_optimal)
    f1 = f1_score(y_true, y_pred_optimal)
    roc_auc = roc_auc_score(y_true, y_pred_proba)
    
    # Print results
    print(f"\n{'='*50}")
    print(f"COMPREHENSIVE EVALUATION: {model_name}")
    print(f"{'='*50}")
    print(f"Optimal Threshold: {optimal_threshold:.4f}")
    print(f"ROC AUC: {roc_auc:.4f}")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision_val:.4f}")
    print(f"Recall: {recall_val:.4f}")
    print(f"F1-Score: {f1:.4f}")
    
    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred_optimal)
    print(f"\nConfusion Matrix:")
    print(f"True Negatives: {cm[0,0]}, False Positives: {cm[0,1]}")
    print(f"False Negatives: {cm[1,0]}, True Positives: {cm[1,1]}")
    
    return {
        'optimal_threshold': optimal_threshold,
        'roc_auc': roc_auc,
        'accuracy': accuracy,
        'precision': precision_val,
        'recall': recall_val,
        'f1_score': f1
    }

# Run comprehensive evaluation
results = comprehensive_evaluation(y_test, y_pred_proba, "Logistic Regression")

"""

==================================================
COMPREHENSIVE EVALUATION: Logistic Regression
==================================================
Optimal Threshold: 0.2950
ROC AUC: 0.9068
Accuracy: 0.8700
Precision: 0.7579
Recall: 0.8182
F1-Score: 0.7869

Confusion Matrix:
True Negatives: 189, False Positives: 23
False Negatives: 16, True Positives: 72
"""