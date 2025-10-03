import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import ks_2samp, chi2_contingency
import seaborn as sns

# Set random seed for reproducibility
np.random.seed(42)

# Generate two different distributions
n_samples = 1000

# Distribution 1: Normal distribution
dist1 = np.random.normal(loc=0, scale=1, size=n_samples)

# Distribution 2: Different distributions to test
dist2_normal_same = np.random.normal(loc=0, scale=1, size=n_samples)  # Same distribution
dist2_normal_diff_mean = np.random.normal(loc=0.5, scale=1, size=n_samples)  # Different mean
dist2_normal_diff_var = np.random.normal(loc=0, scale=2, size=n_samples)  # Different variance
dist2_exponential = np.random.exponential(scale=1, size=n_samples)  # Completely different shape

def perform_ks_test(dist1, dist2, title):
    """Perform KS test and plot distributions"""
    # Perform KS test
    ks_statistic, p_value = ks_2samp(dist1, dist2)
    
    # Create visualization
    plt.figure(figsize=(10, 6))
    
    plt.subplot(1, 2, 1)
    plt.hist(dist1, bins=30, alpha=0.7, label='Distribution 1', density=True)
    plt.hist(dist2, bins=30, alpha=0.7, label='Distribution 2', density=True)
    plt.title(f'Histograms\n{title}')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    # ECDF plots
    def ecdf(data):
        """Compute ECDF"""
        x = np.sort(data)
        y = np.arange(1, len(data)+1) / len(data)
        return x, y
    
    x1, y1 = ecdf(dist1)
    x2, y2 = ecdf(dist2)
    plt.plot(x1, y1, label='Distribution 1 ECDF')
    plt.plot(x2, y2, label='Distribution 2 ECDF')
    plt.title(f'ECDF Comparison\nKS Stat: {ks_statistic:.4f}, p-value: {p_value:.4f}')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    # Print results
    print(f"{title}")
    print(f"KS Statistic: {ks_statistic:.4f}")
    print(f"P-value: {p_value:.4f}")
    if p_value < 0.05:
        print("Conclusion: Distributions are SIGNIFICANTLY different (reject H0)")
    else:
        print("Conclusion: No significant evidence that distributions differ (fail to reject H0)")
    print("-" * 60)
    
    return ks_statistic, p_value

# Test different scenarios
print("KOLMOGOROV-SMIRNOV TEST EXAMPLES")
print("=" * 60)

# Same distribution
ks1, p1 = perform_ks_test(dist1, dist2_normal_same, "Same Distribution (Normal vs Normal)")

# Different mean
ks2, p2 = perform_ks_test(dist1, dist2_normal_diff_mean, "Different Mean (μ=0 vs μ=0.5)")

# Different variance
ks3, p3 = perform_ks_test(dist1, dist2_normal_diff_var, "Different Variance (σ=1 vs σ=2)")

# Completely different distribution
ks4, p4 = perform_ks_test(dist1, dist2_exponential, "Different Shape (Normal vs Exponential)")

"""
KOLMOGOROV-SMIRNOV TEST EXAMPLES
============================================================

Same Distribution (Normal vs Normal)
KS Statistic: 0.0450
P-value: 0.2635
Conclusion: No significant evidence that distributions differ (fail to reject H0)
------------------------------------------------------------

Different Mean (μ=0 vs μ=0.5)
KS Statistic: 0.2070
P-value: 0.0000
Conclusion: Distributions are SIGNIFICANTLY different (reject H0)
------------------------------------------------------------

Different Variance (σ=1 vs σ=2)
KS Statistic: 0.2010
P-value: 0.0000
Conclusion: Distributions are SIGNIFICANTLY different (reject H0)
------------------------------------------------------------

Different Shape (Normal vs Exponential)
KS Statistic: 0.4920
P-value: 0.0000
Conclusion: Distributions are SIGNIFICANTLY different (reject H0)
------------------------------------------------------------
"""