##' Intervals Data for the Yahoo Finance API
##'
##' A data frame with the available intervals data for the Yahoo Finance API.
##'
##' @format A data frame.
"data_intervals"

check_symbols <- function(symbols) {
  
  if (is.character(symbols)) {
    symbols <- trimws(symbols)
  }
  
  valid_symbols <- (is.character(symbols) && length(symbols) > 0 &&
                      all(nzchar(symbols)) && !anyNA(symbols))
  
  if(!valid_symbols) {
    stop("invalid 'symbols'")
  }
  
}

check_date <- function(date, type) {
  
  valid_date <- as.Date(date, format = "%Y-%m-%d")
  
  if (is.na(valid_date)) {
    stop(paste0("invalid '", type, "'"))
  }
  
}

check_interval <- function(interval) {
  
  valid_interval <- yfhist::data_intervals[["field"]]
  
  if (!interval %in% valid_interval) {
    stop("invalid 'interval'")
  }
  
}

check_intraday <- function(from_date, to_date, interval) {
  
  from_date <- as.Date(from_date)
  to_date <- as.Date(to_date)
  
  valid_lookback <- yfhist::data_intervals[["lookback"]][yfhist::data_intervals[["field"]] == interval]
  
  if (to_date - from_date <= 0) {
    stop("value of 'to_date' must be greater than 'from_date'")
  }
  
  if ((interval == "1m") && (to_date - from_date > 8)) {
    stop("number of days between 'from_date' and 'to_date' must be less than or equal to 8")
  }
  
  if (!is.na(valid_lookback) && (Sys.Date() - from_date >= valid_lookback)) {
    stop(paste0("number of days between 'from_date' and today must be less than ", valid_lookback))
  }
  
}

process_date <- function(date) {
  as.integer(as.POSIXct(date, tz = "UTC"))
}

process_url <- function(params) {
  paste0("?", paste(names(params), params, sep = "=", collapse = "&"))
}

with_env <- function(new_env, code) {
  
  old_env <- list()
  env_names <- names(new_env)
  
  for (i in 1:length(env_names)) {
    
    name <- env_names[i]
    old_env[[name]] <- Sys.getenv(name, unset = NA)
    
  }
  
  on.exit({
    for (i in 1:length(env_names)) {
      
      name <- env_names[i]
      val <- old_env[[name]]
      
      if (is.na(val)) {
        Sys.unsetenv(name)
      } else {
        Sys.setenv(name = val)
      }
      
    }
  }, add = TRUE)
  
  do.call(Sys.setenv, as.list(new_env))
  force(code)
  
}

##' Get the Crumb, Cookies, and Handle for Yahoo Finance API
##'
##' A function to get the crumb, cookies, and handle required to authenticate and interact
##' with the Yahoo Finance API.
##'
##' @return A list containing the following elements:
##' \item{handle}{A curl handle object for subsequent requests.}
##' \item{crumb}{A string representing the crumb value for authentication.}
##' \item{cookies}{A data frame of cookies for the request.}
##' @examples
##' session <- get_session()
##' @export
get_session <- function() {
  
  handle <- curl::new_handle()
  
  api_url <- "https://query1.finance.yahoo.com/v1/test/getcrumb"
  
  headers <- c(
    `Accept` = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    `User-Agent` = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
  )
  
  curl::handle_setheaders(handle, .list = headers)
  
  response <- with_env(c(CURL_SSL_BACKEND = "openssl"), {
    curl::curl_fetch_memory(api_url, handle = handle)
  })
  
  crumb <- rawToChar(response$content)
  
  cookies <- curl::handle_cookies(handle)
  
  result <- list(
    handle = handle,
    crumb = crumb,
    cookies = cookies
  )
  
  return(result)
  
}

