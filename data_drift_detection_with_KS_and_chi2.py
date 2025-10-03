# Practical application: Monitoring data drift in machine learning
print("\nPRACTICAL APPLICATION: Data Drift Detection")
print("=" * 60)

def detect_data_drift(train_data, current_data, feature_names, feature_types):
    """
    Detect data drift between training data and current production data
    """
    print("Data Drift Analysis")
    print("Feature".ljust(15) + "KS/Chi2 Stat".ljust(15) + "P-value".ljust(12) + "Drift Detected")
    print("-" * 60)
    
    drift_detected = False
    
    for i, (feature, f_type) in enumerate(zip(feature_names, feature_types)):
        train_feature = train_data[:, i]
        current_feature = current_data[:, i]
        
        if f_type == 'continuous':
            # Use KS test for continuous features
            stat, p_val = ks_2samp(train_feature, current_feature)
            test_name = "KS"
        else:
            # Use Chi-square test for categorical features
            # Convert to integer categories if needed
            train_cats, train_counts = np.unique(train_feature, return_counts=True)
            current_cats, current_counts = np.unique(current_feature, return_counts=True)
            
            # Align categories (handle possible missing categories)
            all_cats = np.union1d(train_cats, current_cats)
            train_aligned = np.zeros(len(all_cats))
            current_aligned = np.zeros(len(all_cats))
            
            for j, cat in enumerate(all_cats):
                train_aligned[j] = train_counts[np.where(train_cats == cat)[0][0]] if cat in train_cats else 0
                current_aligned[j] = current_counts[np.where(current_cats == cat)[0][0]] if cat in current_cats else 0
            
            contingency = np.array([train_aligned, current_aligned])
            stat, p_val, _, _ = chi2_contingency(contingency)
            test_name = "Chi2"
        
        has_drift = p_val < 0.05
        if has_drift:
            drift_detected = True
            
        print(f"{feature.ljust(15)}{test_name.ljust(15)}{p_val:.4f}".ljust(32) + 
              f"{'\t\tYES' if has_drift else '\t\tNO'}")
    
    print("-" * 60)
    if drift_detected:
        print("WARNING: Data drift detected in one or more features!")
    else:
        print("No significant data drift detected.")
    
    return drift_detected

# Simulate data for drift detection
np.random.seed(42)
n_samples = 500

# Training data (baseline)
train_data = np.column_stack([
    np.random.normal(0, 1, n_samples),  # Continuous feature 1
    np.random.normal(10, 2, n_samples), # Continuous feature 2
    np.random.choice([0, 1, 2], n_samples, p=[0.6, 0.3, 0.1]),  # Categorical feature 1
    np.random.choice(['A', 'B', 'C'], n_samples, p=[0.5, 0.3, 0.2])  # Categorical feature 2
])

# Current data (with some drift)
current_data = np.column_stack([
    np.random.normal(0.2, 1.2, n_samples),  # Slight drift in mean and variance
    np.random.normal(11, 1.5, n_samples),   # Drift in mean and variance
    np.random.choice([0, 1, 2], n_samples, p=[0.5, 0.35, 0.15]),  # Changed proportions
    np.random.choice(['A', 'B', 'C'], n_samples, p=[0.4, 0.4, 0.2])  # Changed proportions
])

feature_names = ['Feature_1', 'Feature_2', 'Category_1', 'Category_2']
feature_types = ['continuous', 'continuous', 'categorical', 'categorical']

# Detect drift
drift_found = detect_data_drift(train_data, current_data, feature_names, feature_types)

"""
PRACTICAL APPLICATION: Data Drift Detection
============================================================
Data Drift Analysis
Feature        KS/Chi2 Stat   P-value     Drift Detected
------------------------------------------------------------
Feature_1      KS             0.0089        YES
Feature_2      KS             0.0000        YES
Category_1     Chi2           0.2862        NO
Category_2     Chi2           0.0019        YES
------------------------------------------------------------
WARNING: Data drift detected in one or more features!
"""