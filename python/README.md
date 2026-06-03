# hist

[![PyPI version](https://img.shields.io/pypi/v/yfhist?label=PyPI&color=brightgreen)](https://pypi.org/project/yfhist/)
[![codecov](https://codecov.io/gh/jasonjfoster/hist/graph/badge.svg)](https://app.codecov.io/github/jasonjfoster/hist)
[![Downloads](https://img.shields.io/pypi/dm/yfhist?color=brightgreen)](https://pypistats.org/packages/yfhist)

## Overview

'yfhist' provides simple and efficient access to Yahoo Finance's 'history' API <https://finance.yahoo.com/> for querying and retrieving financial data.

The 'yfhist' package abstracts the complexities of interacting with Yahoo Finance APIs, such as session management, crumb and cookie handling, query construction, date validation, and interval management. This abstraction allows users to focus on retrieving data rather than managing API details. Use cases include retrieving historical data across a range of security types:

* **Equities and ETFs**: end-of-day or intraday Open, High, Low, Close, Volume (OHLCV), and adjusted close prices
* **Indices**: levels over time for benchmarking and research
* **Other tickers**: additional symbols supported by Yahoo Finance where chart data is available

The package supports flexible query capabilities, including customizable date ranges, multiple time intervals, and automatic data validation. It manages interval-specific limitations automatically, such as lookback periods for intraday data and maximum date ranges for minute-level intervals.

The implementation uses standard HTTP libraries to handle API interactions efficiently and is available in both R and 'Python' for accessibility to a broad audience.

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

First, import the package and explore the available interval options:

```python
import yfhist as yfh

print(yfh.data_intervals)
```

Then, to retrieve historical data, use the `get_data()` method:

```python
data = yfh.get_data(["AAPL", "MSFT"])
```
