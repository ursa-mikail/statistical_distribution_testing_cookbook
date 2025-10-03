# =============================================================================
# WHEN TO USE WHICH STATISTICAL TEST - SIMPLE GUIDE
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp, chi2_contingency, ttest_ind, mannwhitneyu
import seaborn as sns

# Set style for better visuals
plt.style.use('default')
sns.set_palette("husl")

print("=" * 70)
print("STATISTICAL TESTS SIMPLE GUIDE")
print("=" * 70)

# =============================================================================
# 1. T-TEST - The "Average" Test
# =============================================================================
print("\n1. T-TEST: Are the AVERAGES different?")
print("   → Example: 'Does the new feature increase average revenue?'")

# Generate more realistic data with some overlap
np.random.seed(42)
group_a = np.random.normal(100, 20, 200)  # Average revenue $100
group_b = np.random.normal(108, 20, 200)  # Average revenue $108 (smaller difference)

# Plot
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.hist(group_a, alpha=0.7, label='Old Feature', bins=20)
plt.hist(group_b, alpha=0.7, label='New Feature', bins=20)
plt.xlabel('Revenue per User ($)')
plt.legend()
plt.title('T-Test: Compare AVERAGES')

plt.subplot(1, 2, 2)
means = [np.mean(group_a), np.mean(group_b)]
errors = [np.std(group_a)/np.sqrt(len(group_a)), np.std(group_b)/np.sqrt(len(group_b))]
plt.bar(['Old Feature', 'New Feature'], means, yerr=errors, capsize=10, alpha=0.7)
plt.title('Average Revenue ± Standard Error')
plt.ylabel('Dollars ($)')

plt.tight_layout()
plt.show()

# Test
t_stat, pval = ttest_ind(group_a, group_b)
print(f"   Result: p-value = {pval:.6f}")
print(f"   Old Feature: ${np.mean(group_a):.1f}, New Feature: ${np.mean(group_b):.1f}")
if pval < 0.05:
    print("   ✅ New feature significantly increases revenue!")
else:
    print("   ❌ No significant revenue difference")

# =============================================================================
# 2. CHI-SQUARE TEST - The "Preference" Test  
# =============================================================================
print("\n2. CHI-SQUARE TEST: Did PREFERENCES change?")
print("   → Example: 'After marketing, did product choices change?'")

# Generate more realistic data (smaller change)
products = ['Product A', 'Product B', 'Product C']
before = [300, 150, 50]   # 60% A, 30% B, 10% C
after = [280, 160, 60]    # 56% A, 32% B, 12% C (smaller change)

# Plot
plt.figure(figsize=(10, 4))
x_pos = np.arange(len(products))
width = 0.35

plt.bar(x_pos - width/2, before, width, label='Before Campaign', alpha=0.7)
plt.bar(x_pos + width/2, after, width, label='After Campaign', alpha=0.7)
plt.xticks(x_pos, products)
plt.ylabel('Number of Customers')
plt.title('Chi-Square: Did PREFERENCES change?')
plt.legend()

# Add percentage labels
total_before = sum(before)
total_after = sum(after)
for i, (b, a) in enumerate(zip(before, after)):
    plt.text(i - width/2, b + 5, f'{b/total_before*100:.0f}%', ha='center')
    plt.text(i + width/2, a + 5, f'{a/total_after*100:.0f}%', ha='center')

plt.show()

# Test
chi2, pval, _, _ = chi2_contingency([before, after])
print(f"   Result: p-value = {pval:.6f}")
if pval < 0.05:
    print("   ✅ Campaign significantly changed preferences!")
else:
    print("   ❌ No significant preference change")
    print("   (Small changes could be due to random variation)")

# =============================================================================
# 3. KOLMOGOROV-SMIRNOV TEST - The "Pattern" Test
# =============================================================================
print("\n3. KOLMOGOROV-SMIRNOV TEST: Did the PATTERN change?")
print("   → Example: 'Did user behavior pattern change (not just average)?'")

# Generate data with more subtle pattern difference
np.random.seed(42)
normal_users = np.random.normal(5, 1.5, 1000)  # Most spend medium time

# Slightly bimodal distribution
bimodal_users = np.concatenate([
    np.random.normal(4, 1, 700),   # Regular users
    np.random.normal(7, 1, 300)    # Power users
])

# Plot
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.hist(normal_users, alpha=0.7, label='Most users similar', bins=30, density=True)
plt.hist(bimodal_users, alpha=0.7, label='Two user types', bins=30, density=True)
plt.xlabel('Time Spent (minutes)')
plt.legend()
plt.title('KS Test: Compare PATTERNS')

plt.subplot(1, 2, 2)
# ECDF plots
def ecdf(data):
    x = np.sort(data)
    y = np.arange(1, len(data)+1) / len(data)
    return x, y

