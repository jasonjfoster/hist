test_that("input checks", {

  # test data
  test_check_symbols <- "AAPL"
  test_check_today <- Sys.Date()

  # check_symbols
  expect_error(get_data(""),
               "invalid 'symbols'")

  # check_date: 'from_date'
  expect_error(get_data(test_check_symbols, from_date = "2023-13-01"),
               "invalid 'from_date'")

  # check_date: 'to_date'
  expect_error(get_data(test_check_symbols, to_date = "2023-13-01"),
               "invalid 'to_date'")

  # check_interval
  expect_error(get_data(test_check_symbols, interval = "2d"),
               "invalid 'interval'")

  # check_intraday: 'to_date'
  expect_error(get_data(test_check_symbols, from_date = "2023-12-31", to_date = "2023-01-01"),
               "value of 'to_date' must be greater than value of 'from_date'")

  # check_intraday: 'from_date' ("1m" range)
  expect_error(get_data(test_check_symbols, from_date = test_check_today - 10,
                        to_date = test_check_today, interval = "1m"),
               "number of days between 'from_date' and 'to_date' must be less than or equal to 8")

  # check_intraday: 'from_date' ("1m" lookback)
  expect_error(get_data(test_check_symbols, from_date = test_check_today - 30,
                        to_date = test_check_today - 25, interval = "1m"),
               "number of days between 'from_date' and today must be less than 30")

  # check_intraday: 'from_date' (lookback)
  expect_error(get_data(test_check_symbols, from_date = test_check_today - 90,
                        to_date = test_check_today - 40, interval = "5m"),
               "number of days between 'from_date' and today must be less than 60")
  expect_error(get_data(test_check_symbols, from_date = test_check_today - 800,
                        to_date = test_check_today - 750, interval = "60m"),
               "number of days between 'from_date' and today must be less than 730")

  # check_col
  expect_error(get_col(test_check_daily, "price"),
               "invalid 'col'")

  # check_data
  expect_error(get_col(test_check_data, "close"),
               "invalid 'data'")

  # check_adjclose
  expect_error(get_col(test_check_noclose, "adjclose"),
               "'adjclose' and 'close' not found")

})

test_that("input warnings", {

  # check_adjclose
  expect_warning(get_col(test_check_intraday, "adjclose"),
                 "'adjclose' not found; using 'close' (intraday data)",
                 fixed = TRUE)
  expect_silent(get_col(test_check_daily, "adjclose"))

})
