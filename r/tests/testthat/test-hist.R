test_that("valid 'from_date' and 'interval'", {
  
  fields <- yfhist::data_intervals[["field"]]
  
  count <- 0
  result_ls <- list()
  errors_ls <- list()
  
  for (field in fields) {
    
    lookback <- yfhist::data_intervals[["lookback"]][yfhist::data_intervals[["field"]] == field]
    
    if (is.na(lookback)) {
      lookback <- NULL
    }
    
    if (is.null(lookback)) {
      from_date <- "2007-01-01"
    } else {
      
      if (field == "1m") {
        from_date <- Sys.Date() - 8
      } else {
        from_date <- Sys.Date() - lookback + 1
      }
      
    }
    
    response <- tryCatch({
      
      data <- suppressWarnings(get_data(test_symbols, from_date = from_date,
                                        interval = field))
      
      for (i in 1:length(test_cols)) {
        response <- get_col(data, test_cols[i])
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
        field = field
      )
    
      error_ls <- append(errors_ls, list(error))
      
    }
    
    count <- count + 1
    
    if (count %% 5 == 0) {
      
      message("pause one second after five requests")
      Sys.sleep(1)
      
    }
  
  }
  
  if (length(errors_ls) > 0) {
    
    result <- do.call(rbind, errors_ls)
    result_ls <- append(result_ls, list(result))
    
  }
  
  expect_equal(result_ls, list())

})