x1, y1 = ecdf(normal_users)
x2, y2 = ecdf(bimodal_users)
plt.plot(x1, y1, label='Most users similar')
plt.plot(x2, y2, label='Two user types')
plt.xlabel('Time Spent (minutes)')
plt.ylabel('Proportion of Users')
plt.title('Cumulative Distribution')
plt.legend()

plt.tight_layout()
plt.show()

# Test
ks_stat, pval = ks_2samp(normal_users, bimodal_users)
print(f"   Result: p-value = {pval:.6f}")
print(f"   KS Statistic: {ks_stat:.4f}")
if pval < 0.05:
    print("   ✅ User behavior pattern significantly changed!")
else:
    print("   ❌ No significant pattern change")

# =============================================================================
# 4. MANN-WHITNEY U TEST - The "Generally Higher" Test
# =============================================================================
print("\n4. MANN-WHITNEY U TEST: Is one group GENERALLY higher?")
print("   → Example: 'Do premium users have higher engagement?'")

# Generate data with more overlap
np.random.seed(42)
free_users = np.random.exponential(3, 500)  # Most low engagement
premium_users = np.random.exponential(4, 500)  # Generally higher but overlapping

# Plot
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.hist(free_users, alpha=0.7, label='Free Users', bins=30, density=True)
plt.hist(premium_users, alpha=0.7, label='Premium Users', bins=30, density=True)
plt.xlabel('Engagement Score')
plt.legend()
plt.title('Mann-Whitney: Compare RANKS')

plt.subplot(1, 2, 2)
plt.boxplot([free_users, premium_users], labels=['Free Users', 'Premium Users'])
plt.ylabel('Engagement Score')
plt.title('Distribution Comparison')

plt.tight_layout()
plt.show()

# Test
u_stat, pval = mannwhitneyu(free_users, premium_users)
print(f"   Result: p-value = {pval:.6f}")
print(f"   Median - Free: {np.median(free_users):.2f}, Premium: {np.median(premium_users):.2f}")
if pval < 0.05:
    print("   ✅ Premium users have significantly higher engagement!")
else:
    print("   ❌ No significant difference in engagement levels")

# =============================================================================
# 5. KL DIVERGENCE - The "Surprise" Measure
# =============================================================================
print("\n5. KL DIVERGENCE: How SURPRISED would we be?")
print("   → Example: 'How different is actual behavior from expected?'")

# Expected vs actual distributions (more realistic)
expected = np.array([0.5, 0.3, 0.2])  # Expected: 50% low, 30% medium, 20% high usage
actual = np.array([0.4, 0.35, 0.25])  # Actual: slightly different

usage_levels = ['Low Usage', 'Medium Usage', 'High Usage']

# Plot
plt.figure(figsize=(10, 4))
x_pos = np.arange(len(usage_levels))
width = 0.35

bars1 = plt.bar(x_pos - width/2, expected, width, label='Expected', alpha=0.7)
bars2 = plt.bar(x_pos + width/2, actual, width, label='Actual', alpha=0.7)
plt.xticks(x_pos, usage_levels)
plt.ylabel('Proportion')
plt.title('KL Divergence: How "surprised" are we?')
plt.legend()

# Add value labels
for i, (exp, act) in enumerate(zip(expected, actual)):
    plt.text(i - width/2, exp + 0.01, f'{exp:.0%}', ha='center')
    plt.text(i + width/2, act + 0.01, f'{act:.0%}', ha='center')

plt.show()

# Calculate KL Divergence (add small value to avoid division by zero)
kl = np.sum(actual * np.log(actual / (expected + 1e-10)))
print(f"   Result: KL Divergence = {kl:.6f}")
if kl > 0.1:
    print("   🔥 Very surprised! Reality differs from expectations")
elif kl > 0.01:
    print("   ⚠️  Moderately surprised - noticeable differences")
else:
    print("   ✅ Little surprise - close to expectations")

# =============================================================================
# INTERPRETING P-VALUES
# =============================================================================
print("\n" + "=" * 70)
print("UNDERSTANDING P-VALUES")
print("=" * 70)

print("""
P-VALUE GUIDE:
• p < 0.05: Statistically significant - unlikely due to chance
• p < 0.01: Highly significant - very unlikely due to chance  
• p < 0.001: Extremely significant - almost certainly not chance
• p > 0.05: Not significant - could be due to random variation

Remember: Statistical significance ≠ Practical importance!
A tiny difference can be 'significant' with large sample sizes.
""")

# =============================================================================
# DECISION TREE - Which Test to Use?
# =============================================================================
print("\n" + "=" * 70)
print("QUICK DECISION TREE")
print("=" * 70)

print("""
ASK YOURSELF:

1. Are you comparing CATEGORIES (like product choices)?
   → USE CHI-SQUARE TEST

2. Are you comparing NUMBERS?
   • "Are the AVERAGES different?" → T-TEST
   • "Is the overall PATTERN different?" → KOLMOGOROV-SMIRNOV  
   • "Is one group GENERALLY higher?" → MANN-WHITNEY U

3. Do you want to measure "how surprised" you'd be?
   → USE KL DIVERGENCE
""")

