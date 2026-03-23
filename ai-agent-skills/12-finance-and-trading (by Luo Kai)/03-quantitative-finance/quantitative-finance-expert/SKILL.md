---
author: luo-kai
name: quantitative-finance-expert
description: Expert-level quantitative finance and algorithmic trading. Use when working with factor models, statistical arbitrage, backtesting, alpha research, portfolio optimization, time series analysis, machine learning for finance, or building systematic trading strategies. Also use when the user mentions 'alpha factor', 'Sharpe ratio', 'mean reversion', 'momentum factor', 'cointegration', 'pairs trading', 'Monte Carlo', 'portfolio optimization', 'systematic strategy', or 'quant model'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: finance
---

# Quantitative Finance Expert

You are a world-class quantitative analyst with deep expertise in statistical modeling, factor research, algorithmic trading, portfolio optimization, risk modeling, and systematic strategy development.

## Before Starting

1. **Goal** — Alpha research, risk modeling, portfolio optimization, or backtesting?
2. **Asset class** — Equities, futures, forex, crypto, fixed income?
3. **Strategy type** — Mean reversion, momentum, statistical arb, or factor?
4. **Timeframe** — High frequency, daily, or longer horizon?
5. **Tools** — Python, R, MATLAB, or other?

---

## Core Expertise Areas

- **Factor Models**: Fama-French, momentum, quality, low volatility
- **Statistical Arbitrage**: pairs trading, cointegration, mean reversion
- **Portfolio Optimization**: Markowitz, Black-Litterman, risk parity
- **Time Series Analysis**: ARIMA, GARCH, stationarity, autocorrelation
- **Backtesting**: walk-forward, overfitting prevention, realistic simulation
- **Risk Models**: VaR, CVaR, factor exposure, stress testing
- **ML in Finance**: feature engineering, regime detection, prediction
- **Execution**: market impact, slippage, transaction cost analysis

---

## Factor Models

### Fama-French Factor Framework
```python
import pandas as pd
import numpy as np
from scipy import stats

def fama_french_regression(returns, mkt_rf, smb, hml, rf):
    """
    Three-factor model regression.
    Returns alpha (excess return unexplained by factors)
    mkt_rf: market excess return
    smb:    small minus big (size factor)
    hml:    high minus low (value factor)
    """
    excess_returns = returns - rf

    X = pd.DataFrame({
        'mkt_rf': mkt_rf,
        'smb':    smb,
        'hml':    hml
    })
    X = np.column_stack([np.ones(len(X)), X])

    # OLS regression
    coeffs, residuals, _, _ = np.linalg.lstsq(X, excess_returns, rcond=None)

    alpha    = coeffs[0]   # Jensen's alpha
    beta_mkt = coeffs[1]   # market beta
    beta_smb = coeffs[2]   # size exposure
    beta_hml = coeffs[3]   # value exposure

    return {
        'alpha':    round(alpha * 252, 4),   # annualized
        'beta_mkt': round(beta_mkt, 4),
        'beta_smb': round(beta_smb, 4),
        'beta_hml': round(beta_hml, 4),
    }

def factor_definitions():
    return {
        'Market (Beta)':   'Excess return of market over risk-free rate',
        'Size (SMB)':      'Small cap minus large cap returns',
        'Value (HML)':     'High book-to-market minus low (value vs growth)',
        'Momentum (WML)':  'Winners minus losers (12-1 month returns)',
        'Quality (QMJ)':   'Quality minus junk (profitability, growth, safety)',
        'Low Vol (BAB)':   'Betting against beta - low vol outperforms risk-adj',
        'Profitability':   'High gross profit/assets minus low',
        'Investment':      'Low asset growth minus high (conservative vs aggressive)'
    }
```

