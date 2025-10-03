# =============================================================================
# KL DIVERGENCE vs JS DIVERGENCE - SIMPLE EXPLANATION
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import jensenshannon

print("=" * 70)
print("KL DIVERGENCE vs JS DIVERGENCE")
print("=" * 70)

# =============================================================================
# 1. KL DIVERGENCE - The "Surprise" Measure
# =============================================================================
print("\n1. KL DIVERGENCE (Kullback-Leibler)")
print("   → 'How SURPRISED would you be if you expected P but saw Q?'")

def kl_divergence(p, q):
    """Calculate KL Divergence between two distributions"""
    # Add small epsilon to avoid log(0)
    p_safe = np.clip(p, 1e-10, 1)
    q_safe = np.clip(q, 1e-10, 1)
    return np.sum(p_safe * np.log(p_safe / q_safe))

# Example 1: Small difference
print("\n--- EXAMPLE 1: Small Difference ---")
p1 = np.array([0.4, 0.3, 0.3])  # Expected distribution
q1 = np.array([0.35, 0.35, 0.3]) # Actual distribution (slightly different)

kl1 = kl_divergence(p1, q1)
print(f"Expected: {p1}")
print(f"Actual:   {q1}")
print(f"KL(P||Q) = {kl1:.6f}")

# Example 2: Large difference
print("\n--- EXAMPLE 2: Large Difference ---")
p2 = np.array([0.8, 0.2])  # Expected: 80% success
q2 = np.array([0.2, 0.8])  # Actual: 20% success (complete reversal)

kl2 = kl_divergence(p2, q2)
print(f"Expected: {p2}")
print(f"Actual:   {q2}")
print(f"KL(P||Q) = {kl2:.6f}")

# =============================================================================
# 2. JS DIVERGENCE - The "Symmetrical" Measure
# =============================================================================
print("\n2. JS DIVERGENCE (Jensen-Shannon)")
print("   → 'How different are P and Q on average?'")

def js_divergence(p, q):
    """Calculate JS Divergence between two distributions"""
    # JS is symmetric and always between 0 and 1
    return jensenshannon(p, q)

# Same examples with JS Divergence
print("\n--- EXAMPLE 1: Small Difference ---")
js1 = js_divergence(p1, q1)
print(f"Expected: {p1}")
print(f"Actual:   {q1}")
print(f"JS(P,Q) = {js1:.6f}")

print("\n--- EXAMPLE 2: Large Difference ---")
js2 = js_divergence(p2, q2)
print(f"Expected: {p2}")
print(f"Actual:   {q2}")
print(f"JS(P,Q) = {js2:.6f}")

# =============================================================================
# 3. KEY DIFFERENCES - Side by Side Comparison
# =============================================================================
print("\n" + "=" * 70)
print("KEY DIFFERENCES")
print("=" * 70)

# Create test cases to demonstrate differences
test_cases = [
    {
        "name": "Identical Distributions",
        "p": np.array([0.5, 0.5]),
        "q": np.array([0.5, 0.5])
    },
    {
        "name": "Small Difference", 
        "p": np.array([0.6, 0.4]),
        "q": np.array([0.55, 0.45])
    },
    {
        "name": "Large Difference",
        "p": np.array([0.9, 0.1]),
        "q": np.array([0.1, 0.9])
    },
    {
        "name": "Zero in Q (KL problem)",
        "p": np.array([0.5, 0.5]),
        "q": np.array([1.0, 0.0])  # This breaks KL!
    }
]

print("\nCOMPARISON TABLE:")
print("-" * 80)
print(f"{'Case':<20} {'KL(P||Q)':<12} {'KL(Q||P)':<12} {'JS(P,Q)':<12} {'Symmetric?'}")
print("-" * 80)

for case in test_cases:
    p, q = case["p"], case["q"]
    
    try:
        kl_pq = kl_divergence(p, q)
    except:
        kl_pq = float('inf')
    
    try:
        kl_qp = kl_divergence(q, p)
    except:
        kl_qp = float('inf')
    
    js = js_divergence(p, q)
    
    symmetric_kl = abs(kl_pq - kl_qp) < 1e-10
    
    print(f"{case['name']:<20} {kl_pq:<12.6f} {kl_qp:<12.6f} {js:<12.6f} {'Yes' if symmetric_kl else 'NO!'}")

# =============================================================================
# 4. VISUAL COMPARISON
# =============================================================================
print("\n" + "=" * 70)
print("VISUAL COMPARISON")
print("=" * 70)

# Create a range of differences and compare KL vs JS
differences = np.linspace(0, 0.9, 20)
kl_values = []
js_values = []

p_base = np.array([0.5, 0.5])

