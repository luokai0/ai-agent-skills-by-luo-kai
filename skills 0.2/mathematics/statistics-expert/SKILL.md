---
name: statistics-expert
description: Expert-level statistics knowledge. Use when working with probability distributions, hypothesis testing, regression, Bayesian statistics, statistical inference, experimental design, ANOVA, or statistical modeling. Also use when the user mentions 'p-value', 'confidence interval', 'hypothesis test', 'regression', 'ANOVA', 'chi-square', 't-test', 'Bayesian', 'maximum likelihood', 'statistical significance', 'correlation', 'normal distribution', or 'sampling distribution'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Statistics Expert

You are a world-class statistician with deep expertise in probability theory, statistical inference, regression analysis, Bayesian statistics, experimental design, multivariate statistics, and applied statistical modeling.

## Before Starting

1. **Topic** — Probability, inference, regression, Bayesian, or experimental design?
2. **Level** — Introductory, undergraduate, or graduate?
3. **Goal** — Analyze data, design study, test hypothesis, or build model?
4. **Context** — Scientific research, industry, medical, or social science?
5. **Approach** — Frequentist or Bayesian?

---

## Core Expertise Areas

- **Probability**: distributions, expectation, variance, central limit theorem
- **Statistical Inference**: estimation, hypothesis testing, confidence intervals
- **Regression**: simple, multiple, logistic, nonlinear
- **ANOVA & Experimental Design**: factorial designs, blocking, mixed models
- **Bayesian Statistics**: priors, posteriors, MCMC, credible intervals
- **Nonparametric Methods**: rank tests, permutation tests, bootstrap
- **Multivariate Statistics**: PCA, cluster analysis, discriminant analysis
- **Time Series**: stationarity, ARIMA, forecasting

---

## Probability Foundations
```python
def probability_distributions():
    return {
        'Discrete Distributions': {
            'Bernoulli(p)': {
                'PMF':      'P(X=1) = p, P(X=0) = 1-p',
                'Mean':     'p',
                'Variance': 'p(1-p)',
                'use':      'Binary outcome (success/failure)'
            },
            'Binomial(n,p)': {
                'PMF':      'C(n,k)·pᵏ·(1-p)^(n-k)',
                'Mean':     'np',
                'Variance': 'np(1-p)',
                'use':      'Number of successes in n trials'
            },
            'Poisson(λ)': {
                'PMF':      'e^(-λ)·λᵏ/k!',
                'Mean':     'λ',
                'Variance': 'λ',
                'use':      'Count of rare events in fixed interval'
            },
            'Geometric(p)': {
                'PMF':      'p(1-p)^(k-1)',
                'Mean':     '1/p',
                'Variance': '(1-p)/p²',
                'use':      'Number of trials until first success'
            },
            'Hypergeometric': {
                'use':      'Sampling without replacement from finite population'
            },
            'Negative Binomial': {
                'use':      'Number of trials until r successes'
            }
        },
        'Continuous Distributions': {
            'Uniform(a,b)': {
                'PDF':      '1/(b-a) for x∈[a,b]',
                'Mean':     '(a+b)/2',
                'Variance': '(b-a)²/12'
            },
            'Normal(μ,σ²)': {
                'PDF':      '(1/σ√2π)exp(-(x-μ)²/2σ²)',
                'Mean':     'μ',
                'Variance': 'σ²',
                'use':      'Central limit theorem, natural phenomena'
            },
            'Exponential(λ)': {
                'PDF':      'λe^(-λx)',
                'Mean':     '1/λ',
                'Variance': '1/λ²',
                'memoryless':'P(X>s+t|X>s) = P(X>t)',
                'use':      'Time between Poisson events'
            },
            'Gamma(α,β)': {
                'use':      'Sum of exponentials, waiting times',
                'special':  'Exponential: α=1; Chi-squared: β=2, α=k/2'
            },
            'Beta(α,β)': {
                'support':  '[0,1]',
                'use':      'Prior for probabilities, proportions',
                'Mean':     'α/(α+β)'
            },
            't-distribution': {
                'use':      'Small samples with unknown σ',
                'heavy_tails':'More robust than normal'
            },
            'Chi-squared(k)': {
                'use':      'Sum of k squared standard normals',
                'applications':'Goodness of fit, independence tests'
            },
            'F-distribution': {
                'use':      'Ratio of chi-squared variables, ANOVA'
            }
        }
    }

def key_theorems():
    return {
        'Law of Large Numbers': {
            'weak':     'Sample mean converges in probability to μ',
            'strong':   'Sample mean converges almost surely to μ'
        },
        'Central Limit Theorem': {
            'statement':'√n(X̄-μ)/σ → N(0,1) as n→∞',
            'practical':'n≥30 usually sufficient (skewed: more)',
            'power':    'Justifies normal-based inference for means'
        },
        'Law of Total Probability': {
            'formula':  'P(A) = Σ P(A|Bᵢ)P(Bᵢ)',
            'use':      'Decompose complex probabilities'
        },
        'Bayes Theorem': {
            'formula':  'P(A|B) = P(B|A)P(A)/P(B)',
            'use':      'Update beliefs with new evidence'
        }
    }
```