### Alpha Factor Research
```python
def compute_momentum_factor(prices, lookback=252, skip=21):
    """
    12-1 month momentum: return from 12 months ago to 1 month ago.
    Skip last month to avoid short-term reversal.
    """
    momentum = prices.shift(skip) / prices.shift(lookback) - 1
    return momentum

def compute_value_factor(price, book_value_per_share):
    """Book-to-market ratio — higher = more value."""
    return book_value_per_share / price

def compute_quality_factor(roa, debt_to_equity, gross_margin):
    """Composite quality score."""
    roa_score    = (roa - roa.mean()) / roa.std()
    debt_score   = -(debt_to_equity - debt_to_equity.mean()) / debt_to_equity.std()
    margin_score = (gross_margin - gross_margin.mean()) / gross_margin.std()
    return (roa_score + debt_score + margin_score) / 3

def rank_and_long_short(factor_scores, top_pct=0.2, bottom_pct=0.2):
    """
    Create long-short portfolio from factor scores.
    Long top quintile, short bottom quintile.
    """
    n = len(factor_scores)
    sorted_scores = factor_scores.sort_values()

    short_cutoff = sorted_scores.iloc[int(n * bottom_pct)]
    long_cutoff  = sorted_scores.iloc[int(n * (1 - top_pct))]

    positions = pd.Series(0, index=factor_scores.index)
    positions[factor_scores >= long_cutoff]  =  1 / (factor_scores >= long_cutoff).sum()
    positions[factor_scores <= short_cutoff] = -1 / (factor_scores <= short_cutoff).sum()

    return positions

def information_coefficient(factor_scores, forward_returns):
    """
    IC = rank correlation between factor scores and future returns.
    IC > 0.05 is considered good, > 0.10 is excellent.
    """
    ic, pvalue = stats.spearmanr(factor_scores, forward_returns)
    return {'IC': round(ic, 4), 'p_value': round(pvalue, 4)}
```

---

## Statistical Arbitrage

### Pairs Trading & Cointegration
```python
from statsmodels.tsa.stattools import coint, adfuller
from statsmodels.regression.linear_model import OLS
import statsmodels.api as sm

def find_cointegrated_pairs(prices_df, pvalue_threshold=0.05):
    """Find cointegrated pairs from a universe of assets."""
    n = prices_df.shape[1]
    tickers = prices_df.columns
    pairs = []

    for i in range(n):
        for j in range(i+1, n):
            s1 = prices_df.iloc[:, i]
            s2 = prices_df.iloc[:, j]
            _, pvalue, _ = coint(s1, s2)
            if pvalue < pvalue_threshold:
                pairs.append({
                    'pair':    (tickers[i], tickers[j]),
                    'pvalue':  round(pvalue, 4)
                })

    return sorted(pairs, key=lambda x: x['pvalue'])

def pairs_trading_spread(s1, s2):
    """Calculate hedge ratio and spread for pairs trade."""
    model = OLS(s1, sm.add_constant(s2)).fit()
    hedge_ratio = model.params[1]
    spread = s1 - hedge_ratio * s2

    # Normalize spread to z-score
    zscore = (spread - spread.mean()) / spread.std()
    return spread, zscore, hedge_ratio

def pairs_signals(zscore, entry_z=2.0, exit_z=0.5):
    """
    Generate trading signals from spread z-score.
    Short spread when z > entry_z (overvalued)
    Long spread when z < -entry_z (undervalued)
    Exit when z crosses exit_z
    """
    signals = pd.Series(0, index=zscore.index)
    position = 0

    for i in range(len(zscore)):
        z = zscore.iloc[i]
        if position == 0:
            if z > entry_z:   position = -1   # short spread
            elif z < -entry_z: position = 1   # long spread
        elif position == 1 and z > -exit_z:
            position = 0
        elif position == -1 and z < exit_z:
            position = 0
        signals.iloc[i] = position

    return signals

def adf_test(series, significance=0.05):
    """Augmented Dickey-Fuller test for stationarity."""
    result = adfuller(series.dropna())
    return {
        'statistic':   round(result[0], 4),
        'pvalue':      round(result[1], 4),
        'is_stationary': result[1] < significance,
        'critical_1%': round(result[4]['1%'], 4),
        'critical_5%': round(result[4]['5%'], 4),
    }
```

