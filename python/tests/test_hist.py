# import pytest
import time
import pandas as pd
import yfhist as yfh

# @pytest.mark.skip(reason = "long-running test")

test_symbols = [["AAPL"], ["AAPL", "MSFT"], ["AAPL", "MSFT", "AMZN"]]
test_cols = ["open", "high", "low", "close", "adjclose", "volume"]

def test_that(): # valid 'from_date' and 'interval'

  fields = yfh.data_intervals["field"]

  count = 0
  result_ls = []
  errors_ls = []

  for field in fields:
    
    lookback = yfh.data_intervals.loc[yfh.data_intervals["field"] == field, "lookback"].item()
    
    if pd.isna(lookback):
      lookback = None
    
    if (lookback is None):
      from_date = "2007-01-01"
    else:
      if (field == "1m"):
        
        to_date = pd.Timestamp.now(tz = "UTC")
        from_date = to_date - pd.Timedelta(days = 8)
        
      else:
        
        to_date = None
        from_date = (pd.Timestamp.today().normalize() - pd.Timedelta(days = int(lookback) - 1))

    for symbols in test_symbols:
      
      try:
  
        data = yfh.get_data(symbols, from_date = from_date,
                            to_date = to_date, interval = field)
        
        for col in test_cols:
          response = yfh.get_col(data, col)
        
        # if (response is None):
        #   response = "success"
          
      except:
        response = None
  
      if response is None:
  
        errors_ls.append({
          "symbols": ", ".join(symbols),
          "field": field
        })
  
      count += 1
          
      if (count % 5 == 0):
              
        print("pause one second after five requests")
        time.sleep(1)

  if len(errors_ls) > 0:
    result_ls.extend(errors_ls)

  result_df = pd.DataFrame(result_ls)

  pd.testing.assert_frame_equal(result_df, pd.DataFrame())