for diff in differences:
    q_test = np.array([0.5 + diff, 0.5 - diff])
    q_test = np.clip(q_test, 0.01, 0.99)  # Avoid zeros
    q_test = q_test / np.sum(q_test)  # Renormalize
    
    kl_values.append(kl_divergence(p_base, q_test))
    js_values.append(js_divergence(p_base, q_test))

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(differences, kl_values, 'b-', label='KL Divergence', linewidth=2)
plt.plot(differences, js_values, 'r-', label='JS Divergence', linewidth=2)
plt.xlabel('Difference between distributions')
plt.ylabel('Divergence Value')
plt.title('KL vs JS Divergence')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
# Show the asymmetry of KL
p_asym = np.array([0.7, 0.3])
q_asym = np.array([0.4, 0.6])

kl_pq = kl_divergence(p_asym, q_asym)
kl_qp = kl_divergence(q_asym, p_asym)
js_both = js_divergence(p_asym, q_asym)

categories = ['P → Q', 'Q → P', 'JS(P,Q)']
values = [kl_pq, kl_qp, js_both]
colors = ['red', 'blue', 'green']

plt.bar(categories, values, color=colors, alpha=0.7)
plt.ylabel('Divergence Value')
plt.title('KL Asymmetry vs JS Symmetry')
for i, v in enumerate(values):
    plt.text(i, v + 0.01, f'{v:.3f}', ha='center')

plt.tight_layout()
plt.show()

# =============================================================================
# 5. REAL-WORLD ANALOGIES
# =============================================================================
print("\n" + "=" * 70)
print("REAL-WORLD ANALOGIES")
print("=" * 70)

print("""
KL DIVERGENCE (Asymmetric):
→ "How surprised would a WEATHER FORECASTER be if they predicted 
   80% sun but it rained all week?"
   
   KL(Prediction||Reality) = High surprise!
   KL(Reality||Prediction) = Different calculation!

JS DIVERGENCE (Symmetric):  
→ "How different are the WEATHER PATTERNS in Seattle vs Miami?"
   
   Same result regardless of which city you put first!
""")

# =============================================================================
# 6. WHEN TO USE WHICH?
# =============================================================================
print("\n" + "=" * 70)
print("WHEN TO USE WHICH?")
print("=" * 70)

use_cases = [
    {
        "situation": "You have a TRUE distribution and a PREDICTED distribution",
        "recommendation": "KL DIVERGENCE",
        "reason": "Measures how 'wrong' the prediction is from truth"
    },
    {
        "situation": "Comparing TWO distributions without 'true' vs 'predicted'",
        "recommendation": "JS DIVERGENCE", 
        "reason": "Symmetric - gives same result either way"
    },
    {
        "situation": "Distributions might have ZERO probabilities",
        "recommendation": "JS DIVERGENCE",
        "reason": "Handles zeros gracefully (KL can be infinite)"
    },
    {
        "situation": "You need results between 0 and 1",
        "recommendation": "JS DIVERGENCE",
        "reason": "Always between 0 (same) and 1 (completely different)"
    },
    {
        "situation": "Information theory applications",
        "recommendation": "KL DIVERGENCE", 
        "reason": "Direct interpretation as 'bits of surprise'"
    }
]

print("\nDECISION GUIDE:")
print("-" * 80)
for i, case in enumerate(use_cases, 1):
    print(f"\n{i}. {case['situation']}")
    print(f"   → USE: {case['recommendation']}")
    print(f"   💡 {case['reason']}")

# =============================================================================
# 7. PRACTICAL EXAMPLE: Data Drift Detection
# =============================================================================
print("\n" + "=" * 70)
print("PRACTICAL EXAMPLE: Data Drift Detection")
print("=" * 70)

# Simulate feature distributions over time
print("\nMonitoring customer age distribution changes:")

# Month 1: Mostly young customers
month1 = np.array([0.6, 0.3, 0.1])  # Young: 60%, Middle: 30%, Senior: 10%

# Month 2: Distribution shifted
month2 = np.array([0.3, 0.4, 0.3])  # Young: 30%, Middle: 40%, Senior: 30%

age_groups = ['Young', 'Middle', 'Senior']

# Calculate both divergences
kl_drift = kl_divergence(month1, month2)
js_drift = js_divergence(month1, month2)

print(f"Month 1: {month1}")
print(f"Month 2: {month2}")
print(f"KL Divergence: {kl_drift:.4f}")
print(f"JS Divergence: {js_drift:.4f}")

# Plot the comparison
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
x_pos = np.arange(len(age_groups))
width = 0.35
plt.bar(x_pos - width/2, month1, width, label='Month 1', alpha=0.7)
plt.bar(x_pos + width/2, month2, width, label='Month 2', alpha=0.7)
plt.xticks(x_pos, age_groups)
plt.ylabel('Proportion')
plt.title('Customer Age Distribution Change')
plt.legend()