---

## Portfolio Optimization

### Mean-Variance Optimization (Markowitz)
```python
from scipy.optimize import minimize

def portfolio_stats(weights, returns, cov_matrix):
    weights = np.array(weights)
    port_return = np.sum(returns.mean() * weights) * 252
    port_vol    = np.sqrt(weights @ cov_matrix @ weights) * np.sqrt(252)
    sharpe      = port_return / port_vol
    return port_return, port_vol, sharpe

def max_sharpe_portfolio(returns, risk_free=0.05):
    """Find portfolio weights that maximize Sharpe ratio."""
    n = returns.shape[1]
    cov = returns.cov() * 252
    mean_returns = returns.mean() * 252

    def neg_sharpe(weights):
        r, v, _ = portfolio_stats(weights, returns, cov)
        return -(r - risk_free) / v

    constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
    bounds = tuple((0, 1) for _ in range(n))
    init   = np.array([1/n] * n)

    result = minimize(neg_sharpe, init, method='SLSQP',
                      bounds=bounds, constraints=constraints)
    return result.x

def min_variance_portfolio(returns):
    """Find minimum variance portfolio weights."""
    n = returns.shape[1]
    cov = returns.cov() * 252

    def portfolio_vol(weights):
        return np.sqrt(np.array(weights) @ cov @ np.array(weights))

    constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
    bounds = tuple((0, 1) for _ in range(n))
    init   = np.array([1/n] * n)

    result = minimize(portfolio_vol, init, method='SLSQP',
                      bounds=bounds, constraints=constraints)
    return result.x

def risk_parity_portfolio(returns):
    """
    Equal risk contribution portfolio.
    Each asset contributes equally to total portfolio risk.
    """
    n = returns.shape[1]
    cov = returns.cov() * 252

    def risk_contribution_error(weights):
        weights = np.array(weights)
        port_var   = weights @ cov @ weights
        marginal_rc = cov @ weights
        risk_contrib = weights * marginal_rc / port_var
        target = np.ones(n) / n  # equal contribution
        return np.sum((risk_contrib - target) ** 2)

    constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
    bounds = tuple((0.01, 1) for _ in range(n))
    init   = np.array([1/n] * n)

    result = minimize(risk_contribution_error, init,
                      method='SLSQP', bounds=bounds, constraints=constraints)
    return result.x
```

---

## Time Series Analysis

### Stationarity & ARIMA
```python
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings

def make_stationary(series):
    """Transform series to stationary via differencing."""
    d = 0
    current = series.copy()

    while adfuller(current.dropna())[1] > 0.05 and d < 3:
        current = current.diff()
        d += 1

    return current, d

def fit_arima(series, order=(1,1,1)):
    """Fit ARIMA model and return forecast."""
    warnings.filterwarnings('ignore')
    model = ARIMA(series, order=order).fit()
    forecast = model.forecast(steps=5)
    return {
        'aic':      round(model.aic, 2),
        'bic':      round(model.bic, 2),
        'forecast': forecast.round(4).tolist(),
        'summary':  model.summary()
    }

def garch_volatility(returns, p=1, q=1):
    """GARCH(1,1) volatility model for financial returns."""
    from arch import arch_model
    model = arch_model(returns * 100, vol='Garch', p=p, q=q)
    result = model.fit(disp='off')
    conditional_vol = result.conditional_volatility / 100
    return {
        'current_vol':     round(conditional_vol.iloc[-1], 6),
        'annualized_vol':  round(conditional_vol.iloc[-1] * np.sqrt(252), 4),
        'vol_forecast':    result.forecast(horizon=5)
    }

def autocorrelation_test(returns, lags=20):
    """Ljung-Box test for autocorrelation (return predictability)."""
    from statsmodels.stats.diagnostic import acorr_ljungbox
    result = acorr_ljungbox(returns, lags=lags, return_df=True)
    significant = result[result['lb_pvalue'] < 0.05]
    return {
        'has_autocorrelation': len(significant) > 0,
        'significant_lags': significant.index.tolist()
    }
```

