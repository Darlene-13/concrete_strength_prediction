# Correlation Analysis Full Interpretation

This section evaluates the correlation between engineered and raw features against the target variable Concrete Compressive Strength. The goal is to validate whether domain driven feature engineering improved predictive signal compared to raw measurements.

---

# Top 5 Strongest Predictors

| Rank | Feature                | Correlation | Type       |
| ---- | ---------------------- | ----------- | ---------- |
| 1    | cement_age_interaction | +0.701      | Engineered |
| 2    | water_binder_ratio     | -0.611      | Engineered |
| 3    | total_binder_content   | +0.598      | Engineered |
| 4    | agg_binder_ratio       | -0.555      | Engineered |
| 5    | log_age                | +0.560      | Engineered |

Key Insight

Every single top 5 feature is engineered. Not one raw feature made it into the top 5.

This is clear validation that domain driven feature engineering worked as intended.

---

# Bottom 5 Weakest Predictors

| Rank | Feature                | Correlation | Notes             |
| ---- | ---------------------- | ----------- | ----------------- |
| 1    | slag_ratio             | +0.003      | Essentially zero  |
| 2    | flyash_flag            | -0.034      | Near zero         |
| 3    | flyash_age_interaction | +0.043      | Surprisingly weak |
| 4    | cement_ratio           | +0.111      | Weak              |
| 5    | Blast Furnace Slag raw | +0.103      | Weak raw feature  |

---

# Parent vs Engineered Feature Comparison

These comparisons confirm that engineered features consistently outperform their raw parents.

cement_age_interaction (+0.701) vs raw Cement (+0.488) with +0.213 improvement
water_binder_ratio (-0.611) vs raw Water (-0.270) with +0.341 improvement
agg_binder_ratio (-0.555) vs raw Coarse (-0.145) and Fine (-0.186) with large improvement
log_age (+0.560) vs raw Age (+0.337) with +0.223 improvement confirming non linearity
water_cement_ratio (-0.489) vs raw Water (-0.270) with strong improvement

These results support the idea that ratio features and interaction terms capture physical relationships better than raw quantities.

---

# Three Findings to Flag

Flag 1. flyash_age_interaction is weak at +0.043

We expected Fly Ash multiplied by log_age to increase strongly. It did flip positive from raw Fly Ash which was negative, but the improvement is small.

The likely reason is distribution. More than half of mixes contain zero Fly Ash. The interaction term is therefore zero for many rows which weakens overall correlation.

This feature may still help tree based models in the subset of mixes that use Fly Ash but it is not globally strong.

Flag 2. slag_ratio is essentially useless at +0.003

The proportion of binder that is slag does not explain strength on its own. Absolute quantity appears to matter more than proportional composition.

This feature is a candidate for removal.

Flag 3. flyash_ratio is weaker than raw Fly Ash

This is the only case where an engineered feature performed worse than its raw parent. Expressing Fly Ash as a fraction of binder reduces useful signal compared to the raw quantity.

This feature should be removed.

---

# Feature Selection Decisions

Keep Strong Engineered Features

cement_age_interaction
water_binder_ratio
total_binder_content
agg_binder_ratio
log_age
water_cement_ratio

Keep Useful Raw Features

Cement
Superplasticizer
Age
Water
Slag
sp_flag
slag_flag
slag_age_interaction

Drop Weak or Redundant Features

slag_ratio
flyash_ratio
flyash_flag
flyash_age_interaction
raw Coarse Aggregate
raw Fine Aggregate
total_aggregate_content

---

# Final Conclusion

The correlation analysis shows that engineered features provide the strongest predictive signal. Domain knowledge improved feature quality and allowed ratios and interaction terms to replace several raw measurements. Removing weak or redundant variables creates a cleaner feature set for modeling.