##' Get Data from the Yahoo Finance API
##'
##' A function to get data from the Yahoo Finance API for symbols using a date 
##' range and interval.
##'
##' @param symbols string. Symbol or vector of symbols.
##' @param from_date string. Start date in \code{"YYYY-MM-DD"} format (e.g., \code{"2007-01-01"}).
##' @param to_date string. End date in \code{"YYYY-MM-DD"} format.
##' @param interval string. Data interval (see \code{"data_intervals"}).
##' @return A data frame or list of data frame(s) that contains data from the
##' Yahoo Finance API for the specified symbol(s).
##'
##' @examples
##' \dontrun{
##' data <- get_data(c("AAPL", "MSFT"))
##' }
##' @export
get_data <- function(symbols, from_date = "2007-01-01", to_date = NULL, interval = "1d") {
  
  if (is.null(to_date)) {
    to_date <- Sys.time()
  }
  
  check_symbols(symbols)
  check_date(from_date, type = "from_date")
  check_date(to_date, type = "to_date")
  check_interval(interval)
  check_intraday(from_date, to_date, interval)
  
  session <- get_session()
  # crumb <- session[["crumb"]]
  cookies <- session[["cookies"]]
  handle <- session[["handle"]]
  
  intraday <- yfhist::data_intervals[["intraday"]][yfhist::data_intervals[["field"]] == interval]
  
  if (!intraday) {
    
    # inclusive end: use midnight after to_date (exclusive bound)
    to_dt <- as.Date(to_date) + 1
    period2 <- process_date(to_dt)
    
  } else {
    
    # intraday: use exact timestamp
    period2 <- process_date(to_date)
    
  }
  
  params <- list(
    period1 = process_date(from_date),
    period2 = period2,
    interval = interval
  )
  
  headers <- c(
    `Content-Type` = "application/json",
    `Cookie` = paste0(cookies[["name"]], "=", cookies[["value"]], collapse = "; ")
  )
  
  count <- 0
  result_ls <- list()
  
  if (!intraday) {
    cols <- c("index", "open", "high", "low", "close", "adjclose", "volume")
  } else {
    cols <- c("index", "open", "high", "low", "close", "volume")
  }
  
  for (symbol in symbols) {
    
    api_url <- paste0("https://query1.finance.yahoo.com/v8/finance/chart/", symbol, process_url(params))
    
    curl::handle_setheaders(handle, .list = headers) # set headers once!
    
    result_df <- tryCatch({
      
      response <- curl::curl(api_url, handle = handle)
      
      result <- jsonlite::fromJSON(response)
      result[["chart"]][["result"]]
      
    }, error = function(e) {
      return(data.frame())
    })
    
    if (length(result_df) > 0) {
      
      tz <- result_df[["meta"]][["exchangeTimezoneName"]]
      ohlcv <- unlist(result_df[["indicators"]][["quote"]][[1]], recursive = FALSE)
      index <- result_df[["timestamp"]][[1]]
      
      if (!intraday) {
        
        adjclose <- unlist(result_df[["indicators"]][["adjclose"]][[1]], recursive = FALSE)
        index <- as.Date(as.POSIXct(index, origin = "1970-01-01", tz = "UTC"), tz = tz)
        
        result_df <- data.frame(
          "index" = index,
          ohlcv,
          "adjclose" = adjclose
        )
        
      } else {
        
        index <- as.POSIXct(index, origin = "1970-01-01", tz = "UTC")
        index <- as.POSIXct(format(index, tz = tz, usetz = TRUE), tz = tz)
        
        result_df <- data.frame(
          "index" = index,
          ohlcv
        )
        
      }
      
      result_df <- result_df[ , cols]
      result_ls <- append(result_ls, list(result_df))
      
    }
    
    count <- count + 1
    
    if (count %% 5 == 0) {
      
      message("pause one second after five requests")
      Sys.sleep(1)
      
    }
    
  }
  
  if (length(result_ls) == 0) {
    return(data.frame())
  } else if (length(result_ls) == 1) {
    return(result_ls[[1]])
  } else {
    
    names(result_ls) <- symbols
    
    return(result_ls)
    
  }
  
}