# =============================================================================
# REAL-WORLD SCENARIOS
# =============================================================================
print("\n" + "=" * 70)
print("REAL-WORLD SCENARIOS")
print("=" * 70)

scenarios = [
    {
        "question": "Did the new website design change how long people stay?",
        "test": "KS TEST",
        "reason": "Looking at the entire pattern of user behavior"
    },
    {
        "question": "After our ad campaign, did product preferences shift?",
        "test": "CHI-SQUARE TEST", 
        "reason": "Comparing category frequencies"
    },
    {
        "question": "Does the new feature increase average revenue per user?",
        "test": "T-TEST",
        "reason": "Comparing average values"
    },
    {
        "question": "Are customer satisfaction scores higher for paid users?",
        "test": "MANN-WHITNEY U",
        "reason": "Scores are usually skewed, not normal"
    },
    {
        "question": "How different is current user behavior from our predictions?",
        "test": "KL DIVERGENCE",
        "reason": "Measuring 'surprise' between expected vs actual"
    }
]

for i, scenario in enumerate(scenarios, 1):
    print(f"\n{i}. {scenario['question']}")
    print(f"   👉 USE: {scenario['test']}")
    print(f"   💡 Why: {scenario['reason']}")

print("\n" + "=" * 70)
print("SUMMARY COMPLETED!")
print("=" * 70)

"""
======================================================================
STATISTICAL TESTS SIMPLE GUIDE
======================================================================

1. T-TEST: Are the AVERAGES different?
   → Example: 'Does the new feature increase average revenue?'

   Result: p-value = 0.000000
   Old Feature: $99.2, New Feature: $109.7
   ✅ New feature significantly increases revenue!

2. CHI-SQUARE TEST: Did PREFERENCES change?
   → Example: 'After marketing, did product choices change?'

   Result: p-value = 0.382639
   ❌ No significant preference change
   (Small changes could be due to random variation)

3. KOLMOGOROV-SMIRNOV TEST: Did the PATTERN change?
   → Example: 'Did user behavior pattern change (not just average)?'

   Result: p-value = 0.000004
   KS Statistic: 0.1140
   ✅ User behavior pattern significantly changed!

4. MANN-WHITNEY U TEST: Is one group GENERALLY higher?
   → Example: 'Do premium users have higher engagement?'
/tmp/ipython-input-3644407060.py:172: MatplotlibDeprecationWarning: The 'labels' parameter of boxplot() has been renamed 'tick_labels' since Matplotlib 3.9; support for the old name will be dropped in 3.11.
  plt.boxplot([free_users, premium_users], labels=['Free Users', 'Premium Users'])

   Result: p-value = 0.003316
   Median - Free: 2.16, Premium: 2.55
   ✅ Premium users have significantly higher engagement!

5. KL DIVERGENCE: How SURPRISED would we be?
   → Example: 'How different is actual behavior from expected?'

   Result: KL Divergence = 0.020481
   ⚠️  Moderately surprised - noticeable differences

======================================================================
UNDERSTANDING P-VALUES
======================================================================

P-VALUE GUIDE:
• p < 0.05: Statistically significant - unlikely due to chance
• p < 0.01: Highly significant - very unlikely due to chance  
• p < 0.001: Extremely significant - almost certainly not chance
• p > 0.05: Not significant - could be due to random variation

Remember: Statistical significance ≠ Practical importance!
A tiny difference can be 'significant' with large sample sizes.


======================================================================
QUICK DECISION TREE
======================================================================

ASK YOURSELF:

1. Are you comparing CATEGORIES (like product choices)?
   → USE CHI-SQUARE TEST

2. Are you comparing NUMBERS?
   • "Are the AVERAGES different?" → T-TEST
   • "Is the overall PATTERN different?" → KOLMOGOROV-SMIRNOV  
   • "Is one group GENERALLY higher?" → MANN-WHITNEY U

3. Do you want to measure "how surprised" you'd be?
   → USE KL DIVERGENCE


======================================================================
REAL-WORLD SCENARIOS
======================================================================

1. Did the new website design change how long people stay?
   👉 USE: KS TEST
   💡 Why: Looking at the entire pattern of user behavior

2. After our ad campaign, did product preferences shift?
   👉 USE: CHI-SQUARE TEST
   💡 Why: Comparing category frequencies

3. Does the new feature increase average revenue per user?
   👉 USE: T-TEST
   💡 Why: Comparing average values

4. Are customer satisfaction scores higher for paid users?
   👉 USE: MANN-WHITNEY U
   💡 Why: Scores are usually skewed, not normal

5. How different is current user behavior from our predictions?
   👉 USE: KL DIVERGENCE
   💡 Why: Measuring 'surprise' between expected vs actual

======================================================================
SUMMARY COMPLETED!
======================================================================
"""