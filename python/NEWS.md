# hist

## Version 0.1.4

* Added the `session` argument to the `get_data` function to reuse a session across calls

* Added input checks for the `col` and `data` arguments of the `get_col` function

* Fixed an issue for symbols with no data in the `get_data` function

* Fixed an issue for the date format of the `from_date` and `to_date` arguments in the `get_data` function

* Fixed an issue for the lookback check of intraday intervals in the `get_data` function

* Fixed an issue for the lookback value of the error messages in the `get_data` function

* Fixed an issue for the error type of the `adjclose` check in the `get_col` function

* Fixed an issue for the `__version__` attribute of the package

* Removed the internal `Check`, `Process`, and `Env` classes from the package namespace

* Added tests for input checks

## Version 0.1.3

* Initial PyPI release