---

## Statistical Inference

### Point Estimation
```
Estimator properties:
  Unbiased: E[θ̂] = θ
  Consistent: θ̂ →ₚ θ as n→∞
  Efficient: minimum variance among unbiased estimators
  Sufficient: captures all information about θ in data

Maximum Likelihood Estimation (MLE):
  L(θ) = Π f(xᵢ|θ)  (likelihood function)
  ℓ(θ) = Σ log f(xᵢ|θ)  (log-likelihood, easier to maximize)
  θ̂_MLE: ∂ℓ/∂θ = 0  (score equation)

Properties of MLE:
  Consistent: θ̂_MLE →ₚ θ
  Asymptotically normal: √n(θ̂-θ) → N(0, I(θ)⁻¹)
  Asymptotically efficient: achieves Cramér-Rao bound
  Invariant: f(θ̂_MLE) = f̂_MLE

Method of Moments:
  Set sample moments = population moments
  Solve for parameters
  Less efficient than MLE but simpler
```

### Confidence Intervals
```
Definition: 95% CI contains true parameter in 95% of repeated experiments
(NOT: 95% probability parameter is in this interval)

Z-interval for μ (σ known):
  x̄ ± z_{α/2} · σ/√n
  z_{0.025} = 1.96 for 95% CI

t-interval for μ (σ unknown):
  x̄ ± t_{α/2,n-1} · s/√n
  t_{0.025,29} ≈ 2.045 for n=30

For proportion p:
  p̂ ± z_{α/2}√(p̂(1-p̂)/n)
  Wilson interval (better for small samples)

Margin of error: E = z_{α/2} · σ/√n
Sample size: n = (z_{α/2} · σ/E)²

Interpretation:
  "We are 95% confident the true parameter lies in [L, U]"
  NOT "95% chance parameter is in [L, U]" (frequentist)
```

### Hypothesis Testing
```python
def hypothesis_testing_framework():
    return {
        'Framework': {
            'H₀':           'Null hypothesis (status quo, no effect)',
            'H₁ or Hₐ':     'Alternative hypothesis (what we want to show)',
            'Test statistic':'Measure of evidence against H₀',
            'p-value':       'P(test stat as extreme or more | H₀ true)',
            'α':             'Significance level (Type I error rate, usually 0.05)',
            'Decision':      'Reject H₀ if p-value < α'
        },
        'Error types': {
            'Type I (α)':   'Reject H₀ when true (false positive)',
            'Type II (β)':  'Fail to reject H₀ when false (false negative)',
            'Power (1-β)':  'Probability of detecting true effect',
            'Trade-off':    'Decreasing α increases β (for fixed n)'
        },
        'One-sample z-test': {
            'H₀':           'μ = μ₀',
            'Test stat':    'z = (x̄ - μ₀)/(σ/√n)',
            'Use when':     'σ known, n large'
        },
        'One-sample t-test': {
            'H₀':           'μ = μ₀',
            'Test stat':    't = (x̄ - μ₀)/(s/√n)',
            'df':           'n-1',
            'Use when':     'σ unknown, normal population'
        },
        'Two-sample t-test': {
            'H₀':           'μ₁ = μ₂',
            'pooled':        't = (x̄₁-x̄₂)/(sp√(1/n₁+1/n₂)), df=n₁+n₂-2',
            'Welch':         't = (x̄₁-x̄₂)/√(s₁²/n₁+s₂²/n₂), df=Satterthwaite',
            'Use pooled when':'Equal variances (test with Levene/F-test first)'
        },
        'Paired t-test': {
            'H₀':           'μd = 0 (mean difference = 0)',
            'Test stat':    't = d̄/(sd/√n), df = n-1',
            'Use when':     'Matched pairs (before/after, siblings)'
        },
        'Chi-square goodness of fit': {
            'H₀':           'Data follows specified distribution',
            'Test stat':    'χ² = Σ(O-E)²/E',
            'df':           'k-1-p (k categories, p estimated params)'
        },
        'Chi-square independence': {
            'H₀':           'Two categorical variables independent',
            'Test stat':    'χ² = Σ(Oᵢⱼ-Eᵢⱼ)²/Eᵢⱼ',
            'Eᵢⱼ':          'Row total × Col total / Grand total',
            'df':           '(r-1)(c-1)'
        }
    }
```

---

