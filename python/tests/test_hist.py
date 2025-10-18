# import pytest
import time
import pandas as pd
import yfhist as yfh

# @pytest.mark.skip(reason = "long-running test")

test_symbols = ["AAPL", "MSFT"]

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
        from_date = (pd.Timestamp.today() - pd.Timedelta(days = 8)).strftime("%Y-%m-%d")
      else:
        from_date = (pd.Timestamp.today() - pd.Timedelta(days = int(lookback) - 1)).strftime("%Y-%m-%d")

    try:

      response = yfh.get_data(test_symbols, from_date = from_date,
                              interval = field)
      
      # if (response is None):
      #   response = "success"
        
    except:
      response = None

    if response is None:

      errors_ls.append({
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
