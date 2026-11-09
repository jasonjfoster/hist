# hist

## Version 0.1.4

* Added the `session` argument to the `get_data` function to reuse a session across calls

* Added an input check for the `data` argument of the `get_col` function

* Fixed an issue for symbols with no data in the `get_data` function

* Fixed an issue for the date range and lookback checks of intraday intervals in the `get_data` function

* Fixed an issue for restoring the `CURL_SSL_BACKEND` environment variable in the `get_session` function

* Added tests for input checks

## Version 0.1.3

* Initial CRAN release