## Regression Analysis
```python
def regression_models():
    return {
        'Simple Linear Regression': {
            'model':        'Y = β₀ + β₁X + ε',
            'OLS estimates':'β̂₁ = Sxy/Sxx, β̂₀ = ȳ - β̂₁x̄',
            'Sxy':          'Σ(xᵢ-x̄)(yᵢ-ȳ)',
            'Sxx':          'Σ(xᵢ-x̄)²',
            'R²':           'SSR/SST = 1 - SSE/SST (proportion variance explained)',
            'r':            '√R² × sign(β̂₁) = Pearson correlation',
            'assumptions':  'LINEAR, INDEPENDENCE, NORMALITY, EQUAL VARIANCE (LINE)'
        },
        'Multiple Linear Regression': {
            'model':        'Y = β₀ + β₁X₁ + ... + βₖXₖ + ε',
            'matrix':       'β̂ = (XᵀX)⁻¹Xᵀy',
            'R²':           'Always increases with more predictors',
            'Adj R²':       '1-(1-R²)(n-1)/(n-k-1) (penalizes extra vars)',
            'F-test':       'Tests H₀: all β = 0 (overall significance)',
            'VIF':          'Variance Inflation Factor (>10 = problematic multicollinearity)'
        },
        'Diagnostics': {
            'Residual plots':  'vs fitted (homoscedasticity), vs order (independence)',
            'QQ plot':         'Check normality of residuals',
            'Leverage':        'hᵢᵢ = Xᵢ(XᵀX)⁻¹Xᵢᵀ (> 2k/n is high)',
            'Cooks distance':  'Influence of single observation (>1 concerns)',
            'DFFITS':          'Change in fit when obs removed'
        },
        'Logistic Regression': {
            'model':        'log(p/(1-p)) = β₀ + β₁X₁ + ...',
            'logit':        'log(odds) = log(p/(1-p))',
            'probability':  'p = 1/(1+e^(-Xβ))',
            'fitting':      'Maximum likelihood (no closed form)',
            'OR':           'Odds ratio = exp(βⱼ) per unit increase in Xⱼ',
            'deviance':     '-2 log-likelihood (analogous to SSE)',
            'pseudo-R²':    "McFadden's: 1 - LL_full/LL_null"
        },
        'Model selection': {
            'AIC':          '-2LL + 2k (lower is better)',
            'BIC':          '-2LL + k·ln(n) (heavier penalty for complexity)',
            'Cross-validation':'K-fold CV for prediction performance',
            'Lasso':        'L1 penalty: β̂ = argmin(||y-Xβ||² + λΣ|βⱼ|) → sparse',
            'Ridge':        'L2 penalty: β̂ = (XᵀX + λI)⁻¹Xᵀy → shrinkage'
        }
    }
```

---

## ANOVA
```
One-way ANOVA:
  H₀: μ₁ = μ₂ = ... = μₖ (all group means equal)
  Decomposition: SST = SSB + SSW
    SST = Σᵢⱼ(yᵢⱼ - ȳ..)²  (total)
    SSB = Σᵢ nᵢ(ȳᵢ. - ȳ..)²  (between groups)
    SSW = Σᵢⱼ(yᵢⱼ - ȳᵢ.)²  (within groups/error)

  F = (SSB/(k-1)) / (SSW/(N-k)) = MSB/MSW
  Under H₀: F ~ F(k-1, N-k)
  Reject H₀ if F > F_{α, k-1, N-k}

Assumptions:
  Independence, normality (within groups), equal variances
  Levene test for homogeneity of variance

Post-hoc tests (if ANOVA significant):
  Tukey HSD: controls family-wise error rate
  Bonferroni: conservative, adjust α by number of tests
  Scheffe: very conservative, flexible
  Fisher LSD: liberal (no ANOVA protection needed)

Two-way ANOVA:
  Factors A and B, interaction term A×B
  Test: main effect A, main effect B, interaction A×B
  If interaction significant: interpret with care

Effect size:
  η² = SSB/SST  (eta-squared, proportion variance explained)
  ω² = (SSB - (k-1)MSW)/(SST + MSW)  (omega-squared, less biased)
  Cohen's f: small=0.1, medium=0.25, large=0.4
```

---

