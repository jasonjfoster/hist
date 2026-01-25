test_that("valid 'from_date' and 'interval'", {

  skip("long-running test")
  
  fields <- yfhist::data_intervals[["field"]]
  
  count <- 0
  result_ls <- list()
  errors_ls <- list()
  
  for (field in fields) {
    
    lookback <- yfhist::data_intervals[["lookback"]][yfhist::data_intervals[["field"]] == field]
    
    if (is.na(lookback)) {
      lookback <- NULL
    }
    
    to_date <- as.POSIXct(Sys.time(), tz = "UTC")
    
    if (is.null(lookback)) {
      from_date <- "2007-01-01"
    } else {
      if (field == "1m") {
        from_date <- as.POSIXct(to_date - 8 * 24 * 3600, tz = "UTC")
      } else {
        from_date <- as.POSIXct(to_date - (lookback - 1) * 24 * 3600, tz = "UTC")
      }
    }
    
    for (symbols in test_symbols) {
      
      response <- tryCatch({
        
        data <- suppressWarnings(get_data(symbols, from_date = from_date,
                                          to_date = to_date, interval = field))
        
        for (col in test_cols) {
          response <- get_col(data, col)
        }
        
        # if (is.null(response)) {
        #   response <- "success"
        # } else {
        response
        # }
        
      }, error = function(e) {
        NULL
      })
      
      if (is.null(response)) {
        
        error <- data.frame(
          symbols = paste(symbols, collapse = ","),
          field = field
        )
        
        errors_ls <- append(errors_ls, list(error))
        
      }
      
      count <- count + 1
      
      if (count %% 5 == 0) {
        
        message("pause one second after five requests")
        Sys.sleep(1)
        
      }
      
    }
    
  }
  
  if (length(errors_ls) > 0) {
    
    result <- do.call(rbind, errors_ls)
    result_ls <- append(result_ls, list(result))
    
  }
  
  expect_equal(result_ls, list())

})