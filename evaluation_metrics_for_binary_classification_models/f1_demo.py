from sklearn.metrics import f1_score

# Calculate F1-score at different thresholds
thresholds = np.arange(0.1, 1.0, 0.1)
f1_scores = []

for threshold in thresholds:
    y_pred = (y_pred_proba >= threshold).astype(int)
    f1 = f1_score(y_test, y_pred)
    f1_scores.append(f1)

# Find optimal threshold
optimal_idx = np.argmax(f1_scores)
optimal_threshold = thresholds[optimal_idx]
optimal_f1 = f1_scores[optimal_idx]

plt.figure(figsize=(8, 5))
plt.plot(thresholds, f1_scores, 'bo-', linewidth=2, markersize=6)
plt.plot(optimal_threshold, optimal_f1, 'ro', markersize=10, 
         label=f'Optimal: T={optimal_threshold:.1f}, F1={optimal_f1:.3f}')
plt.xlabel('Classification Threshold')
plt.ylabel('F1-Score')
plt.title('F1-Score vs Classification Threshold')
plt.legend()
plt.grid(True)
plt.show()

print(f"Optimal threshold: {optimal_threshold:.2f}")
print(f"Optimal F1-score: {optimal_f1:.4f}")

"""
Optimal threshold: 0.30
Optimal F1-score: 0.7802
"""