## Bayesian Statistics
```python
def bayesian_framework():
    return {
        'Bayes Theorem': {
            'formula':      'p(θ|data) ∝ p(data|θ) × p(θ)',
            'posterior':    'p(θ|data): updated belief about θ',
            'likelihood':   'p(data|θ): probability of data given θ',
            'prior':        'p(θ): belief about θ before data',
            'evidence':     'p(data): normalizing constant'
        },
        'Conjugate priors': {
            'Beta-Binomial':    'Beta prior + Binomial likelihood = Beta posterior',
            'Normal-Normal':    'Normal prior + Normal likelihood = Normal posterior',
            'Gamma-Poisson':    'Gamma prior + Poisson likelihood = Gamma posterior',
            'Dirichlet-Multinom':'Dirichlet prior + Multinomial = Dirichlet posterior',
            'advantage':        'Closed-form posterior (no MCMC needed)'
        },
        'Prior selection': {
            'Informative':  'Encodes strong prior knowledge',
            'Weakly informative': 'Regularizes without strong beliefs (recommended)',
            'Non-informative': 'Jeffreys prior: invariant to reparametrization',
            'Flat':         'Uniform — NOT truly non-informative'
        },
        'Posterior summaries': {
            'MAP':          'Maximum a posteriori: mode of posterior',
            'Posterior mean':'E[θ|data]',
            'Credible interval': '95% CI: P(a≤θ≤b|data) = 0.95 (TRUE probability!)',
            'HDI':          'Highest density interval: shortest credible interval'
        },
        'MCMC (Markov Chain Monte Carlo)': {
            'Metropolis-Hastings': 'Accept/reject proposals',
            'Gibbs sampling':      'Sample each parameter conditional on others',
            'HMC':                 'Hamiltonian Monte Carlo: efficient for continuous',
            'NUTS':                'No-U-Turn Sampler: adaptive HMC (Stan, PyMC)',
            'Diagnostics':         'R̂ (< 1.01), effective sample size, trace plots'
        },
        'Software': {
            'Stan':     'Probabilistic programming, HMC/NUTS, R or Python',
            'PyMC':     'Python, NUTS, user-friendly',
            'JAGS':     'Just Another Gibbs Sampler',
            'brms':     'R, Bayesian regression using Stan'
        }
    }
```

---

## Nonparametric Methods
```
When to use:
  Non-normal data, small samples, ordinal data, robust analysis

Mann-Whitney U test:
  Nonparametric alternative to two-sample t-test
  Tests whether one distribution stochastically dominates
  Uses ranks of combined sample

Wilcoxon signed-rank test:
  Nonparametric alternative to paired t-test
  Tests whether median difference = 0

Kruskal-Wallis test:
  Nonparametric alternative to one-way ANOVA
  Tests whether k groups have same distribution

Spearman correlation:
  rs = Pearson correlation of ranks
  Robust to outliers, detects monotonic relationships
  Test H₀: ρs = 0 using t-distribution

Bootstrap:
  Resample with replacement from sample
  Estimate sampling distribution empirically
  Bootstrap CI: percentile, BCa, or t-bootstrap

Permutation tests:
  Permute labels/values, compute test statistic
  p-value = proportion of permutations with stat ≥ observed
  Exact test, no distributional assumptions
```

---

## Power Analysis & Sample Size
```python
def power_analysis():
    return {
        'Components': {
            'α':        'Type I error rate (usually 0.05)',
            'β':        'Type II error rate',
            '1-β':      'Power (usually 0.80 or 0.90)',
            'effect_size': 'Magnitude of difference to detect',
            'n':        'Sample size (solve for this)'
        },
        'Effect sizes': {
            'Cohens_d':     'd = (μ₁-μ₂)/σ  (small:0.2, medium:0.5, large:0.8)',
            'Cohens_f':     'For ANOVA  (small:0.1, medium:0.25, large:0.4)',
            'Cohens_w':     'For chi-square',
            'r':            'Correlation  (small:0.1, medium:0.3, large:0.5)'
        },
        'Sample size for t-test': {
            'formula':      'n = 2(z_α/2 + z_β)²σ²/δ² per group',
            'practical':    'Use G*Power, pwr package (R), scipy.stats.power'
        },
        'Multiple testing': {
            'Problem':      'Testing m hypotheses: P(≥1 false positive) = 1-(1-α)ᵐ',
            'Bonferroni':   'Reject if p < α/m (controls FWER, conservative)',
            'Holm':         'Stepdown Bonferroni (less conservative)',
            'BH':           'Benjamini-Hochberg: controls FDR at level α',
            'FDR':          'Expected proportion of false discoveries among rejections'
        }
    }
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| p-value = probability H₀ true | p-value = P(data this extreme or more | H₀ true) |
| Fail to reject = accept H₀ | Absence of evidence ≠ evidence of absence |
| 95% CI contains parameter 95% of time | Correct! But not: 95% prob this specific CI contains it |
| Correlation = causation | Correlation only; need experiments for causation |
| Multiple testing ignored | Apply Bonferroni, BH, or Holm correction |
| Normality assumed for large n | CLT justifies, but check for extreme outliers/skew |
| Significant = important | Statistical significance ≠ practical significance (check effect size) |

---

## Related Skills

- **probability-expert**: Deeper probability theory
- **linear-algebra-expert**: Matrix algebra for regression
- **machine-learning-expert**: Predictive modeling methods
- **calculus-expert**: Mathematical foundations
- **experimental-design-expert**: Study design principles
- **data-science-expert**: Applied statistical analysis
