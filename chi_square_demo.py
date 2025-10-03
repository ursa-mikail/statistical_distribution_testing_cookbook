# Chi-square test examples
print("\nCHI-SQUARE TEST EXAMPLES")
print("=" * 60)

def perform_chi2_test(observed1, observed2, categories, title):
    """Perform Chi-square test for categorical data"""
    
    # Create contingency table
    contingency_table = np.array([observed1, observed2])
    
    # Perform Chi-square test
    chi2_stat, p_value, dof, expected = chi2_contingency(contingency_table)
    
    # Create visualization
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    x_pos = np.arange(len(categories))
    width = 0.35
    
    plt.bar(x_pos - width/2, observed1, width, label='Group 1', alpha=0.7)
    plt.bar(x_pos + width/2, observed2, width, label='Group 2', alpha=0.7)
    plt.xlabel('Categories')
    plt.ylabel('Frequency')
    plt.title(f'Category Frequencies\n{title}')
    plt.xticks(x_pos, categories)
    plt.legend()
    
    plt.subplot(1, 2, 2)
    # Expected vs observed for group 1
    x_pos_small = np.arange(len(categories))
    plt.bar(x_pos_small - width/2, observed1, width, label='Observed', alpha=0.7)
    plt.bar(x_pos_small + width/2, expected[0], width, label='Expected', alpha=0.7)
    plt.xlabel('Categories')
    plt.ylabel('Frequency')
    plt.title(f'Observed vs Expected (Group 1)\nχ²: {chi2_stat:.4f}, p-value: {p_value:.4f}')
    plt.xticks(x_pos_small, categories)
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    # Print results
    print(f"{title}")
    print(f"Contingency Table:")
    print(f"Group 1: {observed1}")
    print(f"Group 2: {observed2}")
    print(f"Chi-square Statistic: {chi2_stat:.4f}")
    print(f"P-value: {p_value:.4f}")
    print(f"Degrees of freedom: {dof}")
    print("Expected frequencies:")
    print(expected)
    if p_value < 0.05:
        print("Conclusion: Category distributions are SIGNIFICANTLY different (reject H0)")
    else:
        print("Conclusion: No significant evidence that category distributions differ (fail to reject H0)")
    print("-" * 60)
    
    return chi2_stat, p_value

# Example 1: Same distribution of colors
categories = ['Red', 'Blue', 'Green', 'Yellow']
observed1_same = [25, 30, 35, 20]  # Group 1
observed2_same = [26, 29, 34, 21]  # Group 2 (similar distribution)

chi1, p1 = perform_chi2_test(observed1_same, observed2_same, categories, 
                           "Same Distribution (Similar Proportions)")

# Example 2: Different distribution of colors
observed1_diff = [25, 30, 35, 20]  # Group 1
observed2_diff = [45, 15, 25, 25]  # Group 2 (different distribution)

chi2, p2 = perform_chi2_test(observed1_diff, observed2_diff, categories,
                           "Different Distribution (Different Proportions)")

# Example 3: Customer preference change over time
print("\nREAL-WORLD EXAMPLE: Customer Preference Change")
print("=" * 60)

# Before marketing campaign
categories_product = ['Product A', 'Product B', 'Product C', 'Product D']
preferences_before = [120, 80, 60, 40]  # 300 customers total
preferences_after = [150, 70, 50, 30]   # 300 customers after campaign

chi3, p3 = perform_chi2_test(preferences_before, preferences_after, categories_product,
                           "Customer Preferences: Before vs After Marketing Campaign")

"""

CHI-SQUARE TEST EXAMPLES
============================================================

Same Distribution (Similar Proportions)
Contingency Table:
Group 1: [25, 30, 35, 20]
Group 2: [26, 29, 34, 21]
Chi-square Statistic: 0.0754
P-value: 0.9946
Degrees of freedom: 3
Expected frequencies:
[[25.5 29.5 34.5 20.5]
 [25.5 29.5 34.5 20.5]]
Conclusion: No significant evidence that category distributions differ (fail to reject H0)
------------------------------------------------------------

Different Distribution (Different Proportions)
Contingency Table:
Group 1: [25, 30, 35, 20]
Group 2: [45, 15, 25, 25]
Chi-square Statistic: 12.9365
P-value: 0.0048
Degrees of freedom: 3
Expected frequencies:
[[35.  22.5 30.  22.5]
 [35.  22.5 30.  22.5]]
Conclusion: Category distributions are SIGNIFICANTLY different (reject H0)
------------------------------------------------------------

REAL-WORLD EXAMPLE: Customer Preference Change
============================================================

Customer Preferences: Before vs After Marketing Campaign
Contingency Table:
Group 1: [120, 80, 60, 40]
Group 2: [150, 70, 50, 30]
Chi-square Statistic: 6.3377
P-value: 0.0963
Degrees of freedom: 3
Expected frequencies:
[[135.  75.  55.  35.]
 [135.  75.  55.  35.]]
Conclusion: No significant evidence that category distributions differ (fail to reject H0)
------------------------------------------------------------
"""