plt.subplot(1, 2, 2)
divergences = [kl_drift, js_drift]
labels = ['KL Divergence', 'JS Divergence']
colors = ['red', 'blue']
plt.bar(labels, divergences, color=colors, alpha=0.7)
plt.ylabel('Divergence Value')
plt.title('Data Drift Detection')
for i, v in enumerate(divergences):
    plt.text(i, v + 0.01, f'{v:.3f}', ha='center')

plt.tight_layout()
plt.show()

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print("""
KL DIVERGENCE:
✓ Asymmetric: KL(P||Q) ≠ KL(Q||P)
✓ Can be infinite if Q has zeros where P doesn't
✓ Interpretation: "Surprise when expecting P but seeing Q"
✓ Common in: Information theory, machine learning loss functions

JS DIVERGENCE:
✓ Symmetric: JS(P,Q) = JS(Q,P)  
✓ Always between 0 and 1
✓ Handles zero probabilities gracefully
✓ Interpretation: "Average difference between distributions"
✓ Common in: Distribution comparison, clustering, data drift
""")

"""
======================================================================
KL DIVERGENCE vs JS DIVERGENCE
======================================================================

1. KL DIVERGENCE (Kullback-Leibler)
   → 'How SURPRISED would you be if you expected P but saw Q?'

--- EXAMPLE 1: Small Difference ---
Expected: [0.4 0.3 0.3]
Actual:   [0.35 0.35 0.3 ]
KL(P||Q) = 0.007167

--- EXAMPLE 2: Large Difference ---
Expected: [0.8 0.2]
Actual:   [0.2 0.8]
KL(P||Q) = 0.831777

2. JS DIVERGENCE (Jensen-Shannon)
   → 'How different are P and Q on average?'

--- EXAMPLE 1: Small Difference ---
Expected: [0.4 0.3 0.3]
Actual:   [0.35 0.35 0.3 ]
JS(P,Q) = 0.042384

--- EXAMPLE 2: Large Difference ---
Expected: [0.8 0.2]
Actual:   [0.2 0.8]
JS(P,Q) = 0.439027

======================================================================
KEY DIFFERENCES
======================================================================

COMPARISON TABLE:
--------------------------------------------------------------------------------
Case                 KL(P||Q)     KL(Q||P)     JS(P,Q)      Symmetric?
--------------------------------------------------------------------------------
Identical Distributions 0.000000     0.000000     0.000000     Yes
Small Difference     0.005094     0.005146     0.035768     NO!
Large Difference     1.757780     1.757780     0.606683     Yes
Zero in Q (KL problem) 10.819778    0.693147     0.464501     NO!

======================================================================
VISUAL COMPARISON
======================================================================


======================================================================
REAL-WORLD ANALOGIES
======================================================================

KL DIVERGENCE (Asymmetric):
→ "How surprised would a WEATHER FORECASTER be if they predicted 
   80% sun but it rained all week?"
   
   KL(Prediction||Reality) = High surprise!
   KL(Reality||Prediction) = Different calculation!

JS DIVERGENCE (Symmetric):  
→ "How different are the WEATHER PATTERNS in Seattle vs Miami?"
   
   Same result regardless of which city you put first!


======================================================================
WHEN TO USE WHICH?
======================================================================

DECISION GUIDE:
--------------------------------------------------------------------------------

1. You have a TRUE distribution and a PREDICTED distribution
   → USE: KL DIVERGENCE
   💡 Measures how 'wrong' the prediction is from truth

2. Comparing TWO distributions without 'true' vs 'predicted'
   → USE: JS DIVERGENCE
   💡 Symmetric - gives same result either way

3. Distributions might have ZERO probabilities
   → USE: JS DIVERGENCE
   💡 Handles zeros gracefully (KL can be infinite)

4. You need results between 0 and 1
   → USE: JS DIVERGENCE
   💡 Always between 0 (same) and 1 (completely different)

5. Information theory applications
   → USE: KL DIVERGENCE
   💡 Direct interpretation as 'bits of surprise'

======================================================================
PRACTICAL EXAMPLE: Data Drift Detection
======================================================================

Monitoring customer age distribution changes:
Month 1: [0.6 0.3 0.1]
Month 2: [0.3 0.4 0.3]
KL Divergence: 0.2197
JS Divergence: 0.2350


======================================================================
SUMMARY
======================================================================

KL DIVERGENCE:
✓ Asymmetric: KL(P||Q) ≠ KL(Q||P)
✓ Can be infinite if Q has zeros where P doesn't
✓ Interpretation: "Surprise when expecting P but seeing Q"
✓ Common in: Information theory, machine learning loss functions

JS DIVERGENCE:
✓ Symmetric: JS(P,Q) = JS(Q,P)  
✓ Always between 0 and 1
✓ Handles zero probabilities gracefully
✓ Interpretation: "Average difference between distributions"
✓ Common in: Distribution comparison, clustering, data drift

"""