import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc, roc_auc_score
from sklearn.metrics import precision_recall_curve, confusion_matrix, classification_report

# Generate sample data
X, y = make_classification(n_samples=1000, n_features=20, n_classes=2, 
                          random_state=42, weights=[0.7, 0.3])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, 
                                                    random_state=42)

# Train a model
model = LogisticRegression()
model.fit(X_train, y_train)

# Get predicted probabilities
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Calculate ROC curve and AUC
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)

print(f"ROC AUC Score: {roc_auc:.4f}")

# Plot ROC curve
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.4f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
plt.grid(True)

# Show some threshold points
threshold_points = [0.2, 0.5, 0.8]
for threshold in threshold_points:
    idx = np.argmin(np.abs(thresholds - threshold))
    plt.plot(fpr[idx], tpr[idx], 'ro', markersize=8)
    plt.annotate(f'T={threshold:.1f}', (fpr[idx], tpr[idx]), 
                xytext=(10, 10), textcoords='offset points')

plt.subplot(1, 2, 2)
# Show threshold distribution
plt.hist(y_pred_proba[y_test == 0], alpha=0.7, label='Class 0', bins=20)
plt.hist(y_pred_proba[y_test == 1], alpha=0.7, label='Class 1', bins=20)
plt.xlabel('Predicted Probability')
plt.ylabel('Frequency')
plt.title('Probability Distribution by True Class')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Interpretation
print(f"\nROC AUC Interpretation:")
print(f"• AUC = {roc_auc:.4f}: The model has a {roc_auc*100:.1f}% chance of ranking")
print("  a random positive instance higher than a random negative instance")
print("• Closer to 1.0 = Better model")
print("• 0.5 = Random guessing")
print("• < 0.5 = Worse than random")

"""
ROC AUC Score: 0.9068


ROC AUC Interpretation:
• AUC = 0.9068: The model has a 90.7% chance of ranking
  a random positive instance higher than a random negative instance
• Closer to 1.0 = Better model
• 0.5 = Random guessing
• < 0.5 = Worse than random
"""