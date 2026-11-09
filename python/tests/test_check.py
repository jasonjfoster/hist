import re
import warnings
import pytest
import pandas as pd
import yfhist as yfh

# test data
test_check_daily = pd.DataFrame({
  "index": pd.to_datetime(["2023-01-03", "2023-01-04"]).date,
  "open": [1, 2],
  "high": [1, 2],
  "low": [1, 2],
  "close": [1, 2],
  "adjclose": [1, 2],
  "volume": [1, 2]
})
test_check_daily.attrs["symbol"] = "AAPL"
test_check_intraday = test_check_daily.drop(columns = "adjclose")
test_check_intraday.attrs["symbol"] = "AAPL"
test_check_noclose = test_check_intraday.drop(columns = "close")
test_check_noclose.attrs["symbol"] = "AAPL"
test_check_data = test_check_daily.copy()
test_check_data.attrs.pop("symbol", None)

def test_check(): # input checks

  # test data
  test_check_symbols = "AAPL"
  test_check_today = pd.Timestamp.now(tz = "UTC").normalize()

  # check_symbols
  with pytest.raises(ValueError, match = re.escape("invalid 'symbols'")):
    yfh.get_data("")

  # check_date: 'from_date'
  with pytest.raises(ValueError, match = re.escape("invalid 'from_date'")):
    yfh.get_data(test_check_symbols, from_date = "2023-13-01")

  # check_date: 'to_date'
  with pytest.raises(ValueError, match = re.escape("invalid 'to_date'")):
    yfh.get_data(test_check_symbols, to_date = "2023-13-01")

  # check_interval
  with pytest.raises(ValueError, match = re.escape("invalid 'interval'")):
    yfh.get_data(test_check_symbols, interval = "2d")

  # check_intraday: 'to_date'
  with pytest.raises(ValueError, match = re.escape("value of 'to_date' must be greater than value of 'from_date'")):
    yfh.get_data(test_check_symbols, from_date = "2023-12-31", to_date = "2023-01-01")

  # check_intraday: 'from_date' ("1m" range)
  with pytest.raises(ValueError, match = re.escape("number of days between 'from_date' and 'to_date' must be less than or equal to 8")):
    yfh.get_data(test_check_symbols, from_date = test_check_today - pd.Timedelta(days = 10),
                 to_date = test_check_today, interval = "1m")

  # check_intraday: 'from_date' ("1m" lookback)
  with pytest.raises(ValueError, match = re.escape("number of days between 'from_date' and today must be less than 30")):
    yfh.get_data(test_check_symbols, from_date = test_check_today - pd.Timedelta(days = 30),
                 to_date = test_check_today - pd.Timedelta(days = 25), interval = "1m")

  # check_intraday: 'from_date' (lookback)
  with pytest.raises(ValueError, match = re.escape("number of days between 'from_date' and today must be less than 60")):
    yfh.get_data(test_check_symbols, from_date = test_check_today - pd.Timedelta(days = 90),
                 to_date = test_check_today - pd.Timedelta(days = 40), interval = "5m")
  with pytest.raises(ValueError, match = re.escape("number of days between 'from_date' and today must be less than 730")):
    yfh.get_data(test_check_symbols, from_date = test_check_today - pd.Timedelta(days = 800),
                 to_date = test_check_today - pd.Timedelta(days = 750), interval = "60m")

  # check_col
  with pytest.raises(ValueError, match = re.escape("invalid 'col'")):
    yfh.get_col(test_check_daily, "price")

  # check_data
  with pytest.raises(ValueError, match = re.escape("invalid 'data'")):
    yfh.get_col(test_check_data, "close")

  # check_adjclose
  with pytest.raises(ValueError, match = re.escape("'adjclose' and 'close' not found")):
    yfh.get_col(test_check_noclose, "adjclose")

def test_warning(): # input warnings

  # check_adjclose
  with pytest.warns(UserWarning, match = re.escape("'adjclose' not found; using 'close' (intraday data)")):
    yfh.get_col(test_check_intraday, "adjclose")
  with warnings.catch_warnings():
    warnings.simplefilter("error")
    yfh.get_col(test_check_daily, "adjclose")
