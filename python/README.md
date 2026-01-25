# hist

[![PyPI version](https://img.shields.io/pypi/v/yfhist?label=PyPI&color=brightgreen)](https://pypi.org/project/yfhist/)
[![codecov](https://codecov.io/gh/jasonjfoster/hist/graph/badge.svg)](https://app.codecov.io/github/jasonjfoster/hist)
[![Downloads](https://img.shields.io/pypi/dm/yfhist?color=brightgreen)](https://pypistats.org/packages/yfhist)

## Overview

'hist' is a package that provides simple and efficient access to Yahoo Finance's 'history' API <https://finance.yahoo.com/> for querying and retrieval of financial data.

The core functionality of the 'hist' package abstracts the complexities of interacting with Yahoo Finance APIs, such as session management, crumb and cookie handling, query construction, date validation, and interval management. This abstraction allows users to focus on retrieving data rather than managing API details. Use cases include historical data across a range of security types:

* **Equities & ETFs**: end-of-day or intraday Open, High, Low, Close, Volume (OHLCV), and adjusted close prices
* **Indices**: levels over time for benchmarking and research
* **Other tickers** supported by Yahoo Finance where chart data is available

The package supports flexible query capabilities, including customizable date ranges, multiple time intervals, and automatic data validation. It automatically manages interval-specific limitations, such as lookback periods for intraday data and maximum date ranges for minute-level intervals.

The implementation leverages standard HTTP libraries to handle API interactions efficiently and provides support for both R and 'Python' to ensure accessibility for a broad audience.

## Installation

* Install the released version from PyPI:

```python
pip install yfhist
```

* Or the development version from GitHub:

```python
pip install git+https://github.com/jasonjfoster/hist.git@main#subdirectory=python
```

## Usage

First, load the package and explore the available interval options:

```python
import yfhist as yfh

print(yfh.data_intervals)
```

Then, to retrieve historical data, use the the `get_data` method:

```python
data = yfh.get_data(["AAPL", "MSFT"])
```