---

## Backtesting Framework
```python
def vectorized_backtest(prices, signals, commission=0.001, slippage=0.0005):
    """
    Vectorized backtest with realistic costs.
    signals: +1 long, -1 short, 0 flat
    """
    df = pd.DataFrame({'price': prices, 'signal': signals})
    df['position']    = df['signal'].shift(1)  # trade next bar
    df['returns']     = df['price'].pct_change()
    df['gross_ret']   = df['position'] * df['returns']

    # Transaction costs
    df['trade']       = df['position'].diff().abs()
    df['costs']       = df['trade'] * (commission + slippage)
    df['net_ret']     = df['gross_ret'] - df['costs']

    equity = (1 + df['net_ret']).cumprod()

    # Performance metrics
    ann_return  = df['net_ret'].mean() * 252
    ann_vol     = df['net_ret'].std() * np.sqrt(252)
    sharpe      = ann_return / ann_vol
    peak        = equity.cummax()
    drawdown    = (equity - peak) / peak
    max_dd      = drawdown.min()
    calmar      = ann_return / abs(max_dd)

    # Win rate
    trades      = df[df['trade'] > 0]
    win_rate    = (df['net_ret'][df['position'] != 0] > 0).mean()

    return {
        'annual_return':  round(ann_return * 100, 2),
        'annual_vol':     round(ann_vol * 100, 2),
        'sharpe_ratio':   round(sharpe, 3),
        'max_drawdown':   round(max_dd * 100, 2),
        'calmar_ratio':   round(calmar, 3),
        'win_rate':       round(win_rate * 100, 2),
        'num_trades':     int(df['trade'].sum()),
        'equity_curve':   equity
    }

def walk_forward_test(prices, signal_fn, train_window=252, test_window=63):
    """
    Walk-forward testing to prevent overfitting.
    Train on in-sample, test on out-of-sample, roll forward.
    """
    results = []
    n = len(prices)

    for start in range(0, n - train_window - test_window, test_window):
        train_end  = start + train_window
        test_end   = train_end + test_window

        train_data = prices.iloc[start:train_end]
        test_data  = prices.iloc[train_end:test_end]

        # Fit/optimize on train, evaluate on test
        optimized_params = signal_fn.optimize(train_data)
        signals = signal_fn.generate(test_data, optimized_params)
        result  = vectorized_backtest(test_data, signals)
        results.append(result)

    return pd.DataFrame(results)

def overfitting_checks(in_sample, out_of_sample):
    """Check for overfitting by comparing IS vs OOS performance."""
    degradation = (in_sample['sharpe_ratio'] - out_of_sample['sharpe_ratio'])
    degradation_pct = degradation / in_sample['sharpe_ratio'] * 100

    return {
        'is_sharpe':       in_sample['sharpe_ratio'],
        'oos_sharpe':      out_of_sample['sharpe_ratio'],
        'degradation_pct': round(degradation_pct, 1),
        'likely_overfit':  degradation_pct > 50
    }
```

---

## Risk Models
```python
def value_at_risk(returns, confidence=0.95, method='historical'):
    """Calculate VaR using historical or parametric method."""
    if method == 'historical':
        var = -returns.quantile(1 - confidence)
    else:  # parametric
        from scipy.stats import norm
        var = -returns.mean() + norm.ppf(confidence) * returns.std()
    return round(var, 6)

def conditional_var(returns, confidence=0.95):
    """CVaR / Expected Shortfall — average loss beyond VaR."""
    var = value_at_risk(returns, confidence)
    tail_losses = returns[returns < -var]
    return round(-tail_losses.mean(), 6)

def monte_carlo_var(portfolio_value, daily_return, daily_vol,
                    days=252, simulations=10000, confidence=0.95):
    """Monte Carlo simulation for portfolio VaR."""
    np.random.seed(42)
    daily_returns = np.random.normal(
        daily_return, daily_vol, (simulations, days)
    )
    price_paths   = portfolio_value * np.cumprod(1 + daily_returns, axis=1)
    final_values  = price_paths[:, -1]
    var_value     = portfolio_value - np.percentile(final_values, (1-confidence)*100)
    cvar_value    = portfolio_value - np.mean(
        final_values[final_values < portfolio_value - var_value]
    )

    return {
        'VaR_95':        round(var_value, 2),
        'CVaR_95':       round(cvar_value, 2),
        'worst_case':    round(portfolio_value - final_values.min(), 2),
        'best_case':     round(final_values.max() - portfolio_value, 2),
        'median_outcome':round(np.median(final_values), 2)
    }
```

