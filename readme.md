# statistical_distribution_testing_cookbook

## KS Test: Detects any differences in continuous distributions (shape, location, spread)

![kolmogorov_smirnov_demo_00](kolmogorov_smirnov_demo_00.png)

![kolmogorov_smirnov_demo_01](kolmogorov_smirnov_demo_01.png)

![kolmogorov_smirnov_demo_02](kolmogorov_smirnov_demo_02.png)

![kolmogorov_smirnov_demo_03](kolmogorov_smirnov_demo_03.png)

## Chi-square Test: Detects differences in categorical frequency distributions

![chi_square_demo_00](chi_square_demo_00.png)

![chi_square_demo_01](chi_square_demo_01.png)

![chi_square_demo_02](chi_square_demo_02.png)

# Which Stats Test?

![which_stats_tests_00](which_stats_tests_00.png)

![which_stats_tests_01](which_stats_tests_01.png)

![which_stats_tests_02](which_stats_tests_02.png)

![which_stats_tests_03](which_stats_tests_03.png)

![which_stats_tests_04](which_stats_tests_04.png)


# diff_kl_js_divergence

```
Key Differences:
Symmetry: KL is asymmetric, JS is symmetric

Range: KL can be 0 to ∞, JS is always 0 to 1

Zero handling: KL breaks with zeros, JS handles them

Interpretation: KL = "surprise", JS = "average difference"

Simple Rule:
Use KL when you have "true" vs "predicted"

Use JS when comparing two distributions equally

Use JS when you need consistent, bounded results
```

![diff_kl_js_divergence_00](diff_kl_js_divergence_00.png)

![diff_kl_js_divergence_01](diff_kl_js_divergence_01.png)

