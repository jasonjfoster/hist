# hist

[![GitHub Actions](https://github.com/jasonjfoster/hist/actions/workflows/check-standard.yaml/badge.svg)](https://github.com/jasonjfoster/hist/actions/workflows/check-standard.yaml)
[![CRAN version](https://www.r-pkg.org/badges/version/yfhist)](https://cran.r-project.org/package=yfhist)
[![codecov](https://codecov.io/gh/jasonjfoster/hist/graph/badge.svg)](https://app.codecov.io/github/jasonjfoster/hist)
[![Downloads](https://cranlogs.r-pkg.org/badges/yfhist?color=brightgreen)](https://www.r-pkg.org/pkg/yfhist)

## Overview

`yfhist` is a package that provides simple and efficient access to Yahoo Finance's 'history' API <`https://finance.yahoo.com/`> for querying and retrieval of financial data.

The core functionality of the `yfhist` package abstracts the complexities of interacting with Yahoo Finance APIs, such as session management, crumb and cookie handling, query construction, date validation, and interval management. This abstraction allows users to focus on retrieving data rather than managing API details. Use cases include historical data across a range of security types:

* **Equities & ETFs**: end-of-day or intraday Open, High, Low, Close, Volume (OHLCV), and adjusted close prices
* **Indices**: levels over time for benchmarking and research
* **Other tickers** supported by Yahoo Finance where chart data is available

The package supports flexible query capabilities, including customizable date ranges, multiple time intervals, and automatic data validation. It automatically manages interval-specific limitations, such as lookback periods for intraday data and maximum date ranges for minute-level intervals.

The implementation leverages standard HTTP libraries to handle API interactions efficiently and provides support for both R and 'Python' to ensure accessibility for a broad audience.

## Installation

* Install the released version from CRAN:

```r
install.packages("yfhist")
```

* Or the development version from GitHub:

```r
# install.packages("devtools")
devtools::install_github("jasonjfoster/hist/r")
```

## Usage

First, load the package and explore the available interval options:

```r
library(yfhist)

print(data_intervals)
```

Then, to retrieve historical data, use the the `get_data` function:

```r
data <- get_data(c("AAPL", "MSFT"))
```