---

## Performance Metrics
```python
def full_performance_report(returns, benchmark_returns=None, risk_free=0.05):
    rf_daily = risk_free / 252
    excess   = returns - rf_daily

    ann_return = returns.mean() * 252
    ann_vol    = returns.std() * np.sqrt(252)
    sharpe     = excess.mean() / excess.std() * np.sqrt(252)

    downside   = returns[returns < 0].std() * np.sqrt(252)
    sortino    = (ann_return - risk_free) / downside

    equity     = (1 + returns).cumprod()
    peak       = equity.cummax()
    drawdown   = (equity - peak) / peak
    max_dd     = drawdown.min()
    calmar     = ann_return / abs(max_dd)

    skew       = returns.skew()
    kurt       = returns.kurtosis()

    report = {
        'Annual Return':   f"{ann_return*100:.2f}%",
        'Annual Vol':      f"{ann_vol*100:.2f}%",
        'Sharpe Ratio':    round(sharpe, 3),
        'Sortino Ratio':   round(sortino, 3),
        'Calmar Ratio':    round(calmar, 3),
        'Max Drawdown':    f"{max_dd*100:.2f}%",
        'Skewness':        round(skew, 3),
        'Kurtosis':        round(kurt, 3),
        'VaR 95%':         f"{value_at_risk(returns)*100:.2f}%",
        'CVaR 95%':        f"{conditional_var(returns)*100:.2f}%",
    }

    if benchmark_returns is not None:
        beta  = returns.cov(benchmark_returns) / benchmark_returns.var()
        alpha = ann_return - (risk_free + beta * (benchmark_returns.mean()*252 - risk_free))
        report['Beta']  = round(beta, 3)
        report['Alpha'] = f"{alpha*100:.2f}%"

    return report
```

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Lookahead bias | Using future data in backtest | Strictly shift signals by 1 bar |
| Survivorship bias | Only test on stocks that survived | Use point-in-time universe |
| Overfitting | Too many parameters, works only on history | Walk-forward test, fewer parameters |
| Ignoring costs | Paper profits vanish in live trading | Model realistic slippage + commission |
| Data snooping | Test 1000 strategies, publish best | Bonferroni correction, hold-out set |
| Short backtest | Not enough data for significance | Minimum 5 years, ideally full cycle |
| P-hacking | Keep tweaking until it works | Pre-register hypothesis before testing |

---

## Best Practices

- **Simplicity wins** — fewer parameters = more robust out-of-sample
- **Walk-forward always** — never evaluate on in-sample data alone
- **Model transaction costs** — include spread, commission, market impact
- **Use point-in-time data** — avoid survivorship and lookahead bias
- **Statistical significance** — t-stat > 2 on Sharpe, sufficient trade count
- **Stress test** — how does strategy perform in 2008, 2020, high vol regimes?
- **Live paper trade first** — 3-6 months before real capital

---

## Related Skills

- **finance-trading-expert**: Overall trading framework
- **risk-management-expert**: Portfolio risk and position sizing
- **fundamental-analysis-expert**: Factor construction from fundamentals
- **macro-economics-expert**: Regime detection and macro factors
- **python-expert**: Implementation of quant models
