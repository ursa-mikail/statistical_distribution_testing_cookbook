# Precision-Recall Curve
precision, recall, pr_thresholds = precision_recall_curve(y_test, y_pred_proba)
pr_auc = auc(recall, precision)

plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.plot(recall, precision, color='blue', lw=2, label=f'PR curve (AUC = {pr_auc:.4f})')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
# Compare ROC AUC vs PR AUC
metrics_comparison = ['ROC AUC', 'PR AUC']
scores = [roc_auc, pr_auc]
colors = ['lightcoral', 'lightblue']

plt.bar(metrics_comparison, scores, color=colors, alpha=0.7)
plt.ylabel('Score')
plt.title('ROC AUC vs PR AUC Comparison')
plt.ylim(0, 1)
for i, v in enumerate(scores):
    plt.text(i, v + 0.01, f'{v:.4f}', ha='center')

plt.tight_layout()
plt.show()

print(f"PR AUC: {pr_auc:.4f}")
print("Use PR AUC when:")
print("• Dataset is imbalanced")
print("• You care more about positive class performance")
print("• False positives are costly")

"""
PR AUC: 0.8300
Use PR AUC when:
• Dataset is imbalanced
• You care more about positive class performance
• False positives are costly
"""