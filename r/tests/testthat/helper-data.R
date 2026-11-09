# test arguments
test_symbols <- list("AAPL", c("AAPL", "MSFT"), c("AAPL", "MSFT", "AMZN"))
test_cols <- c("open", "high", "low", "close", "adjclose", "volume")

# test data
test_check_daily <- data.frame(
  index = as.Date(c("2023-01-03", "2023-01-04")),
  open = c(1, 2),
  high = c(1, 2),
  low = c(1, 2),
  close = c(1, 2),
  adjclose = c(1, 2),
  volume = c(1, 2)
)
attr(test_check_daily, "symbol") <- "AAPL"
test_check_intraday <- test_check_daily[ , colnames(test_check_daily) != "adjclose"]
attr(test_check_intraday, "symbol") <- "AAPL"
test_check_noclose <- test_check_intraday[ , colnames(test_check_intraday) != "close"]
attr(test_check_noclose, "symbol") <- "AAPL"
test_check_data <- test_check_daily
attr(test_check_data, "symbol") <- NULL
