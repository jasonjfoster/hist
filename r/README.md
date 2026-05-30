# hist

[![GitHub Actions](https://github.com/jasonjfoster/hist/actions/workflows/check-standard.yaml/badge.svg)](https://github.com/jasonjfoster/hist/actions/workflows/check-standard.yaml)
[![CRAN version](https://www.r-pkg.org/badges/version/yfhist)](https://cran.r-project.org/package=yfhist)
[![codecov](https://codecov.io/gh/jasonjfoster/hist/graph/badge.svg)](https://app.codecov.io/github/jasonjfoster/hist)
[![Downloads](https://cranlogs.r-pkg.org/badges/yfhist?color=brightgreen)](https://www.r-pkg.org/pkg/yfhist)

## Overview

'yfhist' provides simple and efficient access to Yahoo Finance's 'history' API <https://finance.yahoo.com/> for querying and retrieving financial data.

The 'yfhist' package abstracts the complexities of interacting with Yahoo Finance APIs, such as session management, crumb and cookie handling, query construction, date validation, and interval management. This abstraction allows users to focus on retrieving data rather than managing API details. Use cases include retrieving historical data across a range of security types:

* **Equities and ETFs**: end-of-day or intraday Open, High, Low, Close, Volume (OHLCV), and adjusted close prices
* **Indices**: levels over time for benchmarking and research
* **Other tickers** supported by Yahoo Finance where chart data is available

The package supports flexible query capabilities, including customizable date ranges, multiple time intervals, and automatic data validation. It manages interval-specific limitations automatically, such as lookback periods for intraday data and maximum date ranges for minute-level intervals.

The implementation uses standard HTTP libraries to handle API interactions efficiently and is available in both R and 'Python' for accessibility to a broad audience.

## Installation

* Install the released version from CRAN:

```r
install.packages("yfhist")
```

* Or the development version from GitHub:

```r
# install.packages("pak")
pak::pak("jasonjfoster/hist/r")
```

## Usage

First, load the package and explore the available interval options:

```r
library(yfhist)

print(data_intervals)
```

Then, to retrieve historical data, use the `get_data()` function:

```r
data <- get_data(c("AAPL", "MSFT"